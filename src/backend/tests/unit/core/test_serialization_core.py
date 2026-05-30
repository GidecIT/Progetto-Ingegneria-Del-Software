from __future__ import annotations

import pytest
from datetime import datetime
from unittest.mock import Mock
from participium.core.serialization import (
    serialize_user, 
    serialize_category,
    serialize_notification,
    serialize_report_summary,
    serialize_report_detail,
    serialize_photo,
    _serialize_reporter, 
    _serialize_party, 
    _media_url
)
from participium.models.enums import Role, ReportStatus, NotificationType

pytestmark = pytest.mark.unit

@pytest.fixture
def mock_cat():
    cat = Mock()
    cat.id = 10
    cat.name = "Illuminazione Pubblica"
    cat.is_active = True
    cat.created_at = datetime(2024, 1, 1, 10, 0, 0)
    return cat

@pytest.fixture
def mock_user(mock_cat):
    user = Mock()
    user.id = 1
    user.username = "mrossi"
    user.first_name = "Mario"
    user.last_name = "Rossi"
    user.email = "mario.rossi@example.com"
    user.role = Role.CITIZEN
    user.category_id = 10
    user.category = mock_cat
    user.is_active = True
    user.is_email_verified = True
    user.email_notifications_enabled = True
    user.profile_picture_path = "avatar.png"
    user.created_at = datetime(2024, 1, 1, 12, 0, 0)
    return user

@pytest.fixture
def mock_photo():
    p = Mock()
    p.id = 100
    p.file_path = "segnalazione.jpg"
    p.original_filename = "foto.jpg"
    p.content_type = "image/jpeg"
    return p

@pytest.fixture
def mock_report(mock_user, mock_cat, mock_photo):
    r = Mock()
    r.id = 42
    r.title = "Buca in piazza"
    r.description = "Buca profonda in piazza Castello"
    r.category = mock_cat
    r.status = ReportStatus.PENDING_APPROVAL
    r.rejection_reason = None
    r.is_anonymous = False
    r.reporter = mock_user
    r.reporter_id = mock_user.id
    r.category_id = mock_cat.id
    r.latitude = 45.0
    r.longitude = 9.0
    r.photos = [mock_photo]
    r.followers = []
    r.messages = []
    r.status_history = []
    r.created_at = datetime(2024, 1, 2, 9, 0, 0)
    r.updated_at = datetime(2024, 1, 2, 10, 0, 0)
    return r

def test_media_url_logic():
    assert _media_url(None) is None
    assert _media_url("") is None
    assert _media_url("foto.jpg") == "/static/uploads/foto.jpg"

def test_party_deleted():
    assert _serialize_party(None) == {"id": None, "display_name": "Deleted User", "role": None}

def test_party_valid(mock_user):
    res = _serialize_party(mock_user)
    assert res == {"id": 1, "display_name": "Mario Rossi", "role": "citizen"}

def test_party_no_names():
    u = Mock(id=2, username="gianni", first_name="", last_name="", role=Role.ADMIN)
    assert _serialize_party(u)["display_name"] == "gianni"

def test_serialize_category(mock_cat):
    res = serialize_category(mock_cat)
    assert res["id"] == 10
    assert res["name"] == "Illuminazione Pubblica"
    assert res["created_at"] == "2024-01-01T10:00:00"

def test_serialize_category_no_date():
    cat = Mock(id=1, name="Verde Pubblico", is_active=True, created_at=None)
    assert serialize_category(cat)["created_at"] is None

def test_serialize_notification():
    n = Mock()
    n.id = 7; n.type = NotificationType.SYSTEM; n.title = "Titolo"; n.body = "Messaggio"
    n.report_id = 42; n.is_read = False; n.created_at = datetime(2024, 1, 1)
    res = serialize_notification(n)
    assert res["id"] == 7
    assert res["created_at"] == "2024-01-01T00:00:00"

def test_serialize_notification_no_date():
    n = Mock(id=1, type=NotificationType.SYSTEM, title="T", body="B",
             report_id=None, is_read=True, created_at=None)
    assert serialize_notification(n)["created_at"] is None

def test_user_full(mock_user):
    res = serialize_user(mock_user)
    assert res["id"] == 1
    assert res["category"]["name"] == "Illuminazione Pubblica"
    assert res["profile_picture_url"] == "/static/uploads/avatar.png"
    assert res["created_at"] == "2024-01-01T12:00:00"

def test_user_minimal():
    u = Mock(
        id=5, username="min", first_name="A", last_name="B",
        email="m@e.com", role=Role.CITIZEN, category_id=None,
        category=None, is_active=True, is_email_verified=False,
        email_notifications_enabled=True, profile_picture_path=None,
        created_at=None
    )
    res = serialize_user(u)
    assert res["id"] == 5
    assert res["category"] is None
    assert res["profile_picture_url"] is None
    assert res["created_at"] is None

def test_serialize_photo(mock_photo):
    res = serialize_photo(mock_photo)
    assert res["id"] == 100
    assert res["url"] == "/static/uploads/segnalazione.jpg"

def test_report_summary_basic(mock_report):
    res = serialize_report_summary(mock_report)
    assert res["id"] == 42
    assert res["title"] == "Buca in piazza"
    assert res["is_public"] is False
    assert res["followers_count"] == 0

def test_report_summary_public(mock_report):
    mock_report.status = ReportStatus.ASSIGNED
    res = serialize_report_summary(mock_report)
    assert res["is_public"] is True

def test_report_summary_follower(mock_report, mock_user):
    f = Mock()
    f.user_id = mock_user.id
    mock_report.followers = [f]
    res = serialize_report_summary(mock_report, viewer=mock_user)
    assert res["followers_count"] == 1
    assert res["is_followed_by_current_user"] is True

def test_report_summary_no_viewer_follower(mock_report):
    f = Mock(user_id=1)
    mock_report.followers = [f]
    res = serialize_report_summary(mock_report, viewer=None)
    assert res["is_followed_by_current_user"] is False

def test_report_detail_full(mock_report):
    h1 = Mock()
    h1.id = 1; h1.previous_status = None; h1.new_status = ReportStatus.PENDING_APPROVAL
    h1.note = "Inviata"; h1.changed_by = None; h1.created_at = datetime(2024, 1, 2, 9, 0, 0)
    h2 = Mock()
    h2.id = 2; h2.previous_status = ReportStatus.PENDING_APPROVAL; h2.new_status = ReportStatus.ASSIGNED
    h2.note = "Assegnata"; h2.changed_by = None; h2.created_at = datetime(2024, 1, 2, 9, 30, 0)
    mock_report.status_history = [h2, h1]
    mock_report.messages = [Mock(id=500, created_at=datetime(2024, 1, 2, 9, 10, 0), sender=None, recipient=None, body="Ciao", report_id=42)]
    res = serialize_report_detail(mock_report, include_messages=True)
    assert res["status_history"][0]["id"] == 1
    assert res["status_history"][1]["id"] == 2
    assert len(res["messages"]) == 1
    assert res["can_access_messages"] is True

def test_report_detail_minimal(mock_report):
    mock_report.created_at = None
    mock_report.updated_at = None
    res = serialize_report_detail(mock_report, include_messages=False)
    assert "messages" not in res
    assert res["can_access_messages"] is False

def test_reporter_deleted(mock_report):
    mock_report.reporter = None
    assert _serialize_reporter(mock_report) == {"display_name": "Deleted Citizen", "id": None}

def test_reporter_public_anon(mock_report):
    mock_report.is_anonymous = True
    res = _serialize_reporter(mock_report, viewer=None)
    assert res == {"display_name": "Anonymous Citizen", "id": None}

def test_reporter_self_anon(mock_report, mock_user):
    mock_report.is_anonymous = True
    assert _serialize_reporter(mock_report, viewer=mock_user)["id"] == 1

def test_reporter_admin_anon(mock_report):
    mock_report.is_anonymous = True
    v = Mock(id=9, role=Role.ADMIN)
    assert _serialize_reporter(mock_report, viewer=v)["id"] == 1

def test_reporter_op_same_cat_anon(mock_report):
    mock_report.is_anonymous = True
    v = Mock(id=8, role=Role.OPERATOR, category_id=10)
    assert _serialize_reporter(mock_report, viewer=v)["id"] == 1

def test_reporter_op_diff_cat_anon(mock_report):
    mock_report.is_anonymous = True
    v = Mock(id=7, role=Role.OPERATOR, category_id=11)
    assert _serialize_reporter(mock_report, viewer=v)["id"] is None

def test_reporter_other_citizen_anon(mock_report):
    mock_report.is_anonymous = True
    v = Mock(id=6, role=Role.CITIZEN)
    assert _serialize_reporter(mock_report, viewer=v)["id"] is None
