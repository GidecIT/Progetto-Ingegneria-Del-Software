from participium.controllers.user_controller import UserController
from participium.controllers.admin_controller import AdminController
from participium.controllers.auth_controller import AuthController
from participium.controllers.operator_controller import OperatorController
from participium.controllers.report_controller import ReportController
from participium.controllers.statistics_controller import StatisticsController
from participium.services.storage_service import LocalFileStorageService, StorageService
from participium.services.notification_service import NotificationService
from participium.services.category_service import CategoryService
from participium.services.messaging_service import MessagingService
from participium.services.statistics_service import StatisticsService
from participium.services.user_service import UserService
from participium.models.enums import NotificationType, ReportStatus, Role
from participium.services.auth_service import AuthService
import pytest
from unittest.mock import Mock

from participium.services.report_service import ReportService

@pytest.fixture
def user_controller(user_service, notification_service):
    return UserController(user_service=user_service, notification_service=notification_service)

@pytest.fixture
def statistics_controller(statistics_service):
    """Istanza del controller inserendo il servizio mockato."""
    return StatisticsController(statistics_service=statistics_service)

@pytest.fixture
def operator_controller():

    return OperatorController(
        report_service=Mock(spec=ReportService),
        notification_service=Mock(spec=NotificationService),
    )

@pytest.fixture
def report_controller():
    """Fornisce l'istanza di ReportController con i servizi mockati."""
    
    return ReportController(
        report_service=Mock(spec=ReportService),
        messaging_service=Mock(spec=MessagingService),
        notification_service=Mock(spec=NotificationService),
    )

@pytest.fixture
def auth_controller():
    
    return AuthController(
        auth_service=Mock(spec=AuthService)
    )

@pytest.fixture
def admin_controller():
    
    return AdminController(
        category_service=Mock(spec=CategoryService),
        user_service=Mock(spec=UserService),
        statistics_service=Mock(spec=StatisticsService),
    )

@pytest.fixture
def report_service_with_active_category(report_service):
    """Configura una categoria attiva nel category_repository."""
    category = Mock(id=1, is_active=True)
    report_service.category_repository.get_by_id.return_value = category
    return report_service


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
    report.status = ReportStatus.PENDING_APPROVAL  # privato
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
    """Fornisce un Mock standard globale di uno User (Citizen)."""
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
def mock_operator():
    """Fornisce un Mock isolato e indipendente di un Operator."""
    user = Mock()
    user.id = 2
    user.username = "test_operator"
    user.first_name = "Luca"
    user.last_name = "Verdi"
    user.email = "luca.verdi@example.com"
    user.role = Role.OPERATOR
    user.category_id = 6
    user.is_active = True
    user.category = Mock()
    return user


@pytest.fixture
def mock_admin():
    """Fornisce un Mock isolato e indipendente di un Admin."""
    user = Mock()
    user.id = 3
    user.username = "test_admin"
    user.first_name = "Anna"
    user.last_name = "Bianchi"
    user.email = "anna.bianchi@example.com"
    user.role = Role.ADMIN
    user.category_id = None
    user.is_active = True
    return user


@pytest.fixture
def mock_file():
    file = Mock()
    file.filename = "test.png"
    return file


@pytest.fixture
def report_service():
    """ Fornisce l'istanza del servizio ReportService"""

    service = ReportService(
        session=Mock(),
        report_repository=Mock(),
        category_repository=Mock(),
        storage_service=Mock(),
        notification_service=Mock()
    )

    return service


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
        category_repository=Mock()
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
def mock_token():
    """Fornisce un mock standard di un EmailVerificationToken."""
    token = Mock()

    token.id = 1
    token.user_id = 1
    token.token = "fake-token-value-abc123"
    token.is_used = False
    token.expires_at = Mock()
    token.user = Mock()

    return token


@pytest.fixture
def auth_service():
    """
    Fornisce l'istanza del servizio AuthService con tutti i repository mockati.
    Pronto per lo Unit Testing.
    """
    service = AuthService(
        session=Mock(),
        user_repository=Mock(),
        token_repository=Mock(),
        email_gateway=Mock()
    )
    return service
