from __future__ import annotations

import pytest
from flask import Flask, g, session
from participium.core.exceptions import AuthenticationError, AuthorizationError
from participium.core.auth import (
    login_required,
    roles_required,
    current_user,
    login_user,
    logout_user
)
from participium.models.enums import Role


class DummyUser:
    def __init__(self, id: int, role: Role):
        self.id = id
        self.role = role

@pytest.fixture
def app():
    app = Flask("test_auth_core_app")
    app.secret_key = "super_secret_key_for_testing"
    return app

def test_current_user_helper(app):
    with app.test_request_context():
        if hasattr(g, "current_user"):
            delattr(g, "current_user")
        assert current_user() is None

        user = DummyUser(id=99, role=Role.CITIZEN)
        g.current_user = user
        assert current_user() == user


def test_login_user(app):
    user = DummyUser(id=42, role=Role.CITIZEN)

    with app.test_request_context():
        login_user(user)
        assert "user_id" in session
        assert session["user_id"] == 42


def test_logout_user(app):
    with app.test_request_context():

        session["user_id"] = 42
        logout_user()
        assert "user_id" not in session

        logout_user()
        assert "user_id" not in session

def test_login_required_decorator_branching(app, monkeypatch):
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
        g.current_user = DummyUser(id=1, role=Role.CITIZEN)
        result = decorated_view()
        assert result == "view_executed_successfully"


def test_roles_required_decorator_authorization_matrix(app):
    def mock_view(*args, **kwargs):
        return "view_executed_successfully"

    decorated_view = roles_required(Role.ADMIN)(mock_view)

    with app.test_request_context():
        g.current_user = None
        with pytest.raises(AuthenticationError):
            decorated_view()

        g.current_user = DummyUser(id=2, role=Role.CITIZEN)
        with pytest.raises(AuthorizationError) as exc_info:
            decorated_view()
        assert "You do not have permission" in str(exc_info.value)

        g.current_user = DummyUser(id=3, role=Role.ADMIN)
        result = decorated_view()
        assert result == "view_executed_successfully"