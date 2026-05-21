from __future__ import annotations

from unittest.mock import Mock
import pytest
from flask import Flask, g, session

from participium.core.auth import (
    current_user,
    login_required,
    login_user,
    logout_user,
    roles_required,
)
from participium.core.exceptions import AuthenticationError, AuthorizationError
from participium.models.enums import Role

pytestmark = pytest.mark.unit

@pytest.fixture
def app():
    app = Flask("test_auth_core_app")
    app.secret_key = "super_secret_key_for_testing"
    return app


@pytest.fixture
def mock_citizen_user():
    user = Mock()
    user.id = 1
    user.role = Role.CITIZEN
    return user


@pytest.fixture
def mock_admin_user():
    user = Mock()
    user.id = 3
    user.role = Role.ADMIN
    return user

def test_current_user_helper(app, mock_citizen_user):
    with app.test_request_context():
        if hasattr(g, "current_user"):
            delattr(g, "current_user")
        assert current_user() is None

        g.current_user = mock_citizen_user
        assert current_user() == mock_citizen_user


def test_login_user(app, mock_citizen_user):
    with app.test_request_context():
        login_user(mock_citizen_user)
        assert "user_id" in session
        assert session["user_id"] == 1


def test_login_required_decorator_branching(app, monkeypatch, mock_citizen_user):
    def stub_url_for(endpoint, **values):
        return f"/mocked-url-for/{endpoint}"

    import participium.core.auth

    monkeypatch.setattr(participium.core.auth, "url_for", stub_url_for)

    def mock_view(*args, **kwargs):
        return "view_executed_successfully"

    decorated_view = login_required(mock_view)

    with app.test_request_context(path="/api/v1/resources"):
        g.current_user = None
        with pytest.raises(AuthenticationError) as exc_info:
            decorated_view()
        assert "Authentication required." in str(exc_info.value)

    with app.test_request_context(path="/dashboard"):
        g.current_user = None
        response = decorated_view()
        assert response.status_code == 302
        assert "/mocked-url-for/web.login" in response.headers["Location"]

    with app.test_request_context(path="/dashboard"):
        g.current_user = mock_citizen_user
        result = decorated_view()
        assert result == "view_executed_successfully"


def test_roles_required_decorator_authorization_matrix(
    app, mock_citizen_user, mock_admin_user
):
    def mock_view(*args, **kwargs):
        return "view_executed_successfully"

    decorated_view = roles_required(Role.ADMIN)(mock_view)

    with app.test_request_context():
        g.current_user = None
        with pytest.raises(AuthenticationError):
            decorated_view()

        g.current_user = mock_citizen_user
        with pytest.raises(AuthorizationError) as exc_info:
            decorated_view()
        assert "You do not have permission" in str(exc_info.value)

        g.current_user = mock_admin_user
        result = decorated_view()
        assert result == "view_executed_successfully"

def test_logout_user_behavior(app):
    with app.test_request_context():
        session["user_id"] = 42
        assert "user_id" in session

        logout_user()
        assert "user_id" not in session

        logout_user()
        assert "user_id" not in session