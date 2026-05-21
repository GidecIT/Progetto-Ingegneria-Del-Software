from __future__ import annotations

import pytest

from participium.core.exceptions import AuthorizationError, ValidationError
from participium.models.message import Message
from participium.models.report import Report, ReportStatusHistory
from participium.models.enums import Role
from participium.models.user import User
from participium.services.messaging_service import MessagingService
from unittest.mock import Mock



AUTHORIZED_USER = User(id=1, username="mario_r", first_name="Mario", last_name="Rossi", role=Role.CITIZEN)
UNAUTHORIZED_USER = User(id=2, username="luca_b", first_name="Luca", last_name="Bianchi", role=Role.CITIZEN)
OPERATOR_USER = User(id=3, username="op1", role=Role.OPERATOR, first_name="Op", last_name="One")


REPORT1 = Report(id=10, reporter_id=AUTHORIZED_USER.id)
REPORT1.status_history = [
    ReportStatusHistory(changed_by=OPERATOR_USER)
]

REPORT_NO_RECIPIENT = Report(id=11, reporter_id=AUTHORIZED_USER.id)
REPORT_NO_RECIPIENT.status_history = []



VALID_BODY = "Segnalazione"
EMPTY_BODY = ""
WHITESPACE_BODY = "   "
SINGLE_CHAR_BODY = "a"


@pytest.fixture
def messaging_service() -> MessagingService:
    message_repo = Mock()
    message_repo.list_for_report.return_value = []
    
    return MessagingService(
        session=Mock(),
        report_repository=Mock(),
        message_repository=message_repo,
        notification_service=Mock(),
    )

def test_send_message_success(messaging_service: MessagingService) -> None:
    # MS01
    
    message = messaging_service.send_message(REPORT1, AUTHORIZED_USER, VALID_BODY)
    
    assert isinstance(message, Message)
    assert message.body == VALID_BODY
    assert message.sender_id == AUTHORIZED_USER.id
    assert message.report_id == REPORT1.id


def test_send_message_single_char_body(messaging_service: MessagingService) -> None:
    # MSB01
    
    message = messaging_service.send_message(REPORT1, AUTHORIZED_USER, SINGLE_CHAR_BODY)
    
    assert isinstance(message, Message)
    assert message.body == SINGLE_CHAR_BODY


def test_send_message_unauthorized_sender(messaging_service: MessagingService) -> None:
    # MS02
    
    with pytest.raises(AuthorizationError):
        messaging_service.send_message(REPORT1, UNAUTHORIZED_USER, VALID_BODY)


def test_send_message_empty_body(messaging_service: MessagingService) -> None:
    # MS03, MSB03
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT1, AUTHORIZED_USER, EMPTY_BODY)


def test_send_message_whitespace_body(messaging_service: MessagingService) -> None:
    # MS04, MSB04
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT1, AUTHORIZED_USER, WHITESPACE_BODY)


def test_send_message_none_body(messaging_service: MessagingService) -> None:
    # MS05

    pytest.xfail(reason=" body=None ")
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT1, AUTHORIZED_USER, None) # type: ignore

def test_send_message_recipient_not_resolvable(messaging_service: MessagingService) -> None:
    # MS06
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT_NO_RECIPIENT, AUTHORIZED_USER, VALID_BODY)
