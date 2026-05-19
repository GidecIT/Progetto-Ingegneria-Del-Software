from participium.models.enums import ReportStatus, Role
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

    report_repository = Mock()
    report_repository.get_follower.return_value = None  #false
    report_repository.add_follower.return_value = None  #false

    service =  ReportService(
        session=Mock(),
        report_repository=report_repository,
        category_repository=Mock(),
        storage_service=Mock(),
        notification_service=Mock()
    )
    

    return service

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