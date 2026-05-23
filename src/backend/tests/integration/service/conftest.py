


from unittest.mock import Mock

import pytest

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
def populated_db(db_session, test_user, test_category, other_category, make_report, backdate):
    """Popola il database reale in-memory rispettando i vincoli dei modelli Report e User."""
    
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
    """Simula lo storage service per evitare di scrivere file reali sul disco."""
    storage = Mock()
    storage.save.return_value = "uploads/test_saved_photo.jpg"
    return storage

@pytest.fixture
def mock_file():
    mock = Mock()
    mock.filename = "test.jpg"
    mock.content_type = "image/jpeg"
    return mock
