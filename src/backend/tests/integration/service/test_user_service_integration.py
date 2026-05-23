from __future__ import annotations
import pytest
from unittest.mock import Mock

from participium.models.enums import Role, ReportStatus
from participium.models.user import User
from participium.models.message import Message
from participium.models.token import EmailVerificationToken
from participium.core.exceptions import ValidationError, NotFoundError


@pytest.mark.integration
class TestUpdateProfile:

    def test_update_profile_success(self, user_service, test_user):
        updated = user_service.update_profile(
            user=test_user,
            username="new_username",
            first_name="NewName",
            last_name="  NewLastName  ",
            email_notifications_enabled=0
        )
        assert updated.username == "new_username"
        assert updated.last_name == "NewLastName"
        assert updated.email_notifications_enabled is False

    def test_update_profile_picture(self, user_service, test_user):
        mock_file = Mock()
        mock_file.filename = "avatar.png"
        user_service.storage_service.save = Mock(return_value="path/to/avatar.png")

        updated = user_service.update_profile(user=test_user, profile_picture=mock_file)
        assert updated.profile_picture_path == "path/to/avatar.png"
        user_service.storage_service.save.assert_called_once_with(mock_file)

    def test_update_profile_duplicate_username_raises_error(self, user_service, test_user, other_user):
        with pytest.raises(ValidationError, match="Username already in use."):
            user_service.update_profile(user=test_user, username=other_user.username)


@pytest.mark.integration
class TestDeleteAccount:

    def test_delete_account_cascades_and_nullifies_relations(
        self, user_service, db_session, user_with_relations
    ):
        target_user = user_with_relations["user"]
        report = user_with_relations["report"]
        message = user_with_relations["message"]
        token = user_with_relations["token"]

        user_service.delete_account(target_user)
        db_session.commit()

        assert db_session.get(User, target_user.id) is None

        db_session.refresh(report)
        assert report.reporter_id is None
        assert report.is_anonymous is True

        db_session.refresh(message)
        assert message.sender_id is None
        assert message.recipient_id is None

        assert db_session.get(EmailVerificationToken, token.id) is None

    def test_delete_account_nullifies_message_sender_and_recipient(
        self, user_service, db_session, user_with_relations, other_user
    ):
        target_user = user_with_relations["user"]
        report = user_with_relations["report"]
        msg_both = user_with_relations["message"]

        msg_sender_only = Message(
            report_id=report.id,
            sender_id=target_user.id,
            recipient_id=other_user.id,
            body="Inviato da me"
        )

        msg_recipient_only = Message(
            report_id=report.id,
            sender_id=other_user.id,
            recipient_id=target_user.id,
            body="Ricevuto da me"
        )

        db_session.add_all([msg_sender_only, msg_recipient_only])
        db_session.commit()

        user_service.delete_account(target_user)
        db_session.commit()

        db_session.refresh(msg_both)
        assert msg_both.sender_id is None
        assert msg_both.recipient_id is None

        db_session.refresh(msg_sender_only)
        assert msg_sender_only.sender_id is None
        assert msg_sender_only.recipient_id == other_user.id

        db_session.refresh(msg_recipient_only)
        assert msg_recipient_only.sender_id == other_user.id
        assert msg_recipient_only.recipient_id is None


@pytest.mark.integration
class TestListAndGetUser:

    def test_list_users_returns_all_records(self, user_service, test_user, other_user):
        users = user_service.list_users()
        assert len(users) >= 2

    def test_get_user_success(self, user_service, test_user):
        user = user_service.get_user(test_user.id)
        assert user.id == test_user.id

    def test_get_user_not_found_raises_error(self, user_service):
        with pytest.raises(NotFoundError, match="User not found."):
            user_service.get_user(99999)


@pytest.mark.integration
class TestCreateUser:

    def test_create_standard_user_success(self, user_service):
        payload = {
            "username": "fresh_clean_user",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "mario@example.com",
            "password": "SecretPassword123",
            "role": Role.CITIZEN.value
        }
        user = user_service.create_user(payload)
        assert user.username == "fresh_clean_user"

    def test_create_user_missing_required_fields_raises_error(self, user_service):
        payload = {"username": "incomplete"}
        with pytest.raises(ValidationError, match="Missing required fields:"):
            user_service.create_user(payload)

    def test_create_user_duplicate_username_raises_error(self, user_service, test_user):
        payload = {
            "username": test_user.username,
            "first_name": "X", "last_name": "Y",
            "email": "unique@ex.com", "password": "P",
            "role": Role.CITIZEN.value
        }
        with pytest.raises(ValidationError, match="Username already in use."):
            user_service.create_user(payload)

    def test_create_user_duplicate_email_raises_error(self, user_service, test_user):
        payload = {
            "username": "unique_username",
            "first_name": "X", "last_name": "Y",
            "email": test_user.email, "password": "P",
            "role": Role.CITIZEN.value
        }
        with pytest.raises(ValidationError, match="Email already in use."):
            user_service.create_user(payload)

    def test_create_user_invalid_role_raises_error(self, user_service):
        payload = {
            "username": "new_user", "first_name": "X", "last_name": "Y",
            "email": "new@ex.com", "password": "P", "role": "INVALID_ROLE"
        }
        with pytest.raises(ValidationError, match="Invalid user role."):
            user_service.create_user(payload)

    def test_create_operator_missing_category_raises_error(self, user_service):
        payload = {
            "username": "op_user", "first_name": "X", "last_name": "Y",
            "email": "op@ex.com", "password": "P", "role": Role.OPERATOR.value
        }
        with pytest.raises(ValidationError, match="Operator category is required."):
            user_service.create_user(payload)

    def test_create_operator_invalid_category_id_format_raises_error(self, user_service):
        payload = {
            "username": "op_user", "first_name": "X", "last_name": "Y",
            "email": "op@ex.com", "password": "P", "role": Role.OPERATOR.value,
            "category_id": "not_an_int"
        }
        with pytest.raises(ValidationError, match="A valid active category is required for operators."):
            user_service.create_user(payload)

    def test_create_operator_non_existent_category_raises_error(self, user_service):
        payload = {
            "username": "op_user", "first_name": "X", "last_name": "Y",
            "email": "op@ex.com", "password": "P", "role": Role.OPERATOR.value,
            "category_id": 99999
        }
        with pytest.raises(ValidationError, match="A valid active category is required for operators."):
            user_service.create_user(payload)

    def test_create_operator_inactive_category_raises_error(self, user_service, db_session, test_category):
        test_category.is_active = False
        db_session.commit()

        payload = {
            "username": "op_user", "first_name": "X", "last_name": "Y",
            "email": "op@ex.com", "password": "P", "role": Role.OPERATOR.value,
            "category_id": test_category.id
        }
        with pytest.raises(ValidationError, match="A valid active category is required for operators."):
            user_service.create_user(payload)


@pytest.mark.integration
class TestUpdateUser:

    def test_update_user_fields_success(self, user_service, test_user):
        payload = {
            "username": "updated_via_admin",
            "is_active": 0,
            "email_notifications_enabled": 1
        }
        updated = user_service.update_user(test_user.id, payload)
        assert updated.username == "updated_via_admin"
        assert updated.is_active is False
        assert updated.email_notifications_enabled is True

    def test_update_user_duplicate_username_raises_error(self, user_service, test_user, other_user):
        payload = {"username": other_user.username}
        with pytest.raises(ValidationError, match="Username already in use."):
            user_service.update_user(test_user.id, payload)

    def test_update_user_duplicate_email_raises_error(self, user_service, test_user, other_user):
        payload = {"email": other_user.email}
        with pytest.raises(ValidationError, match="Email already in use."):
            user_service.update_user(test_user.id, payload)

    def test_update_user_role_and_category_resolution(self, user_service, test_user, test_category):
        payload = {
            "role": Role.OPERATOR.value,
            "category_id": test_category.id
        }
        updated = user_service.update_user(test_user.id, payload)
        assert updated.role == Role.OPERATOR
        assert updated.category_id == test_category.id

        payload_back = {"role": Role.CITIZEN.value}
        updated_back = user_service.update_user(test_user.id, payload_back)
        assert updated_back.role == Role.CITIZEN
        assert updated_back.category_id is None