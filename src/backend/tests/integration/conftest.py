# tests/integration/conftest.py
from unittest.mock import Mock

import pytest
from participium.database import open_connection, create_all, get_session, close_connection
from participium.models.category import Category
from participium.models.report import Report
from participium.models.user import User
from participium.models.enums import Role
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.report_repository import ReportRepository
from participium.services.report_service import ReportService
from participium.services.category_service import CategoryService

@pytest.fixture(scope="function")
def db_session(monkeypatch):
    """Configura un database SQLite in memoria pulito per ogni singolo test."""
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    
    open_connection()
    create_all()
    session = get_session()
    
    yield session
    
    session.close()
    close_connection()

# --- FIXTURES DELLE ENTITÀ (DATI REALI NEL DB) ---

@pytest.fixture
def test_user(db_session):
    """Crea e persiste un utente reale nel database di integrazione."""
    user = User(
        username="tester_integration", 
        email="test@example.com", 
        first_name="Mario", 
        last_name="Rossi", 
        password_hash="hashed_password",
        role=Role.CITIZEN,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_category(db_session):
    """Crea e persiste una categoria reale nel database di integrazione."""
    cat = Category(name="Strade e Marciapiedi", is_active=True)
    db_session.add(cat)
    db_session.commit()
    return cat

@pytest.fixture
def test_report(db_session, test_user, test_category):
    """Crea e persiste un report reale, agganciato a utente e categoria reali."""
    from participium.models.enums import ReportStatus
    report = Report(
        title="Buca profonda", 
        description="Buca pericolosa in Piazza Castello", 
        latitude=45.4642, 
        longitude=9.1900, 
        status=ReportStatus.RESOLVED,  # Lo impostiamo pubblico per default nei test felici
        reporter_id=test_user.id, 
        category_id=test_category.id
    )
    db_session.add(report)
    db_session.commit()
    return report

# --- FIXTURES DEI SERVIZI (CHE USANO REPO REALI) ---

@pytest.fixture
def integration_report_service(db_session):
    """Fornisce il ReportService configurato con database e repository reali 
    e mock per i servizi non impattati dal flusso."""
    
    report_repo = ReportRepository(db_session)
    category_repo = CategoryRepository(db_session) # Reale, serve per completare l'init
    
    # Servizi esterni non impattati da follow/unfollow, passiamo dei Mock
    mock_storage = Mock()
    mock_notification = Mock()

    return ReportService(
        session=db_session,
        report_repository=report_repo,
        category_repository=category_repo,
        storage_service=mock_storage,
        notification_service=mock_notification
    )

@pytest.fixture
def integration_category_service(db_session):
    """Fornisce il CategoryService configurato con database e repository reali."""
    repository = CategoryRepository(db_session)
    return CategoryService(session=db_session, category_repository=repository)
