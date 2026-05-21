from __future__ import annotations
from datetime import datetime
import pytest
from unittest.mock import Mock

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
def report_service() -> ReportService:
    repo = Mock()

    return ReportService(
        session=Mock(),
        report_repository=repo,
        category_repository=Mock(),
        storage_service=Mock(),
    )

@pytest.fixture
def setup_db(db_session, report_service):
    for report in ALL_REPORTS:
        db_session.add(report)
    db_session.commit()

@pytest.mark.skip(reason="Disabled")
@pytest.mark.parametrize(
        "category_id, status, date_from, date_to, sort, expected_ids",
    [
        (None, None, None, None, "desc",[3, 2, 1, 4]),
        (1, None, None, None, "asc",[1, 2]),
        (None, ReportStatus.ASSIGNED, None, None, "desc",[2]),
        (None, None, DATE_FEB, None, "desc",[3, 2]),
        (None, None, None, DATE_FEB, "desc",[1, 4]),
        (None, None, DATE_FEB, DATE_MAR, "desc",[2]),
        (1, ReportStatus.SUSPENDED, None, None, "asc",[]),
        (1, ReportStatus.SUSPENDED, DATE_FEB, DATE_MAR, "asc",[]),
        (9999, None, None, None, "desc",[]),
        (0, None, None, None, "desc",[4]),
        (10, None, None, None, "desc",[]),
        (-1, None, None, None, "desc",[]),
    ],
)


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