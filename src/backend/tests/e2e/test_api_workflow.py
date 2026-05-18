from __future__ import annotations

import io
import pytest
from flask.testing import FlaskClient

from participium import create_app
from participium.database import close_connection, get_session
from participium.models.category import Category
from participium.models.user import User
from participium.models.enums import Role

@pytest.fixture
def app_client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    monkeypatch.setenv("AUTO_INIT_DB", "true")
    monkeypatch.setenv("BOOTSTRAP_REFERENCE_DATA", "true")
    monkeypatch.setenv("BOOTSTRAP_DEMO_DATA", "false")
    monkeypatch.setenv("EXPOSE_VERIFICATION_LINKS", "true")

    application = create_app()
    application.config.update(TESTING=True)
    client = application.test_client()
    
    yield client
    
    close_connection()

@pytest.mark.e2e
def test_health_check(app_client: FlaskClient):
    response = app_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

@pytest.mark.e2e
def test_reference_data(app_client: FlaskClient):
    response = app_client.get("/api/v1/meta/reference-data")
    assert response.status_code == 200
    data = response.get_json()
    assert "roles" in data
    assert "report_statuses" in data

@pytest.mark.e2e
def test_auth_workflow(app_client: FlaskClient):
    # 1. Register
    reg_payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password123!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = app_client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["user"]["username"] == "testuser"
    verification_url = data.get("verification_url")
    assert verification_url is not None

    # Extract token from URL
    token = verification_url.split("/")[-1]

    # 2. Verify Email
    response = app_client.get(f"/api/v1/auth/verify/{token}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Email verified."

    # 3. Login
    login_payload = {
        "identifier": "testuser",
        "password": "Password123!"
    }
    response = app_client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Logged in."

    # 4. Get Me
    response = app_client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.get_json()["username"] == "testuser"

    # 5. Logout
    response = app_client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    
    # 6. Verify Logged Out
    response = app_client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.e2e
def test_report_workflow(app_client: FlaskClient):
    # Setup: Register and Login
    reg_payload = {
        "username": "reporter",
        "email": "reporter@example.com",
        "password": "Password123!",
        "first_name": "Reporter",
        "last_name": "User"
    }
    app_client.post("/api/v1/auth/register", json=reg_payload)
    
    # Manually activate and verify user in DB to skip email flow for this test
    from participium.database import get_session
    with app_client.application.app_context():
        session = get_session()
        user = session.query(User).filter_by(username="reporter").first()
        user.is_active = True
        user.is_email_verified = True
        user.role = Role.CITIZEN
        session.commit()

    login_resp = app_client.post("/api/v1/auth/login", json={
        "identifier": "reporter",
        "password": "Password123!"
    })
    assert login_resp.status_code == 200

    # 1. List Categories
    response = app_client.get("/api/v1/categories")
    assert response.status_code == 200
    categories = response.get_json()
    assert len(categories) > 0
    cat_id = categories[0]["id"]

    # 2. Create Report
    report_data = {
        "title": "Test Report",
        "description": "Test Description",
        "category_id": cat_id,
        "latitude": 45.0,
        "longitude": 7.0,
        "is_anonymous": "false"
    }
    # Mocking a photo upload
    data = {**report_data}
    data["photos"] = (io.BytesIO(b"fake image content"), "test.jpg")
    
    response = app_client.post(
        "/api/v1/reports",
        data=data,
        content_type="multipart/form-data"
    )
    assert response.status_code == 201
    report = response.get_json()
    assert report["title"] == "Test Report"
    report_id = report["id"]

    # 3. Get Report Detail
    response = app_client.get(f"/api/v1/reports/{report_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Test Report"

    # 4. List My Reports
    response = app_client.get("/api/v1/users/me/reports")
    assert response.status_code == 200
    my_reports = response.get_json()
    assert any(r["id"] == report_id for r in my_reports)
