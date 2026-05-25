import os
import pytest
from participium import create_app
from participium.database import create_all, get_session, open_connection, close_connection

@pytest.fixture(scope="session")
def app():
    """Crea e configura un'istanza dell'applicazione reale per l'intera sessione E2E."""

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
    """Fornisce un client HTTP per inviare richieste reali all'applicazione."""
    return app.test_client()


@pytest.fixture
def clean_db(app):
    """Svuota i dati da tutte le tabelle tra un test e l'altro usando la sessione reale."""
    session = get_session()
    try:
        from participium.models.user import User
        from participium.models.token import EmailVerificationToken

        session.query(EmailVerificationToken).delete()
        session.query(User).delete()
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()