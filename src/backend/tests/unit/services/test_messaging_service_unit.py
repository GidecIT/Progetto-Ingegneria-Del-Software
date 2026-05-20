from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest

from participium.models.enums import Role
from participium.core.exceptions import AuthorizationError, ValidationError

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
    
    def test_can_access_thread_citizen_is_reporter(self, messaging_service, mock_report, mock_user):
        mock_report.reporter_id = mock_user.id  
        result = messaging_service.can_access_thread(mock_report, mock_user)
        assert result == True

    def test_can_access_thread_citizen_not_reporter(self, messaging_service, mock_report, mock_user):
        result = messaging_service.can_access_thread(mock_report, mock_user)
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
        messaging_service.message_repository.add.assert_not_called()
        messaging_service.session.commit.assert_not_called()
        messaging_service.notification_service.notify_new_message.assert_not_called()
    
    def test_send_message_recipient_None(self, messaging_service, mock_report, mock_user):
        messaging_service._ensure_access = Mock(return_value=True)
        messaging_service._resolve_recipient = Mock(return_value=None)
        with pytest.raises(ValidationError) as exc_info:
            messaging_service.send_message(mock_report, mock_user, "body")
        assert str(exc_info.value) == "No recipient available for this conversation yet."
        messaging_service.message_repository.add.assert_not_called()
        messaging_service.session.commit.assert_not_called()
        messaging_service.notification_service.notify_new_message.assert_not_called()
    
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
        messaging_service.notification_service.notify_new_message.assert_called_once_with(recipient=mock_recipient,report=mock_report,sender_name="Mario Rossi",body=expected_cleaned_message)
        messaging_service.session.commit.assert_called_once()
class TestEnsureAccess:
    def test_ensure_access_AuthorizationError(self, mock_report, mock_user, messaging_service):
        messaging_service.can_access_thread = Mock(return_value=False)
        with pytest.raises(AuthorizationError) as exc_info:
            messaging_service._ensure_access(mock_report, mock_user)
        assert str(exc_info.value) == "You do not have access to the message thread for this report."
    
    def test_ensure_access_success(self, mock_report, mock_user, messaging_service):
        messaging_service.can_access_thread = Mock(return_value=True)
        result = messaging_service._ensure_access(mock_report, mock_user)
        assert result is None
        messaging_service.can_access_thread.assert_called_once_with(mock_report, mock_user)


class TestResolveRecipient:
    def test_resolve_recipient_admin(self, mock_report, mock_admin, messaging_service):
        result = messaging_service._resolve_recipient(mock_report, mock_admin)
        assert result == mock_report.reporter

    def test_resolve_recipient_messages_0_iterations(self, mock_report, mock_user, messaging_service):
        """0 iterazioni sia per il primo che per il secondo for"""
        messaging_service.message_repository.list_for_report.return_value = []
        mock_report.status_history = []  

        result = messaging_service._resolve_recipient(mock_report, mock_user)
        assert result is None

    def test_resolve_recipient_messages_1_iteration_found(self, mock_report, mock_user, messaging_service):
        """1 iterazione sui messaggi inviato da operator"""
        mock_sender = Mock()
        mock_sender.role = Role.OPERATOR
        mock_message = Mock(sender=mock_sender)
        
        messaging_service.message_repository.list_for_report.return_value = [mock_message]

        result = messaging_service._resolve_recipient(mock_report, mock_user)
        assert result == mock_sender

    def test_resolve_recipient_messages_2_iterations_returns_last_valid(self, mock_report, mock_user, messaging_service):
        """2 iterazioni sui messaggi: restituisce l'ultimo """
        mock_sender_admin = Mock()
        mock_sender_admin.role = Role.ADMIN
        msg_old = Mock(sender=mock_sender_admin)

        mock_sender_citizen = Mock()
        mock_sender_citizen.role = Role.CITIZEN
        msg_recent = Mock(sender=mock_sender_citizen)

        messaging_service.message_repository.list_for_report.return_value = [msg_old, msg_recent]
        result = messaging_service._resolve_recipient(mock_report, mock_user)
        assert result == mock_sender_admin

    def test_resolve_recipient_status_history_1_iteration_found(self, mock_report, mock_user, messaging_service):
        """status_history ha 1 elemento"""
        messaging_service.message_repository.list_for_report.return_value = []
        mock_changer = Mock()
        mock_changer.role = Role.ADMIN
        status_event = Mock(changed_by=mock_changer)
        
        mock_report.status_history = [status_event]

        result = messaging_service._resolve_recipient(mock_report, mock_user)
        assert result == mock_changer

    def test_resolve_recipient_status_history_2_iterations_returns_last_valid(self, mock_report, mock_user, messaging_service):
        messaging_service.message_repository.list_for_report.return_value = []

        mock_changer_operator = Mock()
        mock_changer_operator.role = Role.OPERATOR
        event_old = Mock(changed_by=mock_changer_operator)
        mock_changer_citizen = Mock()
        mock_changer_citizen.role = Role.CITIZEN
        event_recent = Mock(changed_by=mock_changer_citizen)

        mock_report.status_history = [event_old, event_recent]

        result = messaging_service._resolve_recipient(mock_report, mock_user)
        assert result == mock_changer_operator

class TestSenderName:
    def test_sender_name_with_first_and_last_name(self, messaging_service, mock_user):
        result = messaging_service._sender_name(mock_user)
        assert result == "Mario Rossi"

    def test_sender_name_empty_fallback_to_username(self, messaging_service, mock_user):
        mock_user.first_name = "   "
        mock_user.last_name = ""

        result = messaging_service._sender_name(mock_user)
        assert result == mock_user.username
        

   





