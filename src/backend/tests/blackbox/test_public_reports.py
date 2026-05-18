from __future__ import annotations
from datetime import datetime
import pytest

from participium.services.report_service import ReportService
from participium.models.enums import ReportStatus
from participium.models.report import Report

REPORT_0 = Report(id=4, title="Boundary 0", description="Cat 0", status=ReportStatus.PENDING_APPROVAL, category_id=0)
REPORT_0.created_at = datetime(2024, 1, 1)

REPORT_1 = Report(id=1, title="Segnalazione 1", description="Descrizione 1", status=ReportStatus.PENDING_APPROVAL, category_id=1)
REPORT_1.created_at = datetime(2024, 1, 15)

REPORT_2 = Report(id=2, title="Segnalazione 2", description="Descrizione 2", status=ReportStatus.ASSIGNED, category_id=1)
REPORT_2.created_at = datetime(2024, 2, 15)

REPORT_3 = Report(id=3, title="Segnalazione 3", description="Descrizione 3", status=ReportStatus.SUSPENDED, category_id=2)
REPORT_3.created_at = datetime(2024, 3, 15)

ALL_REPORTS = [REPORT_0, REPORT_1, REPORT_2, REPORT_3]
DATE_FEB = datetime(2024, 2, 1)
DATE_MAR = datetime(2024, 3, 1)

@pytest.fixture
def fixture_state(report_repository, request) -> str:
    # Recupera se "populated" o "empty": state = request.param 
    # Se lo stato della fixture è populated: popola con tutti i report 
    # se lo stato è empty assicura che sia vuoto
    pass

@pytest.fixture
def report_service(session, report_repository, category_repository, storage_service) -> ReportService:
    return ReportService(
        session=session,
        report_repository=report_repository,
        category_repository=category_repository,
        storage_service=storage_service,
    )

@pytest.mark.parametrize(
    "category_id, status, date_from, date_to, sort, fixture_state, expected_ids",
    [
        (None, None, None, None, "desc", "populated", [3, 2, 1, 4]),
        (1, None, None, None, "asc", "populated", [1, 2]),
        (None, ReportStatus.ASSIGNED, None, None, "desc", "populated", [2]),
        (None, None, DATE_FEB, None, "desc", "populated", [3, 2]),
        (None, None, None, DATE_FEB, "desc", "populated", [1, 4]),
        (None, None, DATE_FEB, DATE_MAR, "desc", "populated", [2]),
        (1, ReportStatus.SUSPENDED, None, None, "asc", "populated", []),
        (1, ReportStatus.SUSPENDED, DATE_FEB, DATE_MAR, "asc", "populated", []),
        (None, None, None, None, "desc", "empty", []),
        (9999, None, None, None, "desc", "populated", []),
        (0, None, None, None, "desc", "populated", [4]),
        (10, None, None, None, "desc", "populated", []),
        (-1, None, None, None, "desc", "populated", []),
    ],
    indirect=["fixture_state"]
)

@pytest.mark.skip(reason="Disabled.")
def test_list_public_reports(report_service, fixture_state, category_id, status, date_from, date_to, sort, expected_ids):
    result = report_service.list_public_reports(category_id=category_id,status=status,date_from=date_from,date_to=date_to,sort=sort)
    
    assert isinstance(result, list)
    actual_ids = [r.id for r in result]
    assert actual_ids == expected_ids, f"Errore: attesi {expected_ids}, ottenuti {actual_ids}"

    for report in result:
        assert isinstance(report, Report)
        if category_id is not None:
            assert report.category_id == category_id
        if status is not None:
            assert report.status == status
        if date_from is not None:
            assert report.created_at >= date_from
        if date_to is not None:
            assert report.created_at <= date_to