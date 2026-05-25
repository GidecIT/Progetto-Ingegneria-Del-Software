import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, g, session, jsonify
from participium.app import create_app, _register_request_hooks, _register_error_handlers
from participium.config.settings import Settings
from participium.core.exceptions import DomainError
from pathlib import Path

@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=Settings)
    settings.secret_key = "test_secret"
    settings.max_content_length = 1024 * 1024
    settings.frontend_origin = "http://localhost:3000"
    settings.auto_init_db = False
    settings.instance_path = Path("/tmp/instance").absolute()
    settings.media_root = Path("/tmp/media").absolute()
    return settings

def test_create_app(mock_settings):
    with patch("participium.app.open_connection"), \
         patch("participium.app.AppContainer"), \
         patch("participium.app.init_swagger"), \
         patch("participium.app.register_blueprints"):
        app = create_app(mock_settings)
        assert isinstance(app, Flask)
        assert app.config["SECRET_KEY"] == "test_secret"
        assert app.config["MAX_CONTENT_LENGTH"] == 1024 * 1024

def test_create_app_with_db_init_selective(mock_settings):
    # Test case where bootstrap_reference_data is True but bootstrap_demo_data is False
    mock_settings.auto_init_db = True
    mock_settings.bootstrap_reference_data = True
    mock_settings.bootstrap_demo_data = False
    
    with patch("participium.app.open_connection"), \
         patch("participium.app.AppContainer"), \
         patch("participium.app.init_swagger"), \
         patch("participium.app.register_blueprints"), \
         patch("participium.app.create_all"), \
         patch("participium.app.seed_reference_data") as mock_seed_ref, \
         patch("participium.app.seed_demo_data") as mock_seed_demo, \
         patch("participium.app.get_session"):
        
        create_app(mock_settings)
        assert mock_seed_ref.called
        assert not mock_seed_demo.called

def test_create_app_no_settings():
    # Test create_app with None settings to trigger Settings.from_env()
    with patch("participium.app.Settings.from_env") as mock_from_env, \
         patch("participium.app.open_connection"), \
         patch("participium.app.AppContainer"), \
         patch("participium.app.init_swagger"), \
         patch("participium.app.register_blueprints"), \
         patch("participium.app.Flask") as mock_flask_class:
        
        mock_settings = MagicMock()
        mock_settings.instance_path = "/tmp"
        mock_from_env.return_value = mock_settings
        
        create_app(None)
        assert mock_from_env.called

def test_load_current_user_hook_no_session(mock_settings):
    app = Flask(__name__)
    _register_request_hooks(app)
    
    with app.test_request_context():
        # Simula il trigger del hook before_request
        app.preprocess_request()
        assert g.current_user is None

def test_load_current_user_hook_valid_user(mock_settings):
    app = Flask(__name__)
    app.secret_key = "test"
    _register_request_hooks(app)
    
    mock_user = MagicMock()
    mock_user.is_active = True
    
    with app.test_request_context():
        session["user_id"] = 1
        with patch("participium.app.UserRepository") as mock_repo_class, \
             patch("participium.app.get_session"):
            mock_repo = mock_repo_class.return_value
            mock_repo.get_by_id.return_value = mock_user
            
            app.preprocess_request()
            assert g.current_user == mock_user

def test_load_current_user_hook_inactive_user(mock_settings):
    app = Flask(__name__)
    app.secret_key = "test"
    _register_request_hooks(app)
    
    mock_user = MagicMock()
    mock_user.is_active = False
    
    with app.test_request_context():
        session["user_id"] = 1
        with patch("participium.app.UserRepository") as mock_repo_class, \
             patch("participium.app.get_session"):
            mock_repo = mock_repo_class.return_value
            mock_repo.get_by_id.return_value = mock_user
            
            app.preprocess_request()
            assert g.current_user is None
            assert "user_id" not in session

def test_teardown_hook():
    app = Flask(__name__)
    _register_request_hooks(app)
    
    with patch("participium.app.remove_session") as mock_remove:
        with app.app_context():
            # Il teardown viene chiamato alla fine del context dell'app o della richiesta
            pass
        # Flask chiama teardown_appcontext alla fine del context dell'applicazione
        # Ma di solito viene chiamato dopo che il context viene rimosso dalla stack
        # In questo caso dobbiamo assicurarci che venga chiamato.
        app.do_teardown_appcontext()
        assert mock_remove.called

def test_error_handlers():
    app = Flask(__name__)
    _register_error_handlers(app)
    
    client = app.test_client()
    
    # Test DomainError via client request
    @app.route("/error")
    def trigger_error():
        raise DomainError("Test error", status_code=400)
    
    response = client.get("/error")
    assert response.status_code == 400
    assert response.json == {"error": "Test error"}
    
    # Test 404 via client request
    response = client.get("/non-existent")
    assert response.status_code == 404
    assert response.json == {"error": "Resource not found."}
