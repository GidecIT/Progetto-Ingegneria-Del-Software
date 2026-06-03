import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock
from flask import Flask
from sqlalchemy import update

from participium.database import open_connection, create_all, get_session, close_connection
from participium.core.security import hash_password
from participium.models.category import Category
from participium.models.report import Report
from participium.models.user import User
from participium.models.notification import Notification
from participium.models.token import EmailVerificationToken
from participium.models.enums import NotificationType, Role, ReportStatus
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.message_repository import MessageRepository
from participium.repositories.notification_repository import NotificationRepository
from participium.repositories.report_repository import ReportRepository
from participium.repositories.user_repository import UserRepository
from participium.repositories.token_repository import TokenRepository

@pytest.fixture(scope="function")
def db_session(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    open_connection()
    create_all()
    session = get_session()
    yield session
    session.close()
    close_connection()

@pytest.fixture
def session(db_session):
    return db_session

@pytest.fixture
def test_user(db_session):
    user = User(
        username="tester",
        email="test@ex.com",
        first_name="Mario",
        last_name="Rossi",
        password_hash=hash_password("password_di_test"),
        role=Role.CITIZEN,
        is_active=True,
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_operator(db_session, test_category):
    user = User(
        username="operator_test",
        email="operator@ex.com",
        first_name="Franco",
        last_name="Franchi",
        password_hash=hash_password("password_di_test"),
        role=Role.OPERATOR,
        category_id=test_category.id, 
        is_active=True,
        is_email_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_user(db_session):
    user = User(
        username="admin", 
        email="admin@ex.com", 
        first_name="A", 
        last_name="A", 
        password_hash=hash_password("hash"),
        role=Role.ADMIN  
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def other_user(db_session):
    user = User(
        username="other", 
        email="other@ex.com", 
        first_name="O", 
        last_name="O", 
        password_hash=hash_password("hash")
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_category(db_session):
    category = Category(name="Verde Pubblico", is_active=True)
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def other_category(db_session):
    category = Category(name="Illuminazione", is_active=True)
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def test_report(db_session, test_user, test_category):
    report = Report(
        title="Buca profonda", 
        description="Buca in Piazza Castello", 
        latitude=45.4, 
        longitude=7.41, 
        reporter_id=test_user.id, 
        category_id=test_category.id,
        status=ReportStatus.PENDING_APPROVAL
    )
    db_session.add(report)
    db_session.commit()
    return report

@pytest.fixture
def category_repository(db_session):
    return CategoryRepository(db_session)

@pytest.fixture
def message_repository(db_session):
    return MessageRepository(db_session)

@pytest.fixture
def notification_repository(db_session):
    return NotificationRepository(db_session)

@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)

@pytest.fixture
def token_repository(db_session):
    return TokenRepository(db_session)

@pytest.fixture
def report_repository(db_session):
    return ReportRepository(db_session)

@pytest.fixture
def make_notification(db_session):
    def _maker(user_id: int, **kwargs) -> Notification:
        defaults = {
            "title": "Notifica di Test",
            "body": "Corpo della notifica",
            "type": NotificationType.SYSTEM,
            "is_read": False,
        }
        defaults.update(kwargs)
        notification = Notification(user_id=user_id, **defaults)
        db_session.add(notification)
        db_session.flush()
        return notification
    return _maker

@pytest.fixture
def make_report(db_session):
    def _maker(reporter_id: int, category_id: int, **kwargs) -> Report:
        defaults = {
            "title": "Segnalazione di Test",
            "description": "Descrizione di test",
            "latitude": 41.9028,
            "longitude": 12.4964,
            "status": ReportStatus.PENDING_APPROVAL,
            "is_anonymous": False,
        }
        defaults.update(kwargs)
        report = Report(reporter_id=reporter_id, category_id=category_id, **defaults)
        db_session.add(report)
        db_session.flush()
        return report
    return _maker

@pytest.fixture
def make_token():
    def _maker(
        user_id: int,
        *,
        token: str = "token1",
        is_used: bool = False,
        expires_at: datetime | None = None,
    ) -> EmailVerificationToken:
        return EmailVerificationToken(
            user_id=user_id,
            token=token,
            is_used=is_used,
            expires_at=expires_at or datetime.now() + timedelta(hours=24),
        )
    return _maker

@pytest.fixture
def backdate():
    def _helper(session, model_class, entity_id: int, days: int = 0, seconds: int = 0) -> None:
        delta = timedelta(days=days, seconds=seconds)
        session.execute(
            update(model_class)
            .where(model_class.id == entity_id)
            .values(created_at=datetime.utcnow() - delta)
        )
        session.commit()
    return _helper

@pytest.fixture
def flask_app():
    app = Flask("test_auth_core_app")
    app.secret_key = "super_secret_key_for_testing"
    return app

@pytest.fixture
def mock_citizen_user():
    user = Mock()
    user.id = 1
    user.role = Role.CITIZEN
    return user

@pytest.fixture
def mock_admin_user():
    user = Mock()
    user.id = 3
    user.role = Role.ADMIN
    return user