from __future__ import annotations

from unittest.mock import Mock
import pytest

from participium.services.messaging_service import MessagingService
from participium.models.enums import Role

pytestmark = pytest.mark.whitebox

def create_mocks(sender_role, msg_senders_roles, status_changers_roles):
    mock_reporter = Mock(spec=["id", "role"])
    mock_reporter.id = 999
    
    mock_sender = Mock(spec=["id", "role"])
    mock_sender.role = sender_role
    
    status_history = []
    status_changers = []
    for role in status_changers_roles:
        event = Mock(spec=["changed_by"])
        if role is None:
            event.changed_by = None
            status_changers.append(None)
        else:
            changer = Mock(spec=["role"])
            changer.role = role
            event.changed_by = changer
            status_changers.append(changer)
        status_history.append(event)
        
    mock_report = Mock(spec=["id", "reporter", "status_history"])
    mock_report.id = 1
    mock_report.reporter = mock_reporter
    mock_report.status_history = status_history
    
    mock_msg_repo = Mock()
    messages = []
    message_senders = []
    for role in msg_senders_roles:
        msg = Mock(spec=["sender"])
        if role is None:
            msg.sender = None
            message_senders.append(None)
        else:
            m_sender = Mock(spec=["role"])
            m_sender.role = role
            msg.sender = m_sender
            message_senders.append(m_sender)
        messages.append(msg)
    mock_msg_repo.list_for_report.return_value = messages
    
    return {
        "reporter": mock_reporter,
        "sender": mock_sender,
        "report": mock_report,
        "msg_repo": mock_msg_repo,
        "message_senders": message_senders,
        "status_changers": status_changers
    }

@pytest.mark.parametrize(
    "sender_role, msg_senders_roles, status_changers_roles, expected_key, expected_idx",
    [
        (Role.ADMIN, [], [], "reporter", None),
        (Role.OPERATOR, [], [], "reporter", None),
        (Role.CITIZEN, [Role.ADMIN], [], "msg", 0),
        (Role.CITIZEN, [Role.OPERATOR], [], "msg", 0),
        (Role.CITIZEN, [Role.CITIZEN], [Role.ADMIN], "status", 0),
        (Role.CITIZEN, [Role.CITIZEN], [Role.OPERATOR], "status", 0),
        (Role.CITIZEN, [], [], None, None),
        (Role.CITIZEN, [Role.CITIZEN], [Role.CITIZEN], None, None),
        (Role.CITIZEN, [Role.ADMIN, None], [], "msg", 0),
        (Role.CITIZEN, [Role.CITIZEN], [Role.OPERATOR, None], "status", 0),

        (Role.CITIZEN, [], [Role.ADMIN], "status", 0),
        (Role.CITIZEN, [Role.ADMIN], [], "msg", 0),
        (Role.CITIZEN, [Role.ADMIN, Role.CITIZEN], [], "msg", 0),
        (Role.CITIZEN, [Role.CITIZEN], [], None, None),
        (Role.CITIZEN, [Role.CITIZEN], [Role.OPERATOR], "status", 0),
        (Role.CITIZEN, [Role.CITIZEN], [Role.OPERATOR, Role.CITIZEN], "status", 0),
    ],
)

def test_resolve_recipient(sender_role, msg_senders_roles, status_changers_roles, expected_key, expected_idx): 
    mocks = create_mocks(sender_role, msg_senders_roles, status_changers_roles)
    
    service = MessagingService(message_repository=mocks["msg_repo"])
    
    result = service._resolve_recipient(mocks["report"], mocks["sender"])
    
    if expected_key == "reporter":
        assert result == mocks["reporter"]
    elif expected_key == "msg":
        assert result == mocks["message_senders"][expected_idx]
    elif expected_key == "status":
        assert result == mocks["status_changers"][expected_idx]
    else:
        assert result is None
