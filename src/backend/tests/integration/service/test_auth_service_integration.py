import pytest

from datetime import timedelta
from flask import Flask, g, session
from unittest.mock import Mock

from participium.controllers.auth_controller import AuthController
from participium.core.exceptions import AuthenticationError, AuthorizationError, ValidationError
from participium.core.utils import utcnow
from participium.models.enums import Role
from participium.models.token import EmailVerificationToken
from participium.models.user import User
from participium.core.auth import login_required, roles_required, login_user, logout_user, current_user
from participium.services.auth_service import AuthService


class TestAuthServiceAdditionalExceptions:
    """Verifica i rami difensivi e le eccezioni rimaste scoperte in AuthService usando fixture reali."""

    def test_registration_with_missing_fields_raises_validation_error(self, db_session, user_repository,
                                                                      token_repository):
        mock_email_gateway = Mock()
        service = AuthService(db_session, user_repository, token_repository, mock_email_gateway)

        incomplete_payload = {
            "username": "test_missing",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "mario@example.com"

        }
        with pytest.raises(ValidationError, match="Missing required fields"):
            service.register_user(incomplete_payload)

    def test_registration_with_duplicate_username_raises_error(self, db_session, user_repository, token_repository):
        mock_email_gateway = Mock()
        service = AuthService(db_session, user_repository, token_repository, mock_email_gateway)

        existing_user = User(username="duplicato", email="primo@ex.com", first_name="A", last_name="B",
                             password_hash="h")
        user_repository.add(existing_user)
        db_session.commit()

        payload = {"username": "duplicato", "first_name": "X", "last_name": "Y", "email": "secondo@ex.com",
                   "password": "P!"}
        with pytest.raises(ValidationError, match="Username already in use."):
            service.register_user(payload)

    def test_registration_with_duplicate_email_raises_error(self, db_session, user_repository, token_repository):
        mock_email_gateway = Mock()
        service = AuthService(db_session, user_repository, token_repository, mock_email_gateway)

        existing_user = User(username="primo", email="duplicata@ex.com", first_name="A", last_name="B",
                             password_hash="h")
        user_repository.add(existing_user)
        db_session.commit()

        payload = {"username": "secondo", "first_name": "X", "last_name": "Y", "email": "duplicata@ex.com",
                   "password": "P!"}
        with pytest.raises(ValidationError, match="Email already in use."):
            service.register_user(payload)

    def test_verify_email_with_expired_token_raises_error(self, db_session, user_repository, token_repository):
        mock_email_gateway = Mock()
        service = AuthService(db_session, user_repository, token_repository, mock_email_gateway)

        user = user_repository.add(
            User(username="scaduto", email="s@ex.com", first_name="A", last_name="B", password_hash="h"))
        db_session.commit()

        token = EmailVerificationToken(user_id=user.id, token="token_scaduto", expires_at=utcnow() - timedelta(hours=1))
        token_repository.add(token)
        db_session.commit()

        with pytest.raises(ValidationError, match="Verification token has expired."):
            service.verify_email("token_scaduto")


class TestAuthControllerIntegration:
    """Esercita interamente il file auth_controller.py coordinandosi con le fixture reali."""

    def test_controller_delegates_correctly_to_service(self, db_session, user_repository, token_repository):
        mock_email_gateway = Mock()
        service = AuthService(db_session, user_repository, token_repository, mock_email_gateway)
        controller = AuthController(service)

        payload = {
            "username": "user_controller",
            "first_name": "Mario",
            "last_name": "Rossi",
            "email": "controller@example.com",
            "password": "Password123!"
        }

        user, _ = controller.register(payload)
        assert user.username == "user_controller"

        tokens = token_repository.list_for_user(user.id)
        assert len(tokens) > 0
        token_value = tokens[0].token

        verified_user = controller.verify_email(token_value)
        assert verified_user.is_email_verified is True

        logged_user = controller.login("user_controller", "Password123!")
        assert logged_user.id == user.id


class TestAuthMiddlewareIntegration:
    """Testa le funzioni condizionali e i decoratori presenti in auth.py attingendo da conftest.py."""

    def test_current_user_helper(self, test_app):
        with test_app.test_request_context():
            assert current_user() is None

            class FakeUser: pass

            g.current_user = FakeUser()
            assert current_user() == g.current_user

    def test_login_required_redirects_for_web_routes(self, test_app):
        client = test_app.test_client()
        with test_app.app_context():
            if hasattr(g, "current_user"): delattr(g, "current_user")
            response = client.get("/web/dashboard")

            assert response.status_code == 302
            assert "/login?next=/web/dashboard" in response.headers["Location"]

    def test_login_required_raises_error_for_api_routes(self, test_app):
        client = test_app.test_client()
        with test_app.app_context():
            if hasattr(g, "current_user"): delattr(g, "current_user")
            with pytest.raises(AuthenticationError, match="Authentication required"):
                client.get("/api/v1/data")

    def test_roles_required_raises_error_when_no_user(self, test_app):
        client = test_app.test_client()
        with test_app.app_context():
            if hasattr(g, "current_user"): delattr(g, "current_user")
            with pytest.raises(AuthenticationError, match="Authentication required"):
                client.get("/api/admin")

    def test_roles_required_denies_unauthorized_role(self, test_app):
        client = test_app.test_client()

        class CitizenUser:
            id = 10
            role = Role.CITIZEN

        @test_app.before_request
        def set_user():
            g.current_user = CitizenUser()

        with pytest.raises(AuthorizationError, match="You do not have permission"):
            client.get("/api/admin")

    def test_login_and_logout_utility_functions(self, test_app):
        class FakeUser: id = 99

        with test_app.test_request_context():
            login_user(FakeUser())
            assert session["user_id"] == 99
            logout_user()
            assert "user_id" not in session