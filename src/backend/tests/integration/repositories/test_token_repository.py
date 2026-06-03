import pytest
from datetime import timedelta
from unittest.mock import Mock

from participium.models.token import EmailVerificationToken
from participium.repositories.token_repository import TokenRepository
from participium.models.user import User
from participium.repositories.user_repository import UserRepository
from participium.core.exceptions import AuthenticationError, ValidationError
from participium.core.utils import utcnow
from participium.services.auth_service import AuthService
from participium.controllers.auth_controller import AuthController

pytestmark = pytest.mark.integration




def test_add_token(db_session, token_repository, test_user, make_token):
    added = token_repository.add(make_token(test_user.id, token="Nuovo-token"))
    db_session.commit()

    assert added.id is not None
    assert added.token == "Nuovo-token"
    assert added.is_used is False
    assert added.user_id == test_user.id


def test_get_by_token_found(db_session, token_repository, test_user, make_token):
    db_session.add(make_token(test_user.id, token="token2"))
    db_session.commit()

    result = token_repository.get_by_token("token2")

    assert result is not None
    assert result.token == "token2"
    assert result.user_id == test_user.id


def test_get_by_token_not_found(token_repository):
    assert token_repository.get_by_token("inesistente") is None






def test_list_for_user_empty(token_repository, test_user, make_token):
    assert token_repository.list_for_user(test_user.id) == []


def test_list_for_user_returns_all_tokens(db_session, token_repository, test_user, make_token):
    db_session.add_all([
        make_token(test_user.id, token="tok-1"),
        make_token(test_user.id, token="tok-2", is_used=True),
    ])
    db_session.commit()

    results = token_repository.list_for_user(test_user.id)

    assert len(results) == 2
    assert all(t.user_id == test_user.id for t in results)


def test_list_for_user_isolation(db_session, token_repository, test_user, other_user, make_token):
    db_session.add_all([
        make_token(test_user.id,  token="token_mio"),
        make_token(other_user.id, token="tokeno_altro"),
    ])
    db_session.commit()

    results = token_repository.list_for_user(test_user.id)

    assert len(results) == 1
    assert results[0].token == "token_mio"


def test_auth_controller_and_service_full_flow(db_session, token_repository, test_user):
    """
    copre AuthController e AuthService,
    sfruttando le relazioni native di SQLAlchemy (token.user).
    """
    user_repo = UserRepository(db_session)
    mock_email_gateway = Mock()
    auth_service = AuthService(db_session, user_repo, token_repository, mock_email_gateway)

    auth_controller = AuthController(auth_service)

    test_user.is_email_verified = False
    db_session.commit()

    payload = {
        "username": "nuovo_utente_controller",
        "first_name": "Mario",
        "last_name": "Rossi",
        "email": "controller@example.com",
        "password": "Password123!"
    }
    user_reg, verify_url = auth_controller.register(payload, "https://example.com/verify")
    assert user_reg.username == "nuovo_utente_controller"
    assert verify_url is not None

    db_token = token_repository.list_for_user(user_reg.id)[0]

    db_token.expires_at = utcnow() - timedelta(hours=1)
    db_session.commit()
    with pytest.raises(ValidationError, match="Verification token has expired."):
        auth_controller.verify_email(db_token.token)

    db_token.expires_at = utcnow() + timedelta(hours=1)
    db_session.commit()

    verified_user = auth_controller.verify_email(db_token.token)
    assert verified_user.is_email_verified is True

    with pytest.raises(ValidationError, match="Verification token is invalid."):
        auth_controller.verify_email(db_token.token)

    logged_user = auth_controller.login("nuovo_utente_controller", "Password123!")
    assert logged_user.id == user_reg.id