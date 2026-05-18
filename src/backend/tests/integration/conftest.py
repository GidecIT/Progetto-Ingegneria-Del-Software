import pytest
from participium.database import open_connection, create_all, get_session, close_connection
from participium.models.category import Category
from participium.models.report import Report
from participium.models.user import User
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.message_repository import MessageRepository
from participium.repositories.notification_repository import NotificationRepository

@pytest.fixture(scope="function")
def db_session(monkeypatch):

    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")

    open_connection()
    create_all()
    session = get_session()
    yield session

    session.close()
    close_connection()

# ENTITY FIXTURES 

@pytest.fixture
def test_user(db_session):
    user = User(username="tester", email="test@ex.com", first_name="T", last_name="T", password_hash="hash")
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