


from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from participium.services.messaging_service import MessagingService
from participium.services.statistics_service import StatisticsService
from participium.models.message import Message
from participium.models.report import ReportFollower, ReportStatusHistory
from participium.models.token import EmailVerificationToken
from participium.services.user_service import UserService
from participium.config.constants import PUBLIC_VISIBLE_STATUSES
from participium.models.enums import ReportStatus
from participium.services.notification_service import NotificationService
from participium.services.report_service import ReportService


@pytest.fixture
def notification_service(db_session, notification_repository):
    return NotificationService(
        session=db_session,
        notification_repository=notification_repository,
        email_gateway=Mock(),
    )

@pytest.fixture
def report_service(db_session, report_repository, category_repository, notification_service):
    return ReportService(
        session=db_session,
        report_repository=report_repository,
        category_repository=category_repository,
        storage_service=mock_storage_service,
        notification_service=notification_service,
    )

@pytest.fixture
def user_service(db_session, user_repository, category_repository, token_repository, notification_repository, mock_storage_service):
    return UserService(
        session=db_session,
        user_repository=user_repository,
        category_repository=category_repository,
        token_repository=token_repository,
        notification_repository=notification_repository,
        storage_service=mock_storage_service,
    )

@pytest.fixture
def populated_db(db_session, test_user, test_category, other_category, make_report, backdate):
    
    public_status = next(iter(PUBLIC_VISIBLE_STATUSES))

    rep_public_cat_a = make_report(
        user_id=test_user.id,
        category_id=test_category.id,
        title="Target Cat A",
        description="Descrizione dettagliata della segnalazione A",
        latitude=41.9028,
        longitude=12.4964,
        status=public_status,
        is_anonymous=False
    )

    rep_public_cat_b = make_report(
        user_id=test_user.id,
        category_id=other_category.id,
        title="Escluso Cat B",
        description="Descrizione dettagliata della segnalazione B",
        latitude=45.4642,
        longitude=9.1900,
        status=public_status,
        is_anonymous=True
    )

    rep_private = make_report(
        user_id=test_user.id,
        category_id=test_category.id,
        title="Privato Approvazione",
        description="Segnalazione non ancora approvata dal moderatore",
        latitude=40.8518,
        longitude=14.2681,
        status=ReportStatus.PENDING_APPROVAL
    )

    db_session.add_all([rep_public_cat_a, rep_public_cat_b, rep_private])
    db_session.commit()

    backdate(db_session, rep_public_cat_b.__class__, rep_public_cat_b.id, days=5)

    return {
        "report_pubblico_a": rep_public_cat_a,
        "report_pubblico_b_vecchio": rep_public_cat_b,
        "report_privato": rep_private,
    }

@pytest.fixture
def mock_storage_service():
    storage = Mock()
    storage.save.return_value = "uploads/test_saved_photo.jpg"
    return storage

@pytest.fixture
def mock_file():
    mock = Mock()
    mock.filename = "test.jpg"
    mock.content_type = "image/jpeg"
    return mock

@pytest.fixture
def user_with_relations(db_session, test_user, test_category, make_report, make_notification):
    report = make_report(user_id=test_user.id, category_id=test_category.id)
    db_session.add(report)
    db_session.commit()
    
    follower = ReportFollower(report_id=report.id, user_id=test_user.id)
    
    message = Message(
        report_id=report.id,
        sender_id=test_user.id,
        recipient_id=test_user.id,
        body="Questo è un messaggio di test tra utenti dell'integrazione."
    )
    
    history = ReportStatusHistory(
        report_id=report.id,
        changed_by_id=test_user.id,
        previous_status=ReportStatus.ASSIGNED,
        new_status=ReportStatus.RESOLVED
    )
    
    notification = make_notification(user_id=test_user.id)
    
    token = EmailVerificationToken(
        user_id=test_user.id, 
        token="token-da-eliminare",
        expires_at=datetime.now() + timedelta(days=1)
    )
    
    db_session.add_all([follower, message, history, notification, token])
    db_session.commit()
    
    return {
        "user": test_user,
        "report": report,
        "message": message,
        "history": history,
        "notification": notification,
        "token": token
    }

@pytest.fixture
def statistics_service(report_repository):
    return StatisticsService(report_repository=report_repository)

@pytest.fixture
def make_historical_report(db_session, make_report):
    def _make(user_id, category_id, created_at, is_public=True, status=None):
        if status is None:
            if is_public:
                status = next(iter(PUBLIC_VISIBLE_STATUSES))
            else:
                status = ReportStatus.PENDING_APPROVAL

        report = make_report(user_id=user_id, category_id=category_id, status=status)
        report.created_at = created_at
        
        db_session.add(report)
        db_session.commit()
        return report
    return _make

@pytest.fixture
def notification_service(db_session, notification_repository):
    return NotificationService(
        session=db_session,
        notification_repository=notification_repository,
        email_gateway=Mock(),  
    )

@pytest.fixture
def store_notification(db_session, make_notification):
    def _store(user_id: int, **kwargs):
        notification = make_notification(user_id=user_id, **kwargs)
        db_session.add(notification)
        db_session.commit()
        return notification
    return _store

@pytest.fixture
def messaging_service(db_session, report_repository, message_repository, notification_service):
    return MessagingService(
        session=db_session,
        report_repository=report_repository,
        message_repository=message_repository,
        notification_service=notification_service
    )