from __future__ import annotations

import pytest

from participium.core.exceptions import AuthorizationError, ValidationError
from participium.models.message import Message
from participium.models.report import Report
from participium.models.user import User
from participium.services.messaging_service import MessagingService

AUTHORIZED_USER = User(id=1, username="mario_r")
UNAUTHORIZED_USER = User(id=2, username="luca_b")

REPORT1 = Report(id=10, reporter_id=AUTHORIZED_USER.id)
REPORT_NO_RECIPIENT = Report(id=11, reporter_id=AUTHORIZED_USER.id)

VALID_BODY = "Segnalazione"
EMPTY_BODY = ""
WHITESPACE_BODY = "   "
SINGLE_CHAR_BODY = "a"


@pytest.fixture
def seed_send_message_data() -> None:
    # È necessiario riempire il sistema con il report e gli utenti 
    # necesari per utilizare `MessagingService.send_message`.
    #
    # Configurazione da usare:
    # - 'AUTHORIZED_USER' ha accesso a 'REPORT1'
    # - 'UNAUTHORIZED_USER' non ha accesso a  `REPORT1`
    # - 'REPORT_NO_RECIPIENT' deve fallire la risuluzione del mittente
    pass


@pytest.mark.skip(reason="Disabled.")
def test_send_message_success(seed_send_message_data: None) -> None:
    # MS01
    messaging_service = MessagingService()
    
    message = messaging_service.send_message(REPORT1, AUTHORIZED_USER, VALID_BODY)
    
    assert isinstance(message, Message)
    assert message.body == VALID_BODY
    assert message.sender_id == AUTHORIZED_USER.id
    assert message.report_id == REPORT1.id


@pytest.mark.skip(reason="Disabled.")
def test_send_message_single_char_body(seed_send_message_data: None) -> None:
    # MSB01
    messaging_service = MessagingService()
    
    message = messaging_service.send_message(REPORT1, AUTHORIZED_USER, SINGLE_CHAR_BODY)
    
    assert isinstance(message, Message)
    assert message.body == SINGLE_CHAR_BODY


@pytest.mark.skip(reason="Disabled.")
def test_send_message_unauthorized_sender(seed_send_message_data: None) -> None:
    # MS02
    messaging_service = MessagingService()
    
    with pytest.raises(AuthorizationError):
        messaging_service.send_message(REPORT1, UNAUTHORIZED_USER, VALID_BODY)


@pytest.mark.skip(reason="Disabled.")
def test_send_message_empty_body(seed_send_message_data: None) -> None:
    # MS03, MSB03
    messaging_service = MessagingService()
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT1, AUTHORIZED_USER, EMPTY_BODY)


@pytest.mark.skip(reason="Disabled.")
def test_send_message_whitespace_body(seed_send_message_data: None) -> None:
    # MS04, MSB04
    messaging_service = MessagingService()
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT1, AUTHORIZED_USER, WHITESPACE_BODY)


@pytest.mark.skip(reason="Disabled.")
def test_send_message_none_body(seed_send_message_data: None) -> None:
    # MS05
    messaging_service = MessagingService()
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT1, AUTHORIZED_USER, None) # type: ignore


@pytest.mark.skip(reason="Disabled.")
def test_send_message_recipient_not_resolvable(seed_send_message_data: None) -> None:
    # MS06
    messaging_service = MessagingService()
    
    with pytest.raises(ValidationError):
        messaging_service.send_message(REPORT_NO_RECIPIENT, AUTHORIZED_USER, VALID_BODY)
