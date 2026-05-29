from __future__ import annotations
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from participium.services.email_service import (
    BaseEmailGateway,
    ConsoleEmailGateway,
    SmtpEmailGateway,
    build_email_gateway,
)


class TestBaseEmailGateway:
    def test_base_send_executes_without_errors(self, capsys):
        gateway = BaseEmailGateway()
        gateway.send("test@example.com", "Subject", "Body")
        captured = capsys.readouterr()
        assert "Simulating email send operation." in captured.out


class TestConsoleEmailGateway:
    def test_console_send_creates_file_with_correct_content(self, tmp_path):
        outbox_dir = tmp_path / "mail_out"
        sender = "sender@participium.it"
        gateway = ConsoleEmailGateway(outbox_dir=outbox_dir, sender=sender)

        gateway.send(
            recipient="recipient@example.com",
            subject="Test Subject",
            body="This is the mail body.",
        )

        generated_files = list(outbox_dir.glob("*.txt"))
        assert len(generated_files) == 1
        
        file_content = generated_files[0].read_text(encoding="utf-8")
        assert f"FROM: {sender}" in file_content
        assert "TO: recipient@example.com" in file_content
        assert "SUBJECT: Test Subject" in file_content
        assert "This is the mail body." in file_content


class TestSmtpEmailGateway:
    def test_smtp_send_with_tls_and_login(self, mock_smtp):
        gateway = SmtpEmailGateway(
            host="smtp.test.com",
            port=25,
            username="my_user",
            password="my_password",
            sender="from@test.com",
            use_tls=True,
        )

        gateway.send("to@test.com", "Mail Subject", "Mail Body")

        mock_smtp.starttls.assert_called_once()
        mock_smtp.login.assert_called_once_with("my_user", "my_password")
        mock_smtp.send_message.assert_called_once()

    def test_smtp_send_without_tls_and_without_credentials(self, mock_smtp):
        gateway = SmtpEmailGateway(
            host="smtp.test.com",
            port=25,
            username=None,
            password=None,
            sender="from@test.com",
            use_tls=False,
        )

        gateway.send("to@test.com", "Mail Subject", "Mail Body")

        mock_smtp.starttls.assert_not_called()
        mock_smtp.login.assert_not_called()
        mock_smtp.send_message.assert_called_once()


class TestBuildEmailGatewayFactory:
    def test_build_factory_returns_smtp_gateway_when_configured(self, mock_settings):
        mock_settings.mail_backend = "smtp"
        mock_settings.smtp_host = "smtp.example.com"

        gateway = build_email_gateway(mock_settings)

        assert isinstance(gateway, SmtpEmailGateway)
        assert gateway.host == "smtp.example.com"

    def test_build_factory_fallback_to_console_gateway_if_backend_not_smtp(self, mock_settings):
        mock_settings.mail_backend = "console"

        gateway = build_email_gateway(mock_settings)

        assert isinstance(gateway, ConsoleEmailGateway)

    def test_build_factory_fallback_to_console_gateway_if_host_missing(self, mock_settings):
        mock_settings.mail_backend = "smtp"
        mock_settings.smtp_host = None

        gateway = build_email_gateway(mock_settings)

        assert isinstance(gateway, ConsoleEmailGateway)