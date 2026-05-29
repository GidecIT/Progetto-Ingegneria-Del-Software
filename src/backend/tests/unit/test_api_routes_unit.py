import io
import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, g
from participium.routes.api import api_bp
from participium.models.enums import Role, ReportStatus
from participium.core.exceptions import ValidationError


@pytest.fixture
def app(mock_user):
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    app.config["TESTING"] = True
    app.config["SETTINGS"] = MagicMock(expose_verification_links=True)
    
    @app.before_request
    def set_user():
        g.current_user = mock_user

    # Register error handler for generic errors (if any in tests)
    @app.errorhandler(Exception)
    def handle_exception(e):
        return {"error": str(e)}, getattr(e, 'code', 500)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch("participium.routes.api.get_controllers") as mock_get, \
         patch("participium.routes.api.serialize_user", return_value={"id": 1}) as m_su, \
         patch("participium.routes.api.serialize_category", return_value={"id": 1}) as m_sc, \
         patch("participium.routes.api.serialize_report_summary", return_value={"id": 1}) as m_srs, \
         patch("participium.routes.api.serialize_report_detail", return_value={"id": 1}) as m_srd, \
         patch("participium.routes.api.serialize_message", return_value={"id": 1}) as m_sm, \
         patch("participium.routes.api.serialize_notification", return_value={"id": 1}) as m_sn, \
         patch("participium.routes.api.login_user"), \
         patch("participium.routes.api.logout_user"):
        
        controllers = MagicMock()
        mock_get.return_value = controllers
        yield controllers


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_reference_data_api(client):
    response = client.get("/api/v1/meta/reference-data")
    assert response.status_code == 200
    assert "roles" in response.json

def test_register_user_api(client, app, mock_dependencies):
    mock_dependencies.auth.register.return_value = (MagicMock(), "http://verify")
    # with expose_verification_links = True
    response = client.post("/api/v1/auth/register", json={"email": "test@test.com"})
    assert response.status_code == 201
    
    # with expose_verification_links = False
    app.config["SETTINGS"].expose_verification_links = False
    response = client.post("/api/v1/auth/register", json={"email": "test@test.com"})
    assert response.status_code == 201

def test_verify_email_api(client, mock_dependencies):
    mock_dependencies.auth.verify_email.return_value = MagicMock()
    response = client.get("/api/v1/auth/verify/token123")
    assert response.status_code == 200

def test_login_api(client, mock_dependencies):
    mock_dependencies.auth.login.return_value = MagicMock()
    response = client.post("/api/v1/auth/login", json={"identifier": "x", "password": "y"})
    assert response.status_code == 200

def test_logout_api(client):
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200

def test_list_categories_api(client, mock_dependencies):
    mock_dependencies.admin.list_categories.return_value = [MagicMock()]
    response = client.get("/api/v1/categories")
    assert response.status_code == 200

def test_list_reports_api_filters(client, mock_dependencies):
    mock_dependencies.reports.list_public_reports.return_value = [MagicMock()]
    response = client.get("/api/v1/reports?status=Pending Approval&category_id=1&date_from=2023-01-01&date_to=2023-12-31")
    assert response.status_code == 200

def test_create_report_api(client, mock_dependencies):
    mock_dependencies.reports.create_report.return_value = MagicMock()
    data = {
        "title": "T", "description": "D", "category_id": 1, 
        "latitude": 10.0, "longitude": 20.0, "is_anonymous": "true",
        "photos": (io.BytesIO(b"my file contents"), "test.jpg")
    }
    response = client.post("/api/v1/reports", data=data, content_type='multipart/form-data')
    assert response.status_code == 201

def test_export_reports_api(client, mock_dependencies):
    mock_dependencies.reports.export_rows.return_value = [{"id": 1, "title": "A"}]
    with patch("participium.routes.api.build_csv", return_value="a,b\n1,2"):
        response = client.get("/api/v1/reports/export")
        assert response.status_code == 200

def test_report_detail_api(client, mock_dependencies):
    mock_context = MagicMock()
    mock_context.report = MagicMock()
    mock_context.can_access_messages = True
    mock_dependencies.reports.build_detail_context.return_value = mock_context
    response = client.get("/api/v1/reports/1")
    assert response.status_code == 200

def test_follow_report_api(client, mock_dependencies):
    mock_dependencies.reports.follow_report.return_value = MagicMock()
    response = client.post("/api/v1/reports/1/follow")
    assert response.status_code == 200

def test_unfollow_report_api(client, mock_dependencies):
    mock_dependencies.reports.unfollow_report.return_value = MagicMock()
    response = client.delete("/api/v1/reports/1/follow")
    assert response.status_code == 200

def test_list_messages_api(client, mock_dependencies):
    mock_dependencies.reports.list_messages.return_value = [MagicMock()]
    mock_context = MagicMock()
    mock_dependencies.reports.build_detail_context.return_value = mock_context
    response = client.get("/api/v1/reports/1/messages")
    assert response.status_code == 200

def test_send_message_api(client, mock_dependencies):
    mock_dependencies.reports.send_message.return_value = MagicMock()
    mock_context = MagicMock()
    mock_dependencies.reports.build_detail_context.return_value = mock_context
    response = client.post("/api/v1/reports/1/messages", json={"body": "Hello"})
    assert response.status_code == 201

def test_public_stats_api(client, mock_dependencies):
    mock_dependencies.statistics.public_statistics.return_value = {}
    response = client.get("/api/v1/stats/public?granularity=month")
    assert response.status_code == 200

def test_me_api(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200

def test_update_me_api(client, mock_dependencies):
    mock_dependencies.users.update_profile.return_value = MagicMock()
    
    # json payload
    response = client.put("/api/v1/users/me", json={"email_notifications_enabled": True, "username": "test", "first_name": "A", "last_name": "B"})
    assert response.status_code == 200
    
    # form data
    data = {"email_notifications_enabled": "true", "username": "test"}
    response = client.put("/api/v1/users/me", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    
    # no email_notifications_enabled payload
    response = client.put("/api/v1/users/me", json={"username": "test"})
    assert response.status_code == 200

def test_delete_me_api(client, mock_dependencies):
    response = client.delete("/api/v1/users/me")
    assert response.status_code == 200

def test_my_reports_api(client, mock_dependencies):
    mock_dependencies.reports.list_user_reports.return_value = [MagicMock()]
    response = client.get("/api/v1/users/me/reports")
    assert response.status_code == 200

def test_my_notifications_api(client, mock_dependencies):
    mock_dependencies.users.list_notifications.return_value = [MagicMock()]
    response = client.get("/api/v1/users/me/notifications")
    assert response.status_code == 200

def test_mark_notification_read_api(client, mock_dependencies):
    mock_dependencies.users.mark_notification_as_read.return_value = MagicMock()
    mock_dependencies.users.get_notification_for_user.return_value = MagicMock()
    response = client.post("/api/v1/users/me/notifications/1/read")
    assert response.status_code == 200

def test_pending_reports_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_context = MagicMock()
    mock_context.pending_reports = [MagicMock()]
    mock_dependencies.operators.build_dashboard.return_value = mock_context
    response = client.get("/api/v1/operator/reports/pending")
    assert response.status_code == 200

def test_assigned_reports_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_context = MagicMock()
    mock_context.assigned_reports = [MagicMock()]
    mock_context.unread_message_counts = {1: 2}
    mock_dependencies.operators.build_dashboard.return_value = mock_context
    response = client.get("/api/v1/operator/reports/assigned")
    assert response.status_code == 200

def test_assign_report_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.operators.assign_report.return_value = MagicMock()
    response = client.post("/api/v1/operator/reports/1/assign")
    assert response.status_code == 200

def test_update_report_status_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.operators.update_status.return_value = MagicMock()
    response = client.post("/api/v1/operator/reports/1/status", json={"status": "In Progress", "note": "OK"})
    assert response.status_code == 200

def test_admin_users_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.list_users.return_value = [MagicMock()]
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 200

def test_create_admin_user_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.create_user.return_value = MagicMock()
    response = client.post("/api/v1/admin/users", json={"email": "admin@test.com"})
    assert response.status_code == 201

def test_update_admin_user_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.update_user.return_value = MagicMock()
    response = client.put("/api/v1/admin/users/1", json={"is_active": True, "email_notifications_enabled": False})
    assert response.status_code == 200
    
    # test without boolean fields
    response = client.put("/api/v1/admin/users/1", json={"username": "test"})
    assert response.status_code == 200

def test_admin_categories_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.list_categories.return_value = [MagicMock()]
    response = client.get("/api/v1/admin/categories")
    assert response.status_code == 200

def test_create_category_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.create_category.return_value = MagicMock()
    response = client.post("/api/v1/admin/categories", json={"name": "New Cat"})
    assert response.status_code == 201

def test_update_category_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.update_category.return_value = MagicMock()
    response = client.put("/api/v1/admin/categories/1", json={"is_active": True})
    assert response.status_code == 200
    
    response = client.put("/api/v1/admin/categories/1", json={"name": "test"})
    assert response.status_code == 200

def test_admin_stats_api(client, mock_dependencies, mock_user):
    mock_user.role = Role.ADMIN
    mock_dependencies.admin.admin_statistics.return_value = {}
    response = client.get("/api/v1/admin/stats")
    assert response.status_code == 200
