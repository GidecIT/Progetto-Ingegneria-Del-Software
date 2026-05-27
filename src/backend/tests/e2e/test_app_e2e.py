import os
import pytest
from participium.app import create_app
from participium.config import Settings
from participium.models.user import User
from participium.database import get_session

def test_app_init_db_false():
    settings = Settings.from_env()
    settings.auto_init_db = False
    app = create_app(settings)
    assert app.config["SETTINGS"].auto_init_db is False

def test_app_init_db_no_ref_data():
    settings = Settings.from_env()
    settings.auto_init_db = True
    settings.bootstrap_reference_data = False
    settings.bootstrap_demo_data = False
    app = create_app(settings)
    assert app.config["SETTINGS"].bootstrap_reference_data is False

def test_app_init_db_no_demo_data():
    settings = Settings.from_env()
    settings.auto_init_db = True
    settings.bootstrap_reference_data = True
    settings.bootstrap_demo_data = False
    app = create_app(settings)
    assert app.config["SETTINGS"].bootstrap_demo_data is False

def test_not_found_handler(client):
    response = client.get("/api/v1/invalid-route-that-does-not-exist")
    assert response.status_code == 404
    assert response.json["error"] == "Resource not found."

def test_before_request_invalid_user(client, clean_db):
    with client.session_transaction() as sess:
        sess["user_id"] = 9999
    
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "user_id" not in sess

def test_before_request_inactive_user(client, clean_db):
    db_session = get_session()
    user = User(username="inactive", email="inactive@test.com", password_hash="hash", first_name="A", last_name="B", role="CITIZEN", is_active=False)
    db_session.add(user)
    db_session.commit()
    user_id = user.id
    db_session.close()

    with client.session_transaction() as sess:
        sess["user_id"] = user_id
    
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "user_id" not in sess
