import pytest
from datetime import datetime, timedelta
from participium.controllers.auth_controller import AuthController
from participium.services.auth_service import AuthService
from participium.core.exceptions import ValidationError, AuthenticationError
from participium.models.user import User
from participium.models.enums import Role


# Mock dei componenti minimi per l'esecuzione E2E orchestrata dal controllore
class MockedUserRepository:
    def get_by_username(self, name): return None

    def get_by_email(self, mail): return None

    def add(self, user): user.id = 123

    def get_by_username_or_email(self, identifier):
        if identifier == "valid_citizen":
            # Ritorna un utente valido pronto al login
            from participium.core.security import hash_password
            u = User(username="valid_citizen", first_name="A", last_name="B", email="v@t.com",
                     password_hash=hash_password("password123"), role=Role.CITIZEN)
            u.is_email_verified = True
            u.is_active = True
            return u
        return None


class MockedTokenRepository:
    def add(self, token): pass

    def get_by_token(self, value):
        if value == "valid_token":
            from participium.core.utils import utcnow
            u = User(username="u", first_name="f", last_name="l", email="e@t.com", password_hash="h", role=Role.CITIZEN)
            return type("FakeToken", (),
                        {"token": "valid_token", "is_used": False, "expires_at": utcnow() + timedelta(hours=1),
                         "user": u})()
        return None


class MockedEmailGateway:
    def send(self, recipient, subject, body): pass


class MockedSession:
    def flush(self): pass

    def commit(self): pass


@pytest.fixture
def auth_controller():
    service = AuthService(MockedSession(), MockedUserRepository(), MockedTokenRepository(), MockedEmailGateway())
    return AuthController(service)


def test_controller_registration_e2e_flow(auth_controller):
    """Testa il metodo di registrazione del controllore end-to-end."""
    payload = {
        "username": "new_user",
        "first_name": "E2E",
        "last_name": "Testing",
        "email": "e2e@participium.org",
        "password": "super_safe_password"
    }
    user, url = auth_controller.register(payload, verification_base_url="https://participium.gov/verify")
    assert user.username == "new_user"
    assert "https://participium.gov/verify/" in url


def test_controller_login_e2e_success_and_failures(auth_controller):

    logged_user = auth_controller.login("valid_citizen", "password123")
    assert logged_user.username == "valid_citizen"

    with pytest.raises(AuthenticationError):
        auth_controller.login("valid_citizen", "wrong_password_attempt")

    with pytest.raises(AuthenticationError):
        auth_controller.login("non_existent_user", "any_password")


def test_controller_verify_email_e2e(auth_controller):
    user = auth_controller.verify_email("valid_token")
    assert user.is_email_verified is True

    with pytest.raises(ValidationError):
        auth_controller.verify_email("invalid_or_expired_token")