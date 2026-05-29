import pytest
from unittest.mock import Mock

from participium.repositories.user_repository import UserRepository
from participium.repositories.notification_repository import NotificationRepository
from participium.repositories.token_repository import TokenRepository
from participium.repositories.message_repository import MessageRepository
from participium.repositories.category_repository import CategoryRepository
from participium.repositories.report_repository import ReportRepository
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
from participium.services.report_service import ReportService
from participium.services.auth_service import AuthService
from participium.models.enums import NotificationType, ReportStatus, Role

@pytest.fixture
def mock_settings(tmp_path):
    settings = Mock()
    settings.mail_backend = "console"
    settings.mail_from = "noreply@participium.it"
    settings.mail_outbox_dir = tmp_path / "outbox"
    settings.smtp_host = "smtp.example.com"
    settings.smtp_port = 587
    settings.smtp_username = "user_smtp"
    settings.smtp_password = "secure_password"
    settings.smtp_use_tls = True
    return settings

@pytest.fixture
def mock_smtp(monkeypatch):
    mock_smtp_instance = Mock()
    mock_smtp_class = Mock(return_value=mock_smtp_instance)
    mock_smtp_instance.__enter__ = Mock(return_value=mock_smtp_instance)
    mock_smtp_instance.__exit__ = Mock(return_value=None)
    monkeypatch.setattr("smtplib.SMTP", mock_smtp_class)
    return mock_smtp_instance

@pytest.fixture
def mock_session():
    return Mock()

@pytest.fixture
def user_repository(mock_session):
    return UserRepository(session=mock_session)

@pytest.fixture
def token_repository(mock_session):
    return TokenRepository(session=mock_session)

@pytest.fixture
def notification_repository(mock_session):
    return NotificationRepository(session=mock_session)

@pytest.fixture
def message_repository(mock_session):
    return MessageRepository(session=mock_session)

@pytest.fixture
def report_repository(mock_session):
    return ReportRepository(session=mock_session)

@pytest.fixture
def category_repository(mock_session):
    return CategoryRepository(session=mock_session)

@pytest.fixture
def user_controller(user_service, notification_service):
    return UserController(user_service=user_service, notification_service=notification_service)

@pytest.fixture
def statistics_controller(statistics_service):
    return StatisticsController(statistics_service=statistics_service)

@pytest.fixture
def operator_controller():
    return OperatorController(
        report_service=Mock(spec=ReportService),
        notification_service=Mock(spec=NotificationService),
    )

@pytest.fixture
def report_controller():
    return ReportController(
        report_service=Mock(spec=ReportService),
        messaging_service=Mock(spec=MessagingService),
        notification_service=Mock(spec=NotificationService),
    )

@pytest.fixture
def auth_controller():
    return AuthController(auth_service=Mock(spec=AuthService))

@pytest.fixture
def admin_controller():
    return AdminController(
        category_service=Mock(spec=CategoryService),
        user_service=Mock(spec=UserService),
        statistics_service=Mock(spec=StatisticsService),
    )

@pytest.fixture
def report_service_with_active_category(report_service):
    category = Mock(id=1, is_active=True)
    report_service.category_repository.get_by_id.return_value = category
    return report_service

@pytest.fixture
def mock_category():
    category = Mock()
    category.id = 1
    category.name = "Water"
    category.is_active = True
    return category

@pytest.fixture
def mock_notification(mock_user, mock_report):
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
    report = Mock()
    report.id = 100
    report.title = "Default Report Title"
    report.description = "This is a standard default test description."
    report.latitude = 45.4642
    report.longitude = 9.1900
    report.is_anonymous = False
    report.status = ReportStatus.PENDING_APPROVAL
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
    return ReportService(
        session=Mock(),
        report_repository=Mock(),
        category_repository=Mock(),
        storage_service=Mock(),
        notification_service=Mock()
    )

@pytest.fixture
def user_service():
    return UserService(
        session=Mock(),
        user_repository=Mock(),
        category_repository=Mock(),
        token_repository=Mock(),
        notification_repository=Mock(),
        storage_service=Mock()
    )

@pytest.fixture
def statistics_service():
    return StatisticsService(report_repository=Mock())

@pytest.fixture
def messaging_service():
    return MessagingService(
        session=Mock(),
        report_repository=Mock(),
        message_repository=Mock(),
        notification_service=Mock()
    )

@pytest.fixture
def category_service():
    return CategoryService(
        session=Mock(),
        category_repository=Mock()
    )

@pytest.fixture
def notification_service():
    return NotificationService(
        session=Mock(),
        notification_repository=Mock(),
        email_gateway=Mock()
    )

@pytest.fixture
def storage_service():
    return StorageService()

@pytest.fixture
def local_file_storage_service(tmp_path):
    return LocalFileStorageService(media_root=tmp_path)

@pytest.fixture
def mock_token():
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
    return AuthService(
        session=Mock(),
        user_repository=Mock(),
        token_repository=Mock(),
        email_gateway=Mock()
    )