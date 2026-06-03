from __future__ import annotations
import pytest


class TestAuthController:
    def test_register_delegates_to_service(self, auth_controller, mock_user):
        expected_url = "https://ex.com/verify/token123"
        auth_controller.auth_service.register_user.return_value = (mock_user, expected_url)
        payload = {"username": "user1", "password": "pwd"}

        user, url = auth_controller.register(payload, "https://ex.com/verify")

        assert user == mock_user
        assert url == expected_url
        auth_controller.auth_service.register_user.assert_called_once_with(
            payload, "https://ex.com/verify"
        )

    def test_verify_email_delegates_to_service(self, auth_controller, mock_user):
        auth_controller.auth_service.verify_email.return_value = mock_user

        result = auth_controller.verify_email("token123")

        assert result == mock_user
        auth_controller.auth_service.verify_email.assert_called_once_with("token123")

    def test_login_delegates_to_service(self, auth_controller, mock_user):
        auth_controller.auth_service.authenticate.return_value = mock_user

        result = auth_controller.login("user1", "pwd")

        assert result == mock_user
        auth_controller.auth_service.authenticate.assert_called_once_with("user1", "pwd")