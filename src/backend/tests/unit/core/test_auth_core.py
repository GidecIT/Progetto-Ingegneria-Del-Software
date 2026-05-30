from __future__ import annotations

from unittest.mock import Mock
import pytest
from flask import g, session

import participium.core.auth
from participium.controllers.auth_controller import AuthController
from participium.core.auth import (
    current_user,
    login_required,
    login_user,
    logout_user,
    roles_required,
)
from participium.core.exceptions import AuthenticationError, AuthorizationError
from participium.models.enums import Role
from participium.models.user import User

pytestmark = pytest.mark.unit

def test_current_user_helper(flask_app, mock_citizen_user):
    with flask_app.test_request_context():
        if hasattr(g, "current_user"):
            delattr(g, "current_user")
        assert current_user() is None

        g.current_user = mock_citizen_user
        assert current_user() == mock_citizen_user


def test_login_user(flask_app, mock_citizen_user):
    with flask_app.test_request_context():
        login_user(mock_citizen_user)
        assert "user_id" in session
        assert session["user_id"] == mock_citizen_user.id


def test_logout_user_behavior(flask_app):
    with flask_app.test_request_context():
        session["user_id"] = 42
        logout_user()
        assert "user_id" not in session

        logout_user()
        assert "user_id" not in session


class TestLoginRequiredDecorator:

    def test_login_required_when_logged_in(self, flask_app, mock_citizen_user):
        mock_view = Mock(return_value="success_response")
        decorated_view = login_required(mock_view)

        with flask_app.test_request_context():
            g.current_user = mock_citizen_user
            result = decorated_view()

            assert result == "success_response"
            mock_view.assert_called_once()

    def test_login_required_api_endpoint_raises(self, flask_app):
        mock_view = Mock()
        decorated_view = login_required(mock_view)

        with flask_app.test_request_context(path="/api/v1/reports"):
            g.current_user = None

            with pytest.raises(AuthenticationError) as exc_info:
                decorated_view()

            assert "Authentication required." in str(exc_info.value)
            mock_view.assert_not_called()

    def test_login_required_web_endpoint_redirects(self, flask_app, monkeypatch):

        def stub_url_for(endpoint, **values):
            return f"/mocked-url-for/{endpoint}?next={values.get('next')}"

        monkeypatch.setattr(participium.core.auth, "url_for", stub_url_for)

        mock_view = Mock()
        decorated_view = login_required(mock_view)

        with flask_app.test_request_context(path="/dashboard"):
            g.current_user = None
            response = decorated_view()

            assert response.status_code == 302
            assert "/mocked-url-for/web.login" in response.headers["Location"]
            assert "next=/dashboard" in response.headers["Location"]
            mock_view.assert_not_called()


class TestRolesRequiredDecorator:
    def test_roles_required_no_user_raises(self, flask_app):
        mock_view = Mock()
        decorated_view = roles_required(Role.ADMIN)(mock_view)

        with flask_app.test_request_context():
            g.current_user = None

            with pytest.raises(AuthenticationError) as exc_info:
                decorated_view()

            assert "Authentication required." in str(exc_info.value)
            mock_view.assert_not_called()

    def test_roles_required_insufficient_permissions(self, flask_app, mock_citizen_user):
        mock_view = Mock()
        decorated_view = roles_required(Role.ADMIN)(mock_view)

        with flask_app.test_request_context():
            g.current_user = mock_citizen_user

            with pytest.raises(AuthorizationError) as exc_info:
                decorated_view()

            assert "You do not have permission" in str(exc_info.value)
            mock_view.assert_not_called()

    def test_roles_required_authorized_user_passes(self, flask_app, mock_admin_user):
        mock_view = Mock(return_value="content")
        decorated_view = roles_required(Role.ADMIN, Role.OPERATOR)(mock_view)

        with flask_app.test_request_context():
            g.current_user = mock_admin_user
            result = decorated_view()

            assert result == "content"
            mock_view.assert_called_once()

class TestAuthControllerDirect:

    def test_controller_flows(self):
        mock_auth_service = Mock()
        controller = AuthController(mock_auth_service)
        mock_user = Mock(spec=User)

        mock_auth_service.register_user.return_value = (mock_user, "https://verify.url")
        payload = {"username": "test"}
        user, url = controller.register(payload, "https://verify.url")
        assert user == mock_user
        assert url == "https://verify.url"
        mock_auth_service.register_user.assert_called_once_with(payload, "https://verify.url")

        mock_auth_service.verify_email.return_value = mock_user
        assert controller.verify_email("token123") == mock_user
        mock_auth_service.verify_email.assert_called_once_with("token123")

        mock_auth_service.authenticate.return_value = mock_user
        assert controller.login("test", "pass") == mock_user
        mock_auth_service.authenticate.assert_called_once_with("test", "pass")