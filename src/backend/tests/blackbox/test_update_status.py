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
OPERATOR_CAT_0 = User(id=100, username="op1", role=Role.OPERATOR, category_id=0)
OPERATOR_CAT_1 = User(id=101, username="op2", role=Role.OPERATOR, category_id=1)
OPERATOR_CAT_INVALID = User(id=102, username="op_cat_inv", role=Role.OPERATOR, category_id=-1)
USER_NO_PERM = User(id=103, username="generic_user", role=Role.CITIZEN)


@pytest.fixture
def seed_report_service() -> None:
    pass


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


def test_us01_update_status_success_with_note(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)

    mock_history = ReportStatusHistory(note="Tutto OK")
    mock_report.status_history = [mock_history]

    mock_report.reporter = OPERATOR_CAT_0
    mock_report.reporter_id = OPERATOR_CAT_0.id
    mock_report.followers = []


    repo.get_by_id.return_value = mock_report

    report = service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note="Tutto OK")

    assert isinstance(report, Report)
    assert report.status == ReportStatus.ASSIGNED
    assert report.id == 10
    assert report.reporter == OPERATOR_CAT_0
    assert report.reporter_id == OPERATOR_CAT_0.id


def test_us02_update_status_success_no_note(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_history = ReportStatusHistory(note=None)
    mock_report.status_history = [mock_history]
    mock_report.reporter = OPERATOR_CAT_0
    mock_report.reporter_id = OPERATOR_CAT_0.id
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.status == ReportStatus.ASSIGNED
    assert report.id == 10


def test_us03_update_status_not_found(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.update_status(INVALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value)


def test_us04_update_status_unauthorized_role(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(AuthorizationError):
        service.update_status(VALID_REPORT_ID, USER_NO_PERM, ReportStatus.ASSIGNED.value)


def test_us05_update_status_wrong_category(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(AuthorizationError):
        service.update_status(VALID_REPORT_ID, OPERATOR_CAT_1, ReportStatus.ASSIGNED.value)


def test_us06_update_status_rejected_missing_note(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note=None)


def test_us07_update_status_invalid_workflow_transition(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=VALID_REPORT_ID, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.RESOLVED.value)


def test_usb01_exact_boundary(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=1, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_history = ReportStatusHistory(note=None)
    mock_report.status_history = [mock_history]
    mock_report.reporter = OPERATOR_CAT_0
    mock_report.reporter_id = OPERATOR_CAT_0.id
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(1, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.id == 1


def test_usb02_immediately_below_boundary(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.update_status(-1, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)


def test_usb03_exact_boundary_next_status_and_note(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    # We assume moving to REJECTED from PENDING_APPROVAL is allowed
    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_history = ReportStatusHistory(note="N")
    mock_report.status_history = [mock_history]
    mock_report.reporter = OPERATOR_CAT_0
    mock_report.reporter_id = OPERATOR_CAT_0.id
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(10, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note="N")

    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == ReportStatus.REJECTED


def test_usb04_immediately_below_note_none(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(10, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note=None)


def test_usb05_immediately_below_note_empty(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(ValidationError):
        service.update_status(10, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note="")


def test_usb06_exact_boundary_category(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=0, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    mock_history = ReportStatusHistory(note=None)
    mock_report.status_history = [mock_history]
    mock_report.reporter = OPERATOR_CAT_0
    mock_report.reporter_id = OPERATOR_CAT_0.id
    mock_report.followers = []

    repo.get_by_id.return_value = mock_report

    report = service.update_status(0, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.id == 0


def test_usb07_immediately_below_operator_category(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=0, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(AuthorizationError):
        service.update_status(10, OPERATOR_CAT_INVALID, ReportStatus.ASSIGNED.value, note=None)


def test_usb08_immediately_above_report_category(report_context, seed_report_service: None) -> None:
    service = report_context["service"]
    repo = report_context["repo"]

    mock_report = Report(id=10, category_id=5, status=ReportStatus.PENDING_APPROVAL)
    repo.get_by_id.return_value = mock_report

    with pytest.raises(AuthorizationError):
        service.update_status(10, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)