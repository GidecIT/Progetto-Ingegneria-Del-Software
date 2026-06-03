from __future__ import annotations
from datetime import timedelta
from unittest.mock import Mock, ANY

import pytest

from participium.core.exceptions import ValidationError, AuthenticationError
from participium.models.user import User
from participium.core.utils import utcnow
from participium.core.security import hash_password


class TestRegisterUser:
    @pytest.mark.parametrize("missing_field", ["username", "first_name", "last_name", "email", "password"])
    def test_register_rejects_missing_required_fields(self, auth_service, missing_field):
        payload = {"username": "j", "first_name": "J", "last_name": "D", "email": "j@ex.com", "password": "p"}
        payload[missing_field] = ""
        with pytest.raises(ValidationError):
            auth_service.register_user(payload)

    def test_register_rejects_duplicate_username(self, auth_service):
        auth_service.user_repository.get_by_username.return_value = Mock(spec=User)
        with pytest.raises(ValidationError):
            auth_service.register_user(
                {"username": "u", "first_name": "J", "last_name": "D", "email": "j@ex.com", "password": "p"})

    def test_register_rejects_duplicate_email(self, auth_service):
        auth_service.user_repository.get_by_username.return_value = None
        auth_service.user_repository.get_by_email.return_value = Mock(spec=User)
        with pytest.raises(ValidationError):
            auth_service.register_user(
                {"username": "u", "first_name": "J", "last_name": "D", "email": "j@ex.com", "password": "p"})

    def test_register_success_with_verification_url(self, auth_service):
        auth_service.user_repository.get_by_username.return_value = None
        auth_service.user_repository.get_by_email.return_value = None

        payload = {"username": "user", "first_name": "J", "last_name": "D", "email": "j@ex.com", "password": "p"}

        user, url = auth_service.register_user(payload, verification_base_url="https://ex.com/verify")
        
        assert user.username == "user"
        assert url.startswith("https://ex.com/verify/")
        auth_service.email_gateway.send.assert_called_once_with(
            recipient=user.email,
            subject="Verify your Participium account",
            body=ANY
        )
        auth_service.session.commit.assert_called_once()

    def test_register_success_without_verification_url(self, auth_service):
        auth_service.user_repository.get_by_username.return_value = None
        auth_service.user_repository.get_by_email.return_value = None

        payload = {"username": "user", "first_name": "J", "last_name": "D", "email": "j@ex.com", "password": "p"}

        user, url = auth_service.register_user(payload, verification_base_url=None)
        
        assert user.username == "user"
        assert url is None
        auth_service.email_gateway.send.assert_not_called()
        auth_service.session.commit.assert_called_once()


class TestVerifyEmail:
    def test_verify_email_invalid_token(self, auth_service):
        auth_service.token_repository.get_by_token.return_value = None
        with pytest.raises(ValidationError):
            auth_service.verify_email("invalid")

    def test_verify_email_expired_token(self, auth_service):
        mock_token = Mock()
        mock_token.is_used = False
        mock_token.expires_at = utcnow() - timedelta(hours=1)
        auth_service.token_repository.get_by_token.return_value = mock_token
        with pytest.raises(ValidationError):
            auth_service.verify_email("expired")

    def test_verify_email_success(self, auth_service):
        mock_user = Mock(spec=User)
        mock_token = Mock(is_used=False, expires_at=utcnow() + timedelta(hours=1), user=mock_user)
        auth_service.token_repository.get_by_token.return_value = mock_token

        result = auth_service.verify_email("good")
        assert mock_token.is_used is True
        auth_service.session.commit.assert_called_once()


class TestAuthenticate:
    def test_authenticate_invalid_credentials(self, auth_service):
        auth_service.user_repository.get_by_username_or_email.return_value = None
        with pytest.raises(AuthenticationError):
            auth_service.authenticate("ghost", "pass")

    def test_authenticate_unverified_email(self, auth_service):
        mock_user = Mock(is_active=True, is_email_verified=False, password_hash=hash_password("pass"))
        auth_service.user_repository.get_by_username_or_email.return_value = mock_user
        with pytest.raises(AuthenticationError):
            auth_service.authenticate("user", "pass")

    def test_authenticate_success(self, auth_service):
        mock_user = Mock(is_active=True, is_email_verified=True, password_hash=hash_password("pass"))
        auth_service.user_repository.get_by_username_or_email.return_value = mock_user

        assert auth_service.authenticate("user", "pass") == mock_user