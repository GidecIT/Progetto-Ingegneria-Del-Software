from __future__ import annotations
from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest

from participium.models.enums import ReportStatus
from participium.models.report import Report
from participium.services.report_service import ReportService

DATE_FEB = datetime(2024, 2, 1)
DATE_MAR = datetime(2024, 3, 1)

DATE_REPORT_2 = datetime(2024, 2, 15)


@pytest.fixture
def test_reports() -> list[Report]:
    report_0 = Report(id=4, title="Boundary 0", description="Cat 0", status=ReportStatus.IN_PROGRESS, category_id=3, latitude=45.0, longitude=7.0, reporter_id=1)
    report_0.created_at = datetime(2024, 1, 1)

    report_1 = Report(id=1, title="Segnalazione 1", description="Descrizione 1", status=ReportStatus.IN_PROGRESS, category_id=1, latitude=45.0, longitude=7.0, reporter_id=1)
    report_1.created_at = datetime(2024, 1, 15)

    report_2 = Report(id=2, title="Segnalazione 2", description="Descrizione 2", status=ReportStatus.ASSIGNED, category_id=1, latitude=45.0, longitude=7.0, reporter_id=1)
    report_2.created_at = DATE_REPORT_2

    report_3 = Report(id=3, title="Segnalazione 3", description="Descrizione 3", status=ReportStatus.SUSPENDED, category_id=2, latitude=45.0, longitude=7.0, reporter_id=1)
    report_3.created_at = datetime(2024, 3, 15)

    return [report_0, report_1, report_2, report_3]


@pytest.fixture
def mock_report_repository():
    return Mock()


@pytest.fixture
def report_service(mock_report_repository) -> ReportService:
    return ReportService(
        session=Mock(),
        report_repository=mock_report_repository, 
        category_repository=Mock(),
        storage_service=Mock(),                  
    )


@pytest.mark.parametrize(
    "category_id,status,date_from,date_to,sort,expected_ids",
    [
        (None, None, None, None, "desc", [3, 2, 1, 4]),
        (1, None, None, None, "asc", [1, 2]),
        (None, ReportStatus.ASSIGNED, None, None, "desc", [2]),
        (None, None, DATE_FEB, None, "desc", [3, 2]),
        (None, None, None, DATE_FEB, "desc", [1, 4]),
        (None, None, DATE_FEB, DATE_MAR, "desc", [2]),
        (1, ReportStatus.SUSPENDED, None, None, "asc", []),
        (1, ReportStatus.SUSPENDED, DATE_FEB, DATE_MAR, "asc", []),
        (9999, None, None, None, "desc", []),
        (1, None, None, None, "desc", [2, 1]),
        (-1, None, None, None, "desc", []),
        (None, None, None, DATE_REPORT_2, "desc", [2, 1, 4]),
        (None, None, None, DATE_REPORT_2 - timedelta(seconds=1), "desc", [1, 4]),
        (None, None, None, DATE_REPORT_2 + timedelta(seconds=1), "desc", [2, 1, 4]),
        (None, None, DATE_REPORT_2, None, "desc", [3, 2]),
        (None, None, DATE_REPORT_2 - timedelta(seconds=1), None, "desc", [3, 2]),
        (None, None, DATE_REPORT_2 + timedelta(seconds=1), None, "desc", [3]),
    ],
)
def test_list_public_reports(report_service, mock_report_repository, test_reports, category_id, status, date_from, date_to, sort, expected_ids):
    
    def mock_side_effect(*args, **kwargs):
        filtered = []
        for r in test_reports:
            if category_id is not None and r.category_id != category_id:
                continue
            if status is not None and r.status != status:
                continue
            if date_from is not None and r.created_at < date_from:
                continue
            if date_to is not None and r.created_at > date_to:
                continue
            filtered.append(r)
        
        is_desc = (sort == "desc")
        filtered.sort(key=lambda x: x.created_at, reverse=is_desc)
        return filtered

    mock_report_repository.list_reports.side_effect = mock_side_effect

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

    mock_report_repository.list_reports.assert_called_once_with(public_only=True,category_id=category_id,status=status,date_from=date_from,date_to=date_to,sort=sort)


def test_list_public_reports_empty_db(report_service, mock_report_repository):
    mock_report_repository.list_reports.return_value = []
    
    result = report_service.list_public_reports(
        category_id=None,
        status=None,
        date_from=None,
        date_to=None,
        sort="desc"
    )
    
    assert result == [], "PR09 Fallito: Con DB vuoto il sistema doveva restituire una lista vuota."
    
    mock_report_repository.list_reports.assert_called_once_with(public_only=True,category_id=None,status=None,date_from=None,date_to=None,sort="desc")