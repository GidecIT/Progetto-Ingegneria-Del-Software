from participium.services.storage_service import LocalFileStorageService, StorageService
from participium.services.notification_service import NotificationService
from participium.services.category_service import CategoryService
from participium.services.messaging_service import MessagingService
from participium.services.statistics_service import StatisticsService
from participium.services.user_service import UserService
from participium.models.enums import NotificationType, ReportStatus, Role
import pytest
from unittest.mock import Mock

from participium.services.report_service import ReportService 


@pytest.fixture
def report_service_with_active_category(report_service):
    """Configura una categoria attiva nel category_repository."""
    category = Mock(id=1, is_active=True)
    report_service.category_repository.get_by_id.return_value = category
    return report_service

@pytest.fixture
def report_service():
    """
    Fornisce l'istanza del servizio ReportService
    """    

    service =  ReportService(
        session=Mock(),
        report_repository=Mock(),
        category_repository=Mock(),
        storage_service=Mock(),
        notification_service=Mock()
    )
    

    return service


@pytest.fixture
def mock_category():
    """Fornisce un mock standard di una categoria"""
    category = Mock()

    category.id = 1
    category.name = "Water"
    category.is_active = True

    return category

@pytest.fixture
def mock_notification(mock_user, mock_report):
    """fornisce un mock standard per notification"""
    notification = Mock()

    notification.id = 1
    notification.user_id = mock_user.id
    notification.report_id = mock_report.id
    notification.type = NotificationType.MESSAGE
    notification.title = "Titolo"
    notification.body = "BOdy"
    notification.is_read = False

    return notification


@pytest.fixture
def mock_report():
    """
    Fornisce un Mock standard globale di un Report.
    """
    report = Mock()
    
    report.id = 100
    report.title = "Default Report Title"
    report.description = "This is a standard default test description."
    report.latitude = 45.4642
    report.longitude = 9.1900
    report.is_anonymous = False
    report.status = ReportStatus.PENDING_APPROVAL #privato
    report.rejection_reason = None
    report.reporter_id = 42
    report.category_id = 5
    
    report.reporter = Mock()
    report.category = Mock()
    report.photos = []
    report.status_history = []
    report.followers = []
    report.messages = []
    
    return report

@pytest.fixture
def mock_user():
    """
    Fornisce un Mock standard globale di uno User.
    """
    user = Mock()
    
    user.id = 1
    user.username = "test_user"
    user.first_name = "Mario"
    user.last_name = "Rossi"
    user.email = "mario.rossi@example.com"
    user.password_hash = "hashed_password_123"
    user.role = Role.CITIZEN  
    user.category_id = 99
    user.is_active = True
    user.is_email_verified = False
    user.email_notifications_enabled = True
    user.profile_picture_path = None
    
    user.category = Mock()
    user.reports = []
    user.notifications = []
    user.verification_tokens = []
    
    return user

@pytest.fixture
def mock_operator(mock_user):
    """Prende l'utente base e lo trasforma in un Operatore"""
    mock_user.id = 2
    mock_user.role = Role.OPERATOR
    mock_user.category_id = 6
    return mock_user

@pytest.fixture
def mock_admin(mock_user):
    """Prende l'utente base e lo trasforma in un Admin"""
    mock_user.id = 3
    mock_user.role = Role.ADMIN
    mock_user.category_id = None  
    return mock_user

@pytest.fixture
def user_service():
    """
    Fornisce l'istanza del servizio UserService con tutti i repository mockati.
    Pronto per lo Unit Testing.
    """
    service = UserService(
        session=Mock(),
        user_repository=Mock(),
        category_repository=Mock(),
        token_repository=Mock(),
        notification_repository=Mock(),
        storage_service=Mock()
    )
    return service

@pytest.fixture
def statistics_service():
    """fornisce istanza di StatisticsService con il repository (mock)"""
    return StatisticsService(report_repository=Mock())

@pytest.fixture
def messaging_service():
    """
    Fornisce l'istanza del servizio MessagingService con tutti i repository mockati.
    """
    service = MessagingService(
        session=Mock(),
        report_repository=Mock(),
        message_repository=Mock(),
        notification_service=Mock()
    )
    return service

@pytest.fixture
def category_service():
    """
    Fornisce l'istanza del servizio category service
    """
    service = CategoryService(
        session=Mock(),
        category_repository = Mock()
    )
    return service

@pytest.fixture
def notification_service():
    """
    Fornisce un istanza di NotificationService
    """
    service = NotificationService(
        session=Mock(),
        notification_repository=Mock(),
        email_gateway=Mock()
    )

    return service

@pytest.fixture
def storage_service():
    return StorageService()

@pytest.fixture
def local_file_storage_service(tmp_path):
    return LocalFileStorageService(media_root=tmp_path)

@pytest.fixture
def mock_file():
    file = Mock()
    file.filename = "test.png"
    return file
