from __future__ import annotations

import pytest

from participium.core.exceptions import AuthorizationError, ValidationError
from participium.models.message import Message
from participium.models.report import Report
from participium.models.user import User
from participium.services.messaging_service import MessagingService

@pytest.fixture
def messaging_service() -> MessagingService:
    return MessagingService()

@pytest.fixture
def user1() -> User:
    return User(id=1, username="user1")

@pytest.fixture
def user2() -> User:
    return User(id=2, username="user2")

@pytest.fixture
def user3() -> User:
    return User(id=None, username="user3")

@pytest.fixture
def report1() -> Report:
    return Report(id=1, reporter_id=1)

@pytest.fixture
def report2() -> Report:
    return Report(id=1, reporter_id=None)

@pytest.fixture
def report3() -> Report:
    return Report(id=None, reporter_id=1)

@pytest.mark.skip(reason="Disabled.")
def test_ms01_all_none(messaging_service: MessagingService) -> None:
    """Tutti e tre i campi omessi"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(None, None, None)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms02_user_only(messaging_service: MessagingService, user1: User) -> None:
    """User valido ma altri due campi omessi"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(None, user1, None)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms03_report_only(messaging_service: MessagingService, report1: Report) -> None:
    """Report valido ma altri due campi omessi"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, None, None)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms04_body_only(messaging_service: MessagingService) -> None:
    """Body valido ma altri due campi omessi"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(None, None, "ciao")  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms05_report_user_valid_body_none(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    """Body omesso"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, None)  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms06_report_body_valid_user_none(messaging_service: MessagingService, report1: Report) -> None:
    """User omesso"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, None, "ciao")  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms07_user_body_valid_report_none(messaging_service: MessagingService, user1: User) -> None:
    """Report omesso"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(None, user1, "ciao")  # type: ignore

@pytest.mark.skip(reason="Disabled.")
def test_ms08_empty_body(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    """Body vuoto"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, "")

@pytest.mark.skip(reason="Disabled.")
def test_ms09_unauthorized_sender(messaging_service: MessagingService, report1: Report, user2: User) -> None:
    """Report non fatto dal mittente"""
    with pytest.raises(AuthorizationError):
        messaging_service.send_message(report1, user2, "ciao")

@pytest.mark.skip(reason="Disabled.")
def test_ms10_user_no_id(messaging_service: MessagingService, report1: Report, user3: User) -> None:
    """User senza un campo id"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user3, "ciao")

@pytest.mark.skip(reason="Disabled.")
def test_ms11_report_no_reporter_id(messaging_service: MessagingService, report2: Report, user1: User) -> None:
    """Report senza un campo reporter_id"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report2, user1, "ciao")

@pytest.mark.skip(reason="Disabled.")
def test_ms12_report_no_id(messaging_service: MessagingService, report3: Report, user1: User) -> None:
    """Report senza un campo id"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report3, user1, "ciao")

@pytest.mark.skip(reason="Disabled.")
def test_ms13_success(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    """Tutto valido"""
    message = messaging_service.send_message(report1, user1, "ciao")
    assert isinstance(message, Message)
    assert message.body == "ciao"
    assert message.sender_id == user1.id
    assert message.report_id == report1.id

# Boundary Tests
@pytest.mark.skip(reason="Disabled.")
def test_msb01_min_length(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    """Minima lunghezza valida"""
    message = messaging_service.send_message(report1, user1, "a")
    assert isinstance(message, Message)
    assert message.body == "a"

@pytest.mark.skip(reason="Disabled.")
def test_msb02_only_whitespace(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    """Solo spazio bianco"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, " ")

@pytest.mark.skip(reason="Disabled.")
def test_msb03_empty_string(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    """Stringa vuota"""
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, "")
