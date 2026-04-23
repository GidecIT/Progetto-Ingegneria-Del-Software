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
def report1() -> Report:
    return Report(id=1, reporter_id=1)

def test_ms01_empty_body(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, "")

def test_ms02_unauthorized_sender(messaging_service: MessagingService, report1: Report, user2: User) -> None:
    with pytest.raises(AuthorizationError):
        messaging_service.send_message(report1, user2, "ciao")

def test_ms03_success(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    message = messaging_service.send_message(report1, user1, "ciao")
    assert isinstance(message, Message)
    assert message.body == "ciao"
    assert message.sender_id == user1.id
    assert message.report_id == report1.id

def test_msb01_exact_boundary(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    message = messaging_service.send_message(report1, user1, ".")
    assert isinstance(message, Message)
    assert message.body == "."

def test_msb02_immediately_below_whitespace(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, " ")

def test_msb03_immediately_below_empty(messaging_service: MessagingService, report1: Report, user1: User) -> None:
    with pytest.raises(ValidationError):
        messaging_service.send_message(report1, user1, "")
