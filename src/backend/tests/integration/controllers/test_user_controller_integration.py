from __future__ import annotations
import pytest

from participium.models.enums import Role
from participium.models.user import User


class TestUserControllerProfileAndAccountIntegration:
    def test_update_profile_integration_success(self, user_controller, test_user, mock_file, db_session):
        uploaded_file = mock_file(filename="avatar.png", content=b"image_bytes")

        updated_user = user_controller.update_profile(
            user=test_user,
            username="updated_user_123",
            first_name="NuovoNome",
            last_name="NuovoCognome",
            email_notifications_enabled=False,
            profile_picture=uploaded_file,
        )

        db_session.refresh(test_user)
        assert updated_user.username == "updated_user_123"
        assert updated_user.first_name == "NuovoNome"
        assert updated_user.last_name == "NuovoCognome"
        assert updated_user.email_notifications_enabled is False
        assert updated_user.profile_picture_path is not None

    def test_update_profile_with_defaults_keeps_existing_values(self, user_controller, test_user, db_session):
        original_username = test_user.username
        original_first_name = test_user.first_name

        updated_user = user_controller.update_profile(user=test_user)

        db_session.refresh(test_user)
        assert updated_user.username == original_username
        assert updated_user.first_name == original_first_name

    def test_delete_account_removes_user_and_cascades_relations(self, user_controller, user_with_relations, db_session):
        target_user = user_with_relations["user"]
        user_id = target_user.id

        user_controller.delete_account(target_user)

        deleted_user = db_session.query(User).get(user_id)
        assert deleted_user is None


class TestUserControllerAdminActionsIntegration:
    def test_list_users_integration(self, user_controller, test_user, db_session):
        users = user_controller.list_users()
        user_ids = [u.id for u in users]
        assert test_user.id in user_ids

    def test_create_user_integration(self, user_controller, db_session):
        payload = {
            "username": "new_integration_user",
            "email": "integration@example.com",
            "first_name": "Mario",
            "last_name": "Rossi",
            "role": Role.CITIZEN,
            "password": "secure_password_123"
        }

        created_user = user_controller.create_user(payload)

        persisted_user = db_session.query(User).get(created_user.id)
        assert persisted_user is not None
        assert persisted_user.username == "new_integration_user"
        assert persisted_user.email == "integration@example.com"

    def test_update_user_integration(self, user_controller, test_user, test_category, db_session):
        payload = {"is_active": False, "role": Role.OPERATOR, "category_id": test_category.id}

        updated_user = user_controller.update_user(test_user.id, payload)

        db_session.refresh(test_user)
        assert updated_user.is_active is False
        assert updated_user.role == Role.OPERATOR
        assert updated_user.category_id == test_category.id


class TestUserControllerNotificationsIntegration:
    def test_list_notifications_integration(self, user_controller, store_notification, test_user):
        stored_notif = store_notification(user_id=test_user.id, title="Test Alert")

        notifications = user_controller.list_notifications(test_user.id)
        notif_ids = [n.id for n in notifications]
        assert stored_notif.id in notif_ids

    def test_get_notification_for_user_integration(self, user_controller, store_notification, test_user):
        stored_notif = store_notification(user_id=test_user.id, title="Direct Alert")

        notification = user_controller.get_notification_for_user(test_user.id, stored_notif.id)
        assert notification.id == stored_notif.id
        assert notification.title == "Direct Alert"

    def test_mark_notification_as_read_integration(self, user_controller, store_notification, test_user, db_session):
        stored_notif = store_notification(user_id=test_user.id, is_read=False)

        updated_notif = user_controller.mark_notification_as_read(stored_notif)

        db_session.refresh(stored_notif)
        assert updated_notif.is_read is True
        assert stored_notif.is_read is True