import pytest
from participium.database import open_connection, create_all, get_session, close_connection
from participium.models.category import Category
from participium.models.report import Report
from participium.models.user import User
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.message_repository import MessageRepository
from participium.repositories.notification_repository import NotificationRepository
from participium.repositories.report_repository import ReportRepository
from participium.repositories.user_repository import UserRepository
from participium.repositories.token_repository import TokenRepository
from participium.models.enums import NotificationType, Role
from participium.models.notification import Notification
from participium.models.enums import ReportStatus
from participium.models.token import EmailVerificationToken
from datetime import datetime, timedelta
from sqlalchemy import update



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
    """Alias di db_session per i test legacy/blackbox che cercano 'session'."""
    return db_session

# ENTITY FIXTURES 

@pytest.fixture
def test_user(db_session):
    user = User(id= 1, username="tester", email="test@ex.com", first_name="T", last_name="T", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_operator(db_session, test_category):
    user = User(username="operator", email="op@ex.com", first_name="O", last_name="P", password_hash="hash", role=Role.OPERATOR, category_id=test_category.id)
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_user(db_session):
    user = User(username="admin", email="admin@ex.com", first_name="A", last_name="A", password_hash="hash",role=Role.ADMIN  )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def other_user(db_session):
    user = User(username="other", email="other@ex.com", first_name="O", last_name="O", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_category(db_session):
    cat = Category(name="Others", is_active=True)
    db_session.add(cat)
    db_session.commit()
    return cat

@pytest.fixture
def other_category(db_session):
    from participium.models.category import Category
    cat = Category(name="Viabilità", is_active=True)
    db_session.add(cat)
    db_session.commit()
    return cat

@pytest.fixture
def test_report(db_session, test_user, test_category):
    report = Report(
        title="Buca profonda", description="Buca in Piazza Castello", 
        latitude=45.4, longitude=7.41, 
        reporter_id=test_user.id, category_id=test_category.id
    )
    db_session.add(report)
    db_session.commit()
    return report


# REPOSITORY FIXTURES

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
def make_notification():
    def _maker(user_id: int, **kwargs) -> Notification:
        defaults = dict(
            type=NotificationType.SYSTEM,
            title="Titolo",
            body="Body",
            is_read=False
        )
        defaults.update(kwargs)
        return Notification(user_id=user_id, **defaults)
    return _maker

@pytest.fixture
def make_report():
    def _maker(user_id: int, category_id: int, **kwargs) -> Report:
        defaults = dict(
            title="Buca",
            description="Buca profonda",
            latitude=45.0,
            longitude=7.0,
            status=ReportStatus.PENDING_APPROVAL,
        )
        defaults.update(kwargs)
        return Report(reporter_id=user_id, category_id=category_id, **defaults)
    return _maker

@pytest.fixture
def make_token():
    """Fixture factory per generare token puliti con valori di default."""
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

