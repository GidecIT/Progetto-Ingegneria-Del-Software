from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock

import pytest

from participium.core.exceptions import AuthorizationError, NotFoundError
from participium.models.enums import NotificationType

class TestCreateNotification:
    def test_create_notification_user_None(self, notification_service):
        result = notification_service.create_notification(None, NotificationType.MESSAGE , "Test", "Body", None)
        assert result is None
    def test_create_notification_success_no_email(self, notification_service, mock_user):
        mock_user.email_notifications_enabled = False
        
        result = notification_service.create_notification(user=mock_user,notification_type=NotificationType.MESSAGE,title="Test",body="Body")
        
        assert result is not None
        assert result.user_id == mock_user.id
        notification_service.notification_repository.add.assert_called_once()
        notification_service.email_gateway.send.assert_not_called()

    def test_create_notification_success_with_email(self, notification_service, mock_user):
        mock_user.email_notifications_enabled = True
        
        result = notification_service.create_notification(mock_user, NotificationType.MESSAGE, "Titolo", "Body")
        
        assert result is not None
        notification_service.email_gateway.send.assert_called_once_with(mock_user.email, "Titolo", "Body")

    def test_create_notification_with_report(self, notification_service, mock_user, mock_report):
        result = notification_service.create_notification(mock_user, NotificationType.MESSAGE, "T", "B", report=mock_report)
        
        assert result.report_id == mock_report.id
        notification_service.notification_repository.add.assert_called_once()

    def test_create_notification_email_failure_does_not_crash(self, notification_service, mock_user):
        mock_user.email_notifications_enabled = True
        notification_service.email_gateway.send.side_effect = Exception("Error")
        
        result = notification_service.create_notification(mock_user, NotificationType.MESSAGE, "T", "B")
    
        assert result is not None
        notification_service.notification_repository.add.assert_called_once()

class TestNotifyStatusChange:
    def test_notify_status_change_empty_list(self, notification_service, mock_report):
        notification_service.create_notification = Mock()
        
        notification_service.notify_status_change([], mock_report, "Body")
        
        notification_service.create_notification.assert_not_called()

    def test_notify_status_change_success(self, notification_service, mock_user, mock_report):
        recipients = [mock_user]
        body = "Test"
        notification_service.create_notification = Mock()

        notification_service.notify_status_change(recipients, mock_report, body)
        
        notification_service.create_notification.assert_called_once_with(mock_user,NotificationType.STATUS_CHANGE,f"Report #{mock_report.id} status updated",body,report=mock_report)

    def test_notify_status_change_duplicates_and_none(self, notification_service, mock_user, mock_report):
        user2 = Mock()
        user2.id = 2
        recipients = [mock_user, None, mock_user, user2]
        
        notification_service.create_notification = Mock()
        
        notification_service.notify_status_change(recipients, mock_report, "Test")
        
        assert notification_service.create_notification.call_count == 2
        
        notification_service.create_notification.assert_any_call(mock_user,NotificationType.STATUS_CHANGE,f"Report #{mock_report.id} status updated","Test",report=mock_report)
        notification_service.create_notification.assert_any_call(user2,NotificationType.STATUS_CHANGE,f"Report #{mock_report.id} status updated","Test",report=mock_report)

class TestNotifyNewMessage:
    def test_notify_new_message_success(self, notification_service, mock_user, mock_report):
        notification_service.create_notification = Mock()
        body = "Body"
        sender_name = "Sender Name"
        notification_service.notify_new_message(mock_user, mock_report, sender_name, body)
        notification_service.create_notification.assert_called_once_with(mock_user, NotificationType.MESSAGE, f"New message on report #{mock_report.id}", f"{sender_name}: {body}", report=mock_report)

class TestListNotification:
    def test_list_notification_success(self, notification_service, mock_notification, mock_user):
        notification_service.notification_repository.list_for_user = Mock(return_value=mock_notification)
        result = notification_service.list_notifications(mock_user.id)
        assert result == mock_notification
        notification_service.notification_repository.list_for_user.assert_called_once_with(mock_user.id)

class TestCountUnreadMessageNotificationsByReport:
    def test_count_unread_message_notifications_by_report_empty(self, notification_service):
        notification_service.notification_repository.list_unread_message_notifications = Mock(return_value=[])
        
        result = notification_service.count_unread_message_notifications_by_report(1)
        assert result == {}
        notification_service.notification_repository.list_unread_message_notifications.assert_called_once_with(user_id=1)

    def test_count_unread_message_notifications_by_report_success(self, notification_service):
        n1 = Mock(report_id=10)
        n2 = Mock(report_id=10)
        n3 = Mock(report_id=20)
        n4 = Mock(report_id=None)
        notifications = [n1, n2, n3, n4]
        
        notification_service.notification_repository.list_unread_message_notifications = Mock(return_value=notifications)
        
        result = notification_service.count_unread_message_notifications_by_report(1)
        
        expected = {10: 2, 20: 1}
        assert result == expected
        notification_service.notification_repository.list_unread_message_notifications.assert_called_once_with(user_id=1)

class TestMarkReportMessageNotificationsAsRead:
    def test_success(self, notification_service):
        n1 = Mock()
        n2 = Mock()
        notifications = [n1, n2]
        notification_service.notification_repository.list_unread_message_notifications = Mock(return_value=notifications)
        notification_service.session = Mock()

        count = notification_service.mark_report_message_notifications_as_read(1, 100)

        assert count == 2
        assert n1.is_read is True
        assert n2.is_read is True
        notification_service.session.commit.assert_called_once()
        notification_service.notification_repository.list_unread_message_notifications.assert_called_once_with(user_id=1, report_id=100)

    def test_empty(self, notification_service):
        notification_service.notification_repository.list_unread_message_notifications = Mock(return_value=[])
        notification_service.session = Mock()

        count = notification_service.mark_report_message_notifications_as_read(1, 100)

        assert count == 0
        notification_service.session.commit.assert_not_called()

class TestGetUserNotification:
    def test_success(self, notification_service, mock_notification, mock_user):
        notification_service.notification_repository.get_by_id = Mock(return_value=mock_notification)

        result = notification_service.get_user_notification(mock_user.id, mock_notification.id)

        assert result == mock_notification
        notification_service.notification_repository.get_by_id.assert_called_once_with(mock_notification.id)

    def test_not_found(self, notification_service, mock_user):
        notification_service.notification_repository.get_by_id = Mock(return_value=None)

        with pytest.raises(NotFoundError):
            notification_service.get_user_notification(mock_user.id, 99)

    def test_unauthorized(self, notification_service, mock_user):
        unauthorized_notification = Mock()
        unauthorized_notification.user_id = 999 
        
        notification_service.notification_repository.get_by_id = Mock(return_value=unauthorized_notification)

        with pytest.raises(AuthorizationError):
            notification_service.get_user_notification(mock_user.id, unauthorized_notification.id)

class TestMarkAsRead:
    def test_success(self, notification_service):
        mock_notif = Mock(is_read=False)
        notification_service.session = Mock()

        result = notification_service.mark_as_read(mock_notif)

        assert result.is_read is True
        notification_service.session.commit.assert_called_once()
