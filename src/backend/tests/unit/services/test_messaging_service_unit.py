from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest

from participium.core.exceptions import ValidationError

class TestCanAccessThread:
    def test_can_access_thread_user_None(self, messaging_service, mock_report):
        result = messaging_service.can_access_thread(mock_report, None)
        assert result == False 
    
    def test_can_access_thread_user_admin(self, messaging_service, mock_report, mock_admin):
        result = messaging_service.can_access_thread(mock_report, mock_admin)
        assert result == True 
    
    def test_can_access_thread_operator_same_category(self, messaging_service, mock_report, mock_operator):
        mock_report.category_id = mock_operator.category_id
        result = messaging_service.can_access_thread(mock_report, mock_operator)
        assert result == True 
    
    def test_can_access_thread_his_report(self, messaging_service, mock_report, mock_operator):
        mock_report.reporter_id= mock_operator.id
        result = messaging_service.can_access_thread(mock_report, mock_operator)
        assert result == True 

    def test_can_access_thread_not_his_report(self, messaging_service, mock_report, mock_operator):
        result = messaging_service.can_access_thread(mock_report, mock_operator)
        assert result == False 

class TestListMessages:
    def test_list_messages_empty(self, messaging_service, mock_report, mock_user):
        messaging_service._ensure_access = Mock(return_value=True)
        messaging_service.message_repository.list_for_report.return_value = []
        result = messaging_service.list_messages(mock_report, mock_user)
        assert result == []
        messaging_service._ensure_access.assert_called_once_with(mock_report, mock_user)
    
    def test_list_messages_with_report(self, messaging_service, mock_report, mock_user):
        messaging_service._ensure_access = Mock(return_value=True)
        fake_message = Mock() 
        messaging_service.message_repository.list_for_report.return_value = [fake_message]
        result = messaging_service.list_messages(mock_report, mock_user)
        assert result == [fake_message]
        messaging_service._ensure_access.assert_called_once_with(mock_report, mock_user)

class TestSendMessage:
    def test_send_message_not_cleaned_body(self, messaging_service, mock_report, mock_user):
        messaging_service._ensure_access = Mock(return_value=True)
        with pytest.raises(ValidationError) as exc_info:
            messaging_service.send_message(mock_report, mock_user, "   ")
        assert str(exc_info.value) == "Message body cannot be empty."
    
    def test_send_message_recipient_None(self, messaging_service, mock_report, mock_user):
        messaging_service._ensure_access = Mock(return_value=True)
        messaging_service._resolve_recipient = Mock(return_value=None)
        with pytest.raises(ValidationError) as exc_info:
            messaging_service.send_message(mock_report, mock_user, "body")
        assert str(exc_info.value) == "No recipient available for this conversation yet."
    
    def test_send_message_recipient_success(self, messaging_service, mock_report, mock_user):
        messaging_service._ensure_access = Mock(return_value=True)
        mock_recipient = Mock()
        messaging_service._resolve_recipient = Mock(return_value= mock_recipient)
        messaging_service._sender_name = Mock(return_value = "Mario Rossi")
        
        valid_message = "Questo è un messaggio valido    "
        expected_cleaned_message = "Questo è un messaggio valido"

        result = messaging_service.send_message(mock_report, mock_user, valid_message)

        assert result.report_id == mock_report.id
        assert result.sender_id == mock_user.id
        assert result.recipient_id == mock_recipient.id
        assert result.body == expected_cleaned_message

        messaging_service._ensure_access.assert_called_once_with(mock_report, mock_user)
        messaging_service._resolve_recipient.assert_called_once_with(mock_report, mock_user)
        messaging_service._sender_name.assert_called_once_with(mock_user)
        messaging_service.message_repository.add.assert_called_once_with(result)
        messaging_service.session.commit.assert_called_once()
        messaging_service.notification_service.notify_new_message.assert_called_once_with(recipient=mock_recipient,report=mock_report,sender_name="Mario Rossi",body=expected_cleaned_message)

   







