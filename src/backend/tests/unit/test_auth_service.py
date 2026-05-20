import pytest
from datetime import datetime, timedelta
from participium.services.auth_service import AuthService
from participium.core.exceptions import ValidationError, AuthenticationError
from participium.models.enums import Role
from participium.models.user import User
from participium.models.token import EmailVerificationToken

class StubSession:
    def __init__(self):
        self.flushed = False
        self.committed = False

    def flush(self): self.flushed = True

    def commit(self): self.committed = True


class StubUserRepository:
    def __init__(self, by_username=None, by_email=None, by_identity=None):
        self._by_username = by_username or {}
        self._by_email = by_email or {}
        self._by_identity = by_identity or {}
        self.added = []

    def get_by_username(self, username): return self._by_username.get(username)

    def get_by_email(self, email): return self._by_email.get(email)

    def get_by_username_or_email(self, identifier): return self._by_identity.get(identifier)

    def add(self, user): self.added.append(user)


class StubTokenRepository:
    def __init__(self, tokens=None):
        self._tokens = tokens or {}
        self.added = []

    def get_by_token(self, token_val): return self._tokens.get(token_val)

    def add(self, token): self.added.append(token)


class StubEmailGateway:
    def __init__(self):
        self.sent_mails = []

    def send(self, recipient, subject, body):
        self.sent_mails.append({"recipient": recipient, "subject": subject, "body": body})


# --- TEST CASES ---
@pytest.mark.parametrize("missing_field", ["username", "first_name", "last_name", "email", "password"])
def test_register_missing_fields_validation(missing_field):

    base_payload = {"username": "u", "first_name": "f", "last_name": "l", "email": "e@t.com", "password": "p"}
    base_payload[missing_field] = ""  # Svuota il campo sotto test

    service = AuthService(StubSession(), StubUserRepository(), StubTokenRepository(), StubEmailGateway())
    with pytest.raises(ValidationError) as exc_info:
        service.register_user(base_payload)
    assert "Missing required fields" in str(exc_info.value)


def test_register_duplicate_username_or_email_validation():
    from participium.core.security import hash_password
    existing_user = User(username="dupe", first_name="A", last_name="B", email="dupe@t.com",
                         password_hash=hash_password("p"), role=Role.CITIZEN)

    u_repo = StubUserRepository(by_username={"dupe": existing_user})
    service = AuthService(StubSession(), u_repo, StubTokenRepository(), StubEmailGateway())
    with pytest.raises(ValidationError) as exc_info:
        service.register_user(
            {"username": "dupe", "first_name": "X", "last_name": "Y", "email": "new@t.com", "password": "p"})
    assert "Username already in use." in str(exc_info.value)

    u_repo = StubUserRepository(by_email={"dupe@t.com": existing_user})
    service = AuthService(StubSession(), u_repo, StubTokenRepository(), StubEmailGateway())
    with pytest.raises(ValidationError) as exc_info:
        service.register_user(
            {"username": "new", "first_name": "X", "last_name": "Y", "email": "dupe@t.com", "password": "p"})
    assert "Email already in use." in str(exc_info.value)


def test_register_user_success_flow():
    session = StubSession()
    u_repo = StubUserRepository()
    t_repo = StubTokenRepository()
    email_gw = StubEmailGateway()
    service = AuthService(session, u_repo, t_repo, email_gw)

    payload = {
        "username": "   citizen_one  ",
        "first_name": " Mario ",
        "last_name": "Rossi",
        "email": "MARIO.ROSSI@Domain.Com",
        "password": "Password123!"
    }

    user, url = service.register_user(payload, verification_base_url="https://participium.org/verify")

    assert user.username == "citizen_one"
    assert user.email == "mario.rossi@domain.com"
    assert user.role == Role.CITIZEN
    assert user.is_email_verified is False

    assert session.flushed is True
    assert session.committed is True
    assert len(t_repo.added) == 1
    assert len(email_gw.sent_mails) == 1
    assert t_repo.added[0].token in url


def test_verify_email_all_branches(monkeypatch):
    now_time = datetime(2026, 5, 18, 12, 0, 0)
    monkeypatch.setattr("participium.services.auth_service.utcnow", lambda: now_time)

    session = StubSession()
    user = User(username="u", first_name="f", last_name="l", email="e@t.com", password_hash="h", role=Role.CITIZEN)

    t_repo = StubTokenRepository(tokens={})
    service = AuthService(session, StubUserRepository(), t_repo, StubEmailGateway())
    with pytest.raises(ValidationError) as exc_info:
        service.verify_email("unknown_token")
    assert "Verification token is invalid." in str(exc_info.value)

    used_token = EmailVerificationToken(user_id=1, token="used", expires_at=now_time + timedelta(hours=1), is_used=True)
    used_token.user = user
    t_repo = StubTokenRepository(tokens={"used": used_token})
    service = AuthService(session, StubUserRepository(), t_repo, StubEmailGateway())
    with pytest.raises(ValidationError):
        service.verify_email("used")

    expired_token = EmailVerificationToken(user_id=1, token="expired", expires_at=now_time - timedelta(seconds=1),
                                           is_used=False)
    expired_token.user = user
    t_repo = StubTokenRepository(tokens={"expired": expired_token})
    service = AuthService(session, StubUserRepository(), t_repo, StubEmailGateway())
    with pytest.raises(ValidationError) as exc_info:
        service.verify_email("expired")
    assert "Verification token has expired." in str(exc_info.value)

    valid_token = EmailVerificationToken(user_id=1, token="valid", expires_at=now_time + timedelta(hours=1),
                                         is_used=False)
    valid_token.user = user
    t_repo = StubTokenRepository(tokens={"valid": valid_token})
    service = AuthService(session, StubUserRepository(), t_repo, StubEmailGateway())

    returned_user = service.verify_email("valid")
    assert returned_user.is_email_verified is True
    assert valid_token.is_used is True
    assert session.committed is True


def test_authenticate_exception_and_success_paths():
    from participium.core.security import hash_password
    h = hash_password("ValidPass123!")

    active_verified = User(username="active", first_name="f", last_name="l", email="a@t.com", password_hash=h,
                           role=Role.CITIZEN, is_active=True, is_email_verified=True)
    inactive_user = User(username="inactive", first_name="f", last_name="l", email="i@t.com", password_hash=h,
                         role=Role.CITIZEN, is_active=False, is_email_verified=True)
    unverified_user = User(username="unverified", first_name="f", last_name="l", email="u@t.com", password_hash=h,
                           role=Role.CITIZEN, is_active=True, is_email_verified=False)

    u_repo = StubUserRepository(by_identity={
        "active": active_verified,
        "inactive": inactive_user,
        "unverified": unverified_user
    })
    service = AuthService(StubSession(), u_repo, StubTokenRepository(), StubEmailGateway())

    with pytest.raises(AuthenticationError) as exc_info:
        service.authenticate("active", "wrong_password")
    assert "Invalid credentials." in str(exc_info.value)

    with pytest.raises(AuthenticationError):
        service.authenticate("ghost_user", "ValidPass123!")

    with pytest.raises(AuthenticationError):
        service.authenticate("inactive", "ValidPass123!")

    with pytest.raises(AuthenticationError) as exc_info:
        service.authenticate("unverified", "ValidPass123!")
    assert "Email verification is required before login." in str(exc_info.value)

    assert service.authenticate("  active ",
                                "ValidPass123!") == active_verified