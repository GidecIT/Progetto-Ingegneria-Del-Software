import os
import pytest

from participium import create_app
from participium.database import create_all, get_session, open_connection, close_connection
from participium.models.user import User
from participium.models.token import EmailVerificationToken
from participium.models.category import Category
from participium.models.report import Report, ReportStatusHistory, ReportFollower, ReportPhoto
from participium.models.message import Message
from participium.models.notification import Notification

@pytest.fixture(scope="session")
def app():
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    os.environ["TESTING"] = "True"
    os.environ["WTF_CSRF_ENABLED"] = "False"
    os.environ["SECRET_KEY"] = "e2e_secret_key_super_secure"

    open_connection()

    app = create_app()

    with app.app_context():
        create_all()
        yield app

    close_connection()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def clean_db(app):
    session = get_session()
    try:
        session.query(Message).delete()
        session.query(Notification).delete()
        session.query(ReportFollower).delete()
        session.query(ReportStatusHistory).delete()
        session.query(ReportPhoto).delete()
        session.query(Report).delete()
        session.query(Category).delete()
        session.query(EmailVerificationToken).delete()
        session.query(User).delete()
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()