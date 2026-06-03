import io
import pytest
from participium.models.user import User
from participium.models.category import Category
from participium.models.report import Report
from participium.models.message import Message
from participium.models.notification import Notification
from participium.database import get_session
from participium.models.enums import Role, ReportStatus, NotificationType

@pytest.fixture
def test_users(clean_db):
    db = get_session()
    admin = User(username="admin", email="admin@test.com", password_hash="hash", first_name="A", last_name="A", role=Role.ADMIN.value, is_active=True)
    oper = User(username="oper", email="oper@test.com", password_hash="hash", first_name="O", last_name="O", role=Role.OPERATOR.value, is_active=True)
    cit = User(username="cit", email="cit@test.com", password_hash="hash", first_name="C", last_name="C", role=Role.CITIZEN.value, is_active=True)
    db.add_all([admin, oper, cit])
    db.commit()
    users = {"admin": admin.id, "oper": oper.id, "cit": cit.id}
    db.close()
    return users

@pytest.fixture
def auth_client(client, test_users):
    def _auth(role):
        with client.session_transaction() as sess:
            sess["user_id"] = test_users[role]
        return client
    return _auth

@pytest.fixture
def test_category(clean_db):
    db = get_session()
    cat = Category(name="Test Cat", is_active=True)
    db.add(cat)
    db.commit()
    cat_id = cat.id
    db.close()
    return cat_id

@pytest.fixture
def test_report(clean_db, test_category, test_users):
    db = get_session()
    rep = Report(
        title="Test Report",
        description="D",
        latitude=10.0,
        longitude=20.0,
        reporter_id=test_users["cit"],
        category_id=test_category,
        status=ReportStatus.PENDING_APPROVAL.value,
        is_anonymous=False
    )
    db.add(rep)
    db.commit()
    rep_id = rep.id
    db.close()
    return rep_id

def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_reference_data(client):
    response = client.get("/api/v1/meta/reference-data")
    assert response.status_code == 200

def test_categories(client, test_category):
    response = client.get("/api/v1/categories")
    assert response.status_code == 200

def test_reports_public(client, test_report):
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    

    response = client.get("/api/v1/reports?status=Pending Approval")
    assert response.status_code == 200
    

    response = client.get("/api/v1/reports?status=Invalid")
    assert response.status_code == 400
    

    response = client.get("/api/v1/reports/export")
    assert response.status_code == 200

def test_create_report(auth_client, test_category):
    client = auth_client("cit")
    data = {
        "title": "T", "description": "D", "category_id": test_category,
        "latitude": 10.0, "longitude": 20.0
    }
    response = client.post("/api/v1/reports", data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    
    data = {
        "title": "T", "description": "D", "category_id": test_category,
        "latitude": 10.0, "longitude": 20.0, "is_anonymous": "false",
        "photos": (io.BytesIO(b"my file contents"), "test.jpg")
    }
    response = client.post("/api/v1/reports", data=data, content_type='multipart/form-data')
    assert response.status_code == 201

def test_report_detail(auth_client, test_report):
    client = auth_client("cit")
    response = client.get(f"/api/v1/reports/{test_report}")
    assert response.status_code == 200

def test_report_follow_unfollow(auth_client, test_report, test_users):
    db = get_session()
    report = db.query(Report).get(test_report)
    report.status = ReportStatus.ASSIGNED.value
    db.commit()
    db.close()
    
    client = auth_client("admin")

    db = get_session()
    cit2 = User(username="cit2", email="cit2@test.com", password_hash="hash", first_name="C", last_name="C", role=Role.CITIZEN.value, is_active=True)
    db.add(cit2)
    db.commit()
    cit2_id = cit2.id
    db.close()
    
    with client.session_transaction() as sess:
        sess["user_id"] = cit2_id
    
    response = client.post(f"/api/v1/reports/{test_report}/follow")
    assert response.status_code == 200
    response = client.delete(f"/api/v1/reports/{test_report}/follow")
    assert response.status_code == 200

def test_report_messages(auth_client, test_report, test_users, test_category):
    db = get_session()
    oper = db.query(User).get(test_users["oper"])
    oper.category_id = test_category
    db.commit()
    db.close()
    
    client = auth_client("oper")
    response = client.post(f"/api/v1/operator/reports/{test_report}/assign")
    assert response.status_code == 200
    
    client = auth_client("cit")
    response = client.post(f"/api/v1/reports/{test_report}/messages", json={"body": "Hello"})
    print("message error:", response.json)
    assert response.status_code == 201
    
    response = client.get(f"/api/v1/reports/{test_report}/messages")
    assert response.status_code == 200

def test_public_stats(client):
    response = client.get("/api/v1/stats/public?granularity=month")
    assert response.status_code == 200

def test_me_api(auth_client):
    client = auth_client("cit")
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    
    response = client.put("/api/v1/users/me", json={"username": "newname"})
    assert response.status_code == 200
    
    response = client.put("/api/v1/users/me", data={"username": "newname2", "email_notifications_enabled": "true"})
    assert response.status_code == 200
    
    response = client.put("/api/v1/users/me", json={"email_notifications_enabled": False})
    assert response.status_code == 200
    
    response = client.get("/api/v1/users/me/reports")
    assert response.status_code == 200
    
    response = client.get("/api/v1/users/me/notifications")
    assert response.status_code == 200

def test_mark_notification_read(auth_client, test_users):
    cit_id = test_users["cit"]
    db = get_session()
    notif = Notification(user_id=cit_id, type=NotificationType.SYSTEM.value, title="A", body="B", is_read=False)
    db.add(notif)
    db.commit()
    n_id = notif.id
    db.close()
    
    client = auth_client("cit")
    response = client.post(f"/api/v1/users/me/notifications/{n_id}/read")
    assert response.status_code == 200

def test_delete_me(auth_client):
    client = auth_client("cit")
    response = client.delete("/api/v1/users/me")
    assert response.status_code == 200

def test_operator_reports(auth_client, test_report, test_users, test_category):
    db = get_session()
    oper = db.query(User).get(test_users["oper"])
    oper.category_id = test_category
    db.commit()
    db.close()
    
    client = auth_client("oper")
    response = client.get("/api/v1/operator/reports/pending")
    assert response.status_code == 200
    
    response = client.get("/api/v1/operator/reports/assigned")
    assert response.status_code == 200
    
    response = client.post(f"/api/v1/operator/reports/{test_report}/assign")
    print("assign error:", response.json)
    assert response.status_code == 200
    
    response = client.post(f"/api/v1/operator/reports/{test_report}/status", json={"status": "In Progress"})
    assert response.status_code == 200

def test_admin_users(auth_client, test_category):
    client = auth_client("admin")
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 200
    
    response = client.post("/api/v1/admin/users", json={"username": "newadmin", "email": "newadmin@test.com", "first_name": "A", "last_name": "B", "role": "operator", "password": "password123", "category_id": test_category})
    assert response.status_code == 201
    
    response = client.put(f"/api/v1/admin/users/{response.json['id']}", json={"is_active": False})
    assert response.status_code == 200

def test_admin_categories(auth_client, test_category):
    client = auth_client("admin")
    response = client.get("/api/v1/admin/categories")
    assert response.status_code == 200
    
    response = client.post("/api/v1/admin/categories", json={"name": "New Cat 2"})
    assert response.status_code == 201
    
    response = client.put(f"/api/v1/admin/categories/{test_category}", json={"is_active": False})
    assert response.status_code == 200
    
    response = client.put(f"/api/v1/admin/categories/{test_category}", json={"name": "New Cat 2 Updated"})
    assert response.status_code == 200

def test_admin_stats(auth_client):
    client = auth_client("admin")
    response = client.get("/api/v1/admin/stats")
    assert response.status_code == 200
