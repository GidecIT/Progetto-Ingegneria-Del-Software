import pytest
from datetime import datetime, timedelta
from flask import jsonify, Blueprint
from participium.database import get_session
from participium.models.user import User
from participium.models.token import EmailVerificationToken
from participium.models.enums import Role
from participium.core.auth import login_required, roles_required


@pytest.mark.e2e
def test_user_authentication_flow_e2e(client, app, clean_db):
    from participium import create_app
    test_app = create_app()
    test_app.config["TESTING"] = True
    
    fake_web_bp = Blueprint("web", __name__)

    @fake_web_bp.route("/login")
    def login():
        return "Fake Login Page"

    test_app.register_blueprint(fake_web_bp)

    @test_app.route("/dashboard-web")
    @login_required
    def fake_web_route():
        return "Web Dashboard"

    @test_app.route("/api/v1/test-roles-allowed")
    @login_required
    @roles_required(Role.CITIZEN, Role.OPERATOR)
    def fake_roles_allowed_route():
        return jsonify({"status": "allowed"})

    @test_app.route("/api/v1/test-roles-only")
    @roles_required(Role.ADMIN)
    def fake_roles_only_route():
        return jsonify({"status": "admin_only"})

    test_client = test_app.test_client()

    response_web_redirect = test_client.get("/dashboard-web")
    assert response_web_redirect.status_code == 302
    assert "next=/dashboard-web" in response_web_redirect.location

    response_roles_no_user = test_client.get("/api/v1/test-roles-only")
    assert response_roles_no_user.status_code == 401

    incomplete_payload = {
        "username": "mario_mancante",
        "password": "SecurePassword123!"
    }
    response_missing = client.post("/api/v1/auth/register", json=incomplete_payload)
    assert response_missing.status_code == 400

    register_payload = {
        "username": "cittadino_e2e",
        "email": "cittadino@example.com",
        "first_name": "Mario",
        "last_name": "Rossi",
        "password": "SecurePassword123!"
    }
    
    app.config["SETTINGS"].expose_verification_links = True
    response = client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    assert "verification_url" in response.json
    app.config["SETTINGS"].expose_verification_links = False
    assert response.json["user"]["username"] == "cittadino_e2e"

    register_payload_custom_url = {
        "username": "utente_custom_url",
        "email": "custom_url@example.com",
        "first_name": "Luca",
        "last_name": "Bianchi",
        "password": "SecurePassword123!",
        "verification_base_url": "https://participium.it/verify"
    }
    response_url = client.post("/api/v1/auth/register", json=register_payload_custom_url)
    assert response_url.status_code == 201

    duplicate_user_payload = register_payload.copy()
    duplicate_user_payload["email"] = "differente@example.com"
    response_dup = client.post("/api/v1/auth/register", json=duplicate_user_payload)
    assert response_dup.status_code in [400, 409]

    duplicate_email_payload = register_payload.copy()
    duplicate_email_payload["username"] = "differente_username"
    response_email_dup = client.post("/api/v1/auth/register", json=duplicate_email_payload)
    assert response_email_dup.status_code in [400, 409]

    login_payload = {
        "identifier": "cittadino_e2e",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401

    response_bad_token = client.get("/api/v1/auth/verify/token_finto_totalmente_123")
    assert response_bad_token.status_code in [400, 404]

    session = get_session()
    try:
        user = session.query(User).filter_by(username="cittadino_e2e").first()
        assert user is not None

        token_entry = session.query(EmailVerificationToken).filter_by(user_id=user.id).first()
        assert token_entry is not None
        real_token = token_entry.token
    finally:
        session.close()

    response = client.get(f"/api/v1/auth/verify/{real_token}")
    assert response.status_code == 200
    assert response.json["user"]["username"] == "cittadino_e2e"

    response_reuse = client.get(f"/api/v1/auth/verify/{real_token}")
    assert response_reuse.status_code in [400, 404, 410]

    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    assert response.json["user"]["username"] == "cittadino_e2e"

    # Per testare i ruoli autenticati usiamo test_client ma dobbiamo loggarci lì
    test_client.post("/api/v1/auth/login", json=login_payload)
    response_allowed = test_client.get("/api/v1/test-roles-allowed")
    assert response_allowed.status_code == 200
    assert response_allowed.json["status"] == "allowed"

    login_remember_payload = login_payload.copy()
    login_remember_payload["remember"] = True
    response_remember = client.post("/api/v1/auth/login", json=login_remember_payload)
    assert response_remember.status_code == 200

    login_with_email_payload = {
        "identifier": "cittadino@example.com",
        "password": "SecurePassword123!"
    }
    response_email_login = client.post("/api/v1/auth/login", json=login_with_email_payload)
    assert response_email_login.status_code == 200

    bad_pwd_payload = {
        "identifier": "cittadino_e2e",
        "password": "PasswordSbagliata!!!"
    }
    response_bad_pwd = client.post("/api/v1/auth/login", json=bad_pwd_payload)
    assert response_bad_pwd.status_code == 401

    ghost_payload = {
        "identifier": "non_esisto_nel_db",
        "password": "SecurePassword123!"
    }
    response_ghost = client.post("/api/v1/auth/login", json=ghost_payload)
    assert response_ghost.status_code == 401

    session = get_session()
    try:
        user_to_disable = session.query(User).filter_by(username="utente_custom_url").first()
        if user_to_disable:
            user_to_disable.is_active = False
            session.commit()
    finally:
        session.close()

    inactive_login_payload = {
        "identifier": "utente_custom_url",
        "password": "SecurePassword123!"
    }
    response_inactive = client.post("/api/v1/auth/login", json=inactive_login_payload)
    assert response_inactive.status_code == 401

    response_admin_route = client.get("/api/v1/admin/stats")
    assert response_admin_route.status_code == 403

    response_logout = client.post("/api/v1/auth/logout")
    assert response_logout.status_code in [200, 204]

    response_protected_after_logout = client.get("/api/v1/admin/stats")
    assert response_protected_after_logout.status_code == 401


@pytest.mark.e2e
def test_expired_token_handling(client, app, clean_db):
    register_payload = {
        "username": "utente_scaduto",
        "email": "scaduto@example.com",
        "first_name": "Test",
        "last_name": "Scaduto",
        "password": "SecurePassword123!"
    }
    client.post("/api/v1/auth/register", json=register_payload)

    session = get_session()
    try:
        user = session.query(User).filter_by(username="utente_scaduto").first()
        token_entry = session.query(EmailVerificationToken).filter_by(user_id=user.id).first()

        past_time = datetime.utcnow() - timedelta(days=5)
        token_entry.created_at = past_time
        if hasattr(token_entry, "expires_at"):
            token_entry.expires_at = past_time

        real_token = token_entry.token
        session.commit()
    finally:
        session.close()

    response = client.get(f"/api/v1/auth/verify/{real_token}")
    assert response.status_code in [400, 410, 422]