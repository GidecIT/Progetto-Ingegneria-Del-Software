from __future__ import annotations
from unittest.mock import Mock

import pytest

from participium.models.enums import NotificationType
from participium.models.notification import Notification


class TestNotificationRepositoryWriteAndGet:
    def test_add(self, notification_repository, mock_session):
        mock_notification = Mock(spec=Notification)
        result = notification_repository.add(mock_notification)
        assert result == mock_notification
        mock_session.add.assert_called_once_with(mock_notification)

    def test_get_by_id_found(self, notification_repository, mock_session):
        mock_notification = Mock(spec=Notification)
        mock_session.get.return_value = mock_notification
        result = notification_repository.get_by_id(1)
        assert result == mock_notification
        mock_session.get.assert_called_once_with(Notification, 1)

    def test_get_by_id_not_found(self, notification_repository, mock_session):
        mock_session.get.return_value = None
        result = notification_repository.get_by_id(999)
        assert result is None
        mock_session.get.assert_called_once_with(Notification, 999)


class TestNotificationRepositoryQueriesAndBranches:
    def test_list_for_user(self, notification_repository, mock_session):
        mock_session.scalars.return_value = []

        result = notification_repository.list_for_user(user_id=1)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_unread_message_notifications_branch_report_id_none(self, notification_repository, mock_session):
        mock_session.scalars.return_value = []

        result = notification_repository.list_unread_message_notifications(user_id=1, report_id=None)
        assert result == []
        mock_session.scalars.assert_called_once()

    def test_list_unread_message_notifications_branch_report_id_not_none(self, notification_repository, mock_session):
        mock_session.scalars.return_value = []

        result = notification_repository.list_unread_message_notifications(user_id=1, report_id=100)
        assert result == []
        mock_session.scalars.assert_called_once()


class TestNotificationRepositoryDelete:
    def test_delete_for_user_empty(self, notification_repository):
        notification_repository.list_for_user = Mock(return_value=[])
        notification_repository.delete_for_user(user_id=1)
        notification_repository.list_for_user.assert_called_once_with(1)

    def test_delete_for_user_with_items(self, notification_repository, mock_session):
        mock_notif_1 = Mock(spec=Notification)
        mock_notif_2 = Mock(spec=Notification)
        notification_repository.list_for_user = Mock(return_value=[mock_notif_1, mock_notif_2])

        notification_repository.delete_for_user(user_id=1)

        notification_repository.list_for_user.assert_called_once_with(1)
        assert mock_session.delete.call_count == 2
        mock_session.delete.assert_any_call(mock_notif_1)
        mock_session.delete.assert_any_call(mock_notif_2)