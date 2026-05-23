from __future__ import annotations
from unittest.mock import Mock
import pytest

from participium.core.exceptions import AuthorizationError, NotFoundError
from participium.models.enums import NotificationType


@pytest.mark.integration
class TestNotificationServiceIntegration:

    def test_create_notification_success_with_email(
        self, notification_service, test_user, test_report, db_session
    ):
        test_user.email_notifications_enabled = True
        db_session.commit()

        notification = notification_service.create_notification(
            user=test_user,
            notification_type=NotificationType.SYSTEM,
            title="Avviso",
            body="Contenuto della notifica",
            report=test_report
        )
        db_session.flush()

        assert notification is not None
        assert notification.id is not None
        assert notification.user_id == test_user.id
        assert notification.report_id == test_report.id
        
        notification_service.email_gateway.send.assert_called_once_with(
            test_user.email, "Avviso", "Contenuto della notifica"
        )

    def test_create_notification_disables_email_when_flag_is_false(
        self, notification_service, test_user, db_session
    ):
        test_user.email_notifications_enabled = False
        db_session.commit()

        notification = notification_service.create_notification(
            user=test_user,
            notification_type=NotificationType.SYSTEM,
            title="No Email",
            body="Questo utente non vuole email"
        )
        db_session.flush()

        assert notification is not None
        notification_service.email_gateway.send.assert_not_called()

    def test_create_notification_user_none_returns_none(self, notification_service):
        res = notification_service.create_notification(
            user=None,
            notification_type=NotificationType.SYSTEM,
            title="Titolo",
            body="Body"
        )
        assert res is None

    def test_create_notification_swallows_email_exception(
        self, notification_service, test_user, db_session
    ):
        test_user.email_notifications_enabled = True
        db_session.commit()
        
        notification_service.email_gateway.send.side_effect = Exception("SMTP Error")

        notification = notification_service.create_notification(
            user=test_user,
            notification_type=NotificationType.SYSTEM,
            title="Titolo",
            body="Body"
        )
        db_session.flush()
        assert notification is not None

    def test_notify_status_change_handles_duplicates_and_none(
        self, notification_service, test_user, test_report, db_session
    ):
        recipients = [test_user, test_user, None]
        
        notification_service.notify_status_change(
            recipients=recipients,
            report=test_report,
            body="Il report è stato preso in carico"
        )
        db_session.flush()

        notifications = notification_service.list_notifications(test_user.id)
        assert len(notifications) == 1
        assert notifications[0].type == NotificationType.STATUS_CHANGE

    def test_notify_new_message(self, notification_service, test_user, test_report, db_session):
        notification_service.notify_new_message(
            recipient=test_user,
            report=test_report,
            sender_name="Operatore Mario",
            body="Ho aggiornato la pratica"
        )
        db_session.flush()

        notifications = notification_service.list_notifications(test_user.id)
        assert len(notifications) == 1
        assert notifications[0].type == NotificationType.MESSAGE
        assert "Operatore Mario" in notifications[0].body

    def test_unread_message_notifications_counters_and_markdown_as_read(
        self, notification_service, test_user, test_report, store_notification
    ):
        store_notification(test_user.id, type=NotificationType.MESSAGE, report_id=test_report.id, is_read=False)
        store_notification(test_user.id, type=NotificationType.MESSAGE, report_id=test_report.id, is_read=False)
        store_notification(test_user.id, type=NotificationType.SYSTEM, report_id=test_report.id, is_read=False)

        counts = notification_service.count_unread_message_notifications_by_report(test_user.id)
        assert counts == {test_report.id: 2}

        marked_count = notification_service.mark_report_message_notifications_as_read(test_user.id, test_report.id)
        assert marked_count == 2

        counts_after = notification_service.count_unread_message_notifications_by_report(test_user.id)
        assert counts_after == {}

    def test_count_unread_message_notifications_ignores_null_report_id(
        self, notification_service, test_user, store_notification
    ):
        store_notification(test_user.id, type=NotificationType.MESSAGE, report_id=None, is_read=False)

        counts = notification_service.count_unread_message_notifications_by_report(test_user.id)
        assert counts == {}

    def test_mark_report_message_notifications_as_read_with_no_notifications(
        self, notification_service, test_user
    ):
        marked_count = notification_service.mark_report_message_notifications_as_read(
            user_id=test_user.id, 
            report_id=99999
        )
        assert marked_count == 0

    def test_get_user_notification_success_and_failures(
        self, notification_service, test_user, other_user, store_notification
    ):
        notification = store_notification(test_user.id, title="Test")

        fetched = notification_service.get_user_notification(test_user.id, notification.id)
        assert fetched.id == notification.id

        with pytest.raises(NotFoundError):
            notification_service.get_user_notification(test_user.id, 99999)

        with pytest.raises(AuthorizationError):
            notification_service.get_user_notification(other_user.id, notification.id)

    def test_mark_as_read(self, notification_service, test_user, store_notification):
        notification = store_notification(test_user.id, is_read=False)
        
        updated = notification_service.mark_as_read(notification)
        assert updated.is_read is True