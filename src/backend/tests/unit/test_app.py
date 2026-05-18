from __future__ import annotations

import pytest
from flask import Flask, g, session
from unittest.mock import MagicMock, patch

from participium.app import create_app
from participium.config import Settings
from participium.core.exceptions import DomainError
from participium.models.user import User

@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=Settings)
    settings.secret_key = "test-secret"
    settings.max_content_length = 1024 * 1024
    settings.frontend_origin = "http://localhost:3000"
    settings.instance_path = "/tmp/instance"
    settings.auto_init_db = False
    return settings

def test_create_app_initialization(mock_settings):
    """Test that create_app initializes the Flask app correctly."""
    # Mocking open_connection to avoid DB connection during tests
    with patch("participium.app.open_connection"):
        app = create_app(mock_settings)
        
        assert isinstance(app, Flask)
        assert app.config["SECRET_KEY"] == "test-secret"
        assert app.config["MAX_CONTENT_LENGTH"] == 1024 * 1024
        assert app.config["SETTINGS"] == mock_settings
        assert "container" in app.extensions

def test_create_app_with_db_init(mock_settings):
    """Test that create_app initializes the database if auto_init_db is True."""
    mock_settings.auto_init_db = True
    mock_settings.bootstrap_reference_data = True
    mock_settings.bootstrap_demo_data = True
    
    with patch("participium.app.open_connection"), \
         patch("participium.app.create_all") as mock_create_all, \
         patch("participium.app.seed_reference_data") as mock_seed_ref, \
         patch("participium.app.seed_demo_data") as mock_seed_demo, \
         patch("participium.app.get_session"):
        
        create_app(mock_settings)
        
        mock_create_all.assert_called_once()
        mock_seed_ref.assert_called_once()
        mock_seed_demo.assert_called_once()

def test_load_current_user_hook_no_user_id(mock_settings):
    """Test load_current_user hook when no user_id is in session."""
    with patch("participium.app.open_connection"):
        app = create_app(mock_settings)
        
        with app.test_request_context():
            # Trigger before_request
            app.preprocess_request()
            assert g.current_user is None

def test_load_current_user_hook_valid_user(mock_settings):
    """Test load_current_user hook when a valid user_id is in session."""
    mock_user = MagicMock(spec=User)
    mock_user.is_active = True
    
    with patch("participium.app.open_connection"), \
         patch("participium.app.UserRepository") as mock_repo_cls:
        
        mock_repo = mock_repo_cls.return_value
        mock_repo.get_by_id.return_value = mock_user
        
        app = create_app(mock_settings)
        
        with app.test_request_context():
            session["user_id"] = 1
            app.preprocess_request()
            assert g.current_user == mock_user

def test_load_current_user_hook_inactive_user(mock_settings):
    """Test load_current_user hook when user is inactive."""
    mock_user = MagicMock(spec=User)
    mock_user.is_active = False
    
    with patch("participium.app.open_connection"), \
         patch("participium.app.UserRepository") as mock_repo_cls:
        
        mock_repo = mock_repo_cls.return_value
        mock_repo.get_by_id.return_value = mock_user
        
        app = create_app(mock_settings)
        
        with app.test_request_context():
            session["user_id"] = 1
            app.preprocess_request()
            assert g.current_user is None
            assert "user_id" not in session

def test_domain_error_handler(mock_settings):
    """Test the DomainError handler."""
    with patch("participium.app.open_connection"):
        app = create_app(mock_settings)
        
        @app.route("/error")
        def trigger_error():
            raise DomainError("Test error", status_code=400)
        
        client = app.test_client()
        response = client.get("/error")
        
        assert response.status_code == 400
        assert response.json == {"error": "Test error"}

def test_404_error_handler(mock_settings):
    """Test the 404 error handler."""
    with patch("participium.app.open_connection"):
        app = create_app(mock_settings)
        client = app.test_client()
        response = client.get("/non-existent-path")
        
        assert response.status_code == 404
        assert response.json == {"error": "Resource not found."}

def test_teardown_appcontext(mock_settings):
    """Test that remove_session is called on app context teardown."""
    with patch("participium.app.open_connection"), \
         patch("participium.app.remove_session") as mock_remove_session:
        
        app = create_app(mock_settings)
        with app.app_context():
            pass
        
        mock_remove_session.assert_called_once()
