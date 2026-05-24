from __future__ import annotations
from datetime import datetime
import pytest

from participium.models.category import Category
from participium.models.enums import ReportStatus
from participium.models.report import Report
from participium.services.report_service import ReportService

DATE_FEB = datetime(2024, 2, 1)
DATE_MAR = datetime(2024, 3, 1)


@pytest.fixture
def test_reports() -> list[Report]:
    report_0 = Report(id=4, title="Boundary 0", description="Cat 0", status=ReportStatus.IN_PROGRESS, category_id=3, latitude=45.0, longitude=7.0, reporter_id=1)
    report_0.created_at = datetime(2024, 1, 1)

    report_1 = Report(id=1, title="Segnalazione 1", description="Descrizione 1", status=ReportStatus.IN_PROGRESS, category_id=1, latitude=45.0, longitude=7.0, reporter_id=1)
    report_1.created_at = datetime(2024, 1, 15)

    report_2 = Report(id=2, title="Segnalazione 2", description="Descrizione 2", status=ReportStatus.ASSIGNED, category_id=1, latitude=45.0, longitude=7.0, reporter_id=1)
    report_2.created_at = datetime(2024, 2, 15)

    report_3 = Report(id=3, title="Segnalazione 3", description="Descrizione 3", status=ReportStatus.SUSPENDED, category_id=2, latitude=45.0, longitude=7.0, reporter_id=1)
    report_3.created_at = datetime(2024, 3, 15)

    return [report_0, report_1, report_2, report_3]


@pytest.fixture
def report_service(db_session, report_repository, category_repository) -> ReportService:
    return ReportService(
        session=db_session,
        report_repository=report_repository,
        category_repository=category_repository,
        storage_service=None,
    )

@pytest.fixture
def setup_db(db_session, test_user, test_reports):
    cat_1 = Category(id=1, name="Categoria 1", is_active=True)
    cat_2 = Category(id=2, name="Categoria 2", is_active=True)
    cat_3 = Category(id=3, name="Categoria 3", is_active=True)
    
    db_session.add_all([cat_1, cat_2, cat_3])
    db_session.flush()

    for report in test_reports:
        db_session.add(report)
        
    db_session.commit()


@pytest.mark.parametrize(
    "category_id,status,date_from,date_to,sort,expected_ids",
    [
        (None, None, None, None, "desc", [3, 2, 1, 4]), # PR01
        (1, None, None, None, "asc", [1, 2]),            # PR02
        (None, ReportStatus.ASSIGNED, None, None, "desc", [2]), # PR03
        (None, None, DATE_FEB, None, "desc", [3, 2]),    # PR04
        (None, None, None, DATE_FEB, "desc", [1, 4]),    # PR05
        (None, None, DATE_FEB, DATE_MAR, "desc", [2]),   # PR06
        (1, ReportStatus.SUSPENDED, None, None, "asc", []), # PR07
        (1, ReportStatus.SUSPENDED, DATE_FEB, DATE_MAR, "asc", []), # PR08
        (9999, None, None, None, "desc", []),            # PR10 / PRB02
        (1, None, None, None, "desc", [2, 1]),           # PRB01
        (-1, None, None, None, "desc", []),              # PRB03
    ],
)
@pytest.mark.usefixtures("setup_db")
def test_list_public_reports(report_service, category_id, status, date_from, date_to, sort, expected_ids):
    result = report_service.list_public_reports(
        category_id=category_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
        sort=sort
    )
    
    assert isinstance(result, list)
    actual_ids = [r.id for r in result]
    assert actual_ids == expected_ids, f"Errore: attesi {expected_ids}, ottenuti {actual_ids}"

    for report in result:
        if category_id is not None:
            assert report.category_id == category_id
        if status is not None:
            assert report.status == status

def test_list_public_reports_empty_db(report_service): #PR09
    result = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=None,
        date_to=None,
        sort="desc"
    )
    
    assert result == [], "PR09 Fallito: Con DB vuoto il sistema doveva restituire una lista vuota."