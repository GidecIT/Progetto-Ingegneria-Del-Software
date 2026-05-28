from __future__ import annotations
import pytest

from participium.models.user import User
from participium.models.token import EmailVerificationToken
from participium.core.exceptions import ValidationError, AuthenticationError


class TestAuthControllerRegisterIntegration:
    def test_register_success(self, auth_controller, db_session):
        payload = {
            "username": "auth_register_test",
            "email": "auth_test@example.com",
            "first_name": "Mario",
            "last_name": "Rossi",
            "password": "secure_password_123"
        }

        user, verification_url = auth_controller.register(payload, "http://localhost/verify")

        assert user.id is not None
        assert user.username == "auth_register_test"
        assert verification_url is not None

        actual_token = verification_url.split("/")[-1]

        persisted_token = db_session.query(EmailVerificationToken).filter_by(token=actual_token).first()
        assert persisted_token is not None
        assert persisted_token.user_id == user.id

    def test_register_duplicate_email_fails(self, auth_controller, test_user):
        payload = {
            "username": "another_username",
            "email": test_user.email,
            "first_name": "Luigi",
            "last_name": "Verdi",
            "password": "secure_password_123"
        }

        with pytest.raises(ValidationError):
            auth_controller.register(payload)


class TestAuthControllerVerifyEmailIntegration:
    def test_verify_email_success(self, auth_controller, user_with_relations, db_session):
        token_obj = user_with_relations["token"]
        target_user = user_with_relations["user"]
        
        target_user.is_email_verified = False
        db_session.commit()

        verified_user = auth_controller.verify_email(token_obj.token)

        db_session.refresh(target_user)
        db_session.refresh(token_obj)
        assert verified_user.is_email_verified is True
        assert token_obj.is_used is True

    def test_verify_email_invalid_token_fails(self, auth_controller):
        with pytest.raises(ValidationError):
            auth_controller.verify_email("non-existent-token-value")


class TestAuthControllerLoginIntegration:
    def test_login_success_with_email(self, auth_controller, test_user, db_session):
        from participium.core.security import hash_password
        test_user.password_hash = hash_password("password_di_test")
        test_user.is_active = True
        test_user.is_email_verified = True
        db_session.commit()

        authenticated_user = auth_controller.login(test_user.email, "password_di_test")
        assert authenticated_user.id == test_user.id

    def test_login_success_with_username(self, auth_controller, test_user, db_session):
        from participium.core.security import hash_password
        test_user.password_hash = hash_password("password_di_test")
        test_user.is_active = True
        test_user.is_email_verified = True
        db_session.commit()

        authenticated_user = auth_controller.login(test_user.username, "password_di_test")
        assert authenticated_user.id == test_user.id

    def test_login_invalid_password_fails(self, auth_controller, test_user):
        with pytest.raises(AuthenticationError):
            auth_controller.login(test_user.email, "wrong_password_abc")