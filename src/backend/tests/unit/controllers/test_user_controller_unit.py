from __future__ import annotations
import pytest
from unittest.mock import Mock


class TestUserControllerProfileAndAccount:
    def test_update_profile_delegates_all_arguments(self, user_controller, mock_user, mock_file):
        user_controller.user_service.update_profile = Mock(return_value=mock_user)

        result = user_controller.update_profile(
            user=mock_user,
            username="new_username",
            first_name="Giovanni",
            last_name="Verdi",
            email_notifications_enabled=False,
            profile_picture=mock_file,
        )

        assert result == mock_user
        user_controller.user_service.update_profile.assert_called_once_with(
            user=mock_user,
            username="new_username",
            first_name="Giovanni",
            last_name="Verdi",
            email_notifications_enabled=False,
            profile_picture=mock_file,
        )

    def test_update_profile_with_defaults(self, user_controller, mock_user):
        user_controller.user_service.update_profile = Mock(return_value=mock_user)

        result = user_controller.update_profile(user=mock_user)

        assert result == mock_user
        user_controller.user_service.update_profile.assert_called_once_with(
            user=mock_user,
            username=None,
            first_name=None,
            last_name=None,
            email_notifications_enabled=None,
            profile_picture=None,
        )

    def test_delete_account_delegates_to_service(self, user_controller, mock_user):
        user_controller.user_service.delete_account = Mock()

        user_controller.delete_account(mock_user)

        user_controller.user_service.delete_account.assert_called_once_with(mock_user)


class TestUserControllerAdminActions:
    def test_list_users_delegates_to_service(self, user_controller, mock_user):
        mock_list = [mock_user]
        user_controller.user_service.list_users = Mock(return_value=mock_list)

        result = user_controller.list_users()

        assert result == mock_list
        user_controller.user_service.list_users.assert_called_once()

    def test_create_user_delegates_payload(self, user_controller, mock_user):
        payload = {"email": "test@example.com", "role": "CITIZEN"}
        user_controller.user_service.create_user = Mock(return_value=mock_user)

        result = user_controller.create_user(payload)

        assert result == mock_user
        user_controller.user_service.create_user.assert_called_once_with(payload)

    def test_update_user_delegates_id_and_payload(self, user_controller, mock_user):
        payload = {"is_active": False}
        user_controller.user_service.update_user = Mock(return_value=mock_user)

        result = user_controller.update_user(user_id=42, payload=payload)

        assert result == mock_user
        user_controller.user_service.update_user.assert_called_once_with(42, payload)


class TestUserControllerNotifications:
    def test_list_notifications_delegates_to_service(self, user_controller, mock_notification):
        mock_list = [mock_notification]
        user_controller.notification_service.list_notifications = Mock(return_value=mock_list)

        result = user_controller.list_notifications(user_id=1)

        assert result == mock_list
        user_controller.notification_service.list_notifications.assert_called_once_with(1)

    def test_get_notification_for_user_delegates_to_service(self, user_controller, mock_notification):
        user_controller.notification_service.get_user_notification = Mock(return_value=mock_notification)

        result = user_controller.get_notification_for_user(user_id=1, notification_id=10)

        assert result == mock_notification
        user_controller.notification_service.get_user_notification.assert_called_once_with(1, 10)

    def test_mark_notification_as_read_delegates_to_service(self, user_controller, mock_notification):
        user_controller.notification_service.mark_as_read = Mock(return_value=mock_notification)

        result = user_controller.mark_notification_as_read(mock_notification)

        assert result == mock_notification
        user_controller.notification_service.mark_as_read.assert_called_once_with(mock_notification)


class TestUserControllerErrorPropagation:
    def test_user_service_error_propagates(self, user_controller):
        user_controller.user_service.list_users = Mock(side_effect=RuntimeError("DB Error"))

        with pytest.raises(RuntimeError) as exc_info:
            user_controller.list_users()

        assert str(exc_info.value) == "DB Error"

    def test_notification_service_error_propagates(self, user_controller):
        user_controller.notification_service.list_notifications = Mock(side_effect=ValueError("Not found"))

        with pytest.raises(ValueError) as exc_info:
            user_controller.list_notifications(user_id=99)

        assert str(exc_info.value) == "Not found"