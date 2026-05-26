from __future__ import annotations

from unittest.mock import Mock
import pytest

from participium.core.exceptions import AuthorizationError, ValidationError, NotFoundError
from participium.models.report import Report
from participium.models.user import User
from participium.models.enums import Role, ReportStatus
from participium.models.report import ReportStatusHistory
from participium.services.report_service import ReportService

VALID_REPORT_ID = 10
INVALID_REPORT_ID = 999

OP_CAT_1 = User(id=100, username="op_cat_1", role=Role.OPERATOR, category_id=0)  
OP_CAT_2 = User(id=101, username="op_cat_2", role=Role.OPERATOR, category_id=1)  
USER_NO_PERM = User(id=103, username="user_no_perm", role=Role.CITIZEN)


@pytest.fixture
def report_context():
    session_mock = Mock()
    repo_mock = Mock()
    cat_repo_mock = Mock()
    storage_mock = Mock()
    notification_mock = Mock()

    service = ReportService(
        session=session_mock,
        report_repository=repo_mock,
        category_repository=cat_repo_mock,
        storage_service=storage_mock,
        notification_service=notification_mock
    )

    return {
        "service": service,
        "repo": repo_mock,
        "session": session_mock
    }


def test_us01_update_status_success_no_note(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_report.status_history = [ReportStatusHistory(note=None)]
    mock_report.reporter = OP_CAT_1
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(VALID_REPORT_ID, OP_CAT_1, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.status == ReportStatus.ASSIGNED
    assert report.id == VALID_REPORT_ID


def test_us02_update_status_success_with_note(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_report.status_history = [ReportStatusHistory(note="Report già segnalato")]
    mock_report.reporter = OP_CAT_1
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(VALID_REPORT_ID, OP_CAT_1, ReportStatus.ASSIGNED.value, note="Report già segnalato")

    assert isinstance(report, Report)
    assert report.status == ReportStatus.ASSIGNED
    assert report.status_history[-1].note == "Report già segnalato"


def test_us03_update_status_not_found(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.update_status(INVALID_REPORT_ID, OP_CAT_1, ReportStatus.ASSIGNED.value, note=None)


def test_us04_update_status_unauthorized_role(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(AuthorizationError):
        service.update_status(VALID_REPORT_ID, USER_NO_PERM, ReportStatus.ASSIGNED.value, note=None)


def test_us05_update_status_wrong_category(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(AuthorizationError):
        service.update_status(VALID_REPORT_ID, OP_CAT_2, ReportStatus.ASSIGNED.value, note=None)


def test_us06_update_status_rejected_missing_note(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(VALID_REPORT_ID, OP_CAT_1, ReportStatus.REJECTED.value, note=None)


def test_us07_update_status_invalid_workflow_transition(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.RESOLVED)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(VALID_REPORT_ID, OP_CAT_1, ReportStatus.REJECTED.value, note="Lo stato non mi piace")


def test_us08_update_status_invalid_enum_value(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(VALID_REPORT_ID, OP_CAT_1, "StatoInventato", note=None)


def test_usb01_exact_boundary_report_id(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=1, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_report.status_history = [ReportStatusHistory(note=None)]
    mock_report.reporter = OP_CAT_1
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(1, OP_CAT_1, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.id == 1


def test_usb02_immediately_below_report_id(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.update_status(-1, OP_CAT_1, ReportStatus.ASSIGNED.value, note=None)


def test_usb03_exact_boundary_next_status_and_note(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_report.status_history = [ReportStatusHistory(note="N")]
    mock_report.reporter = OP_CAT_1
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(10, OP_CAT_1, ReportStatus.REJECTED.value, note="N")

    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == ReportStatus.REJECTED


def test_usb04_immediately_below_note_none(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(10, OP_CAT_1, ReportStatus.REJECTED.value, note=None)


def test_usb05_immediately_below_note_empty(report_context) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(10, OP_CAT_1, ReportStatus.REJECTED.value, note="")
