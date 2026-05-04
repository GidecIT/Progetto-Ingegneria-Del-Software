from __future__ import annotations

import pytest

from participium.core.exceptions import AuthorizationError, ValidationError, NotFoundError
from participium.models.report import Report
from participium.models.user import User
from participium.models.enums import Role, ReportStatus

from participium.services.report_service import ReportService

VALID_REPORT_ID = 10
INVALID_REPORT_ID = 999
OPERATOR_CAT_0 = User(id=100, username="op1", role=Role.OPERATOR, category_id=0)
OPERATOR_CAT_1 = User(id=101, username="op2", role=Role.OPERATOR, category_id=1)
OPERATOR_CAT_INVALID = User(id=102, username="op_cat_inv", role=Role.OPERATOR, category_id=-1)
USER_NO_PERM = User(id=103, username="generic_user", role=Role.CITIZEN)


@pytest.fixture
def seed_report_service() -> None:
    # Populate the system with users and reports needed by
    # `ReportService.update_status`.
    pass

@pytest.fixture
def report_service() -> ReportService:
    return ReportService()

def test_us01_update_status_success_with_note(report_service: ReportService, seed_report_service: None) -> None:
    report = report_service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note="Tutto OK")

    assert isinstance(report, Report)
    assert report.status == ReportStatus.ASSIGNED.value
    assert report.id == 10
    assert report.reporter == OPERATOR_CAT_0
    assert report.reporter_id == OPERATOR_CAT_0.id
    assert report.status_history[-1].note == "Tutto ok"

def test_us02_update_status_success_no_note(report_service: ReportService, seed_report_service: None) -> None:
    report = report_service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.status == ReportStatus.ASSIGNED.value
    assert report.id == 10
    assert report.reporter == OPERATOR_CAT_0
    assert report.reporter_id == OPERATOR_CAT_0.id
    assert report.status_history[-1].note is None

def test_us03_update_status_not_found(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(NotFoundError):
        report_service.update_status(INVALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value)

def test_us04_update_status_unauthorized_role(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(AuthorizationError):
        report_service.update_status(VALID_REPORT_ID, USER_NO_PERM, ReportStatus.ASSIGNED.value)

def test_us05_update_status_wrong_category(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(AuthorizationError):
        report_service.update_status(VALID_REPORT_ID, OPERATOR_CAT_1, ReportStatus.ASSIGNED.value)

def test_us06_update_status_rejected_missing_note(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(ValidationError):
        report_service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note=None)

def test_us07_update_status_invalid_workflow_transition(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(ValidationError):
        report_service.update_status(VALID_REPORT_ID, OPERATOR_CAT_0, ReportStatus.RESOLVED.value)

def test_usb01_exact_boundary(report_service: ReportService, seed_report_service: None) -> None:
    report = report_service.update_status(1, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.id == 1
    assert report.status == ReportStatus.ASSIGNED.value
    assert report.reporter == OPERATOR_CAT_0
    assert report.reporter_id == OPERATOR_CAT_0.id
    assert report.status_history[-1].note is None

def test_usb02_immediately_below_boundary(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(NotFoundError):
        report_service.update_status(-1, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

def test_usb03_exact_boundary_next_status_and_note(report_service: ReportService, seed_report_service: None) -> None:
    report = report_service.update_status(10, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note="N")

    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == ReportStatus.REJECTED.value
    assert report.reporter == OPERATOR_CAT_0
    assert report.reporter_id == OPERATOR_CAT_0.id
    assert report.status_history[-1].note == "N"

def test_usb04_immediately_below_note_none(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(ValidationError):
        report_service.update_status(10, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note=None)

def test_usb05_immediately_below_note_empty(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(ValidationError):
        report_service.update_status(10, OPERATOR_CAT_0, ReportStatus.REJECTED.value, note="")

def test_usb06_exact_boundary_category(report_service: ReportService, seed_report_service: None) -> None:
    report = report_service.update_status(0, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)

    assert isinstance(report, Report)
    assert report.id == 0
    assert report.status == ReportStatus.ASSIGNED.value
    assert report.reporter == OPERATOR_CAT_0
    assert report.reporter_id == OPERATOR_CAT_0.id
    assert report.status_history[-1].note is None

def test_usb07_immediately_below_operator_category(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(ValidationError):
        report_service.update_status(10, OPERATOR_CAT_INVALID, ReportStatus.ASSIGNED.value, note=None)

def test_usb08_immediately_above_report_category(report_service: ReportService, seed_report_service: None) -> None:

    with pytest.raises(ValidationError):
        report_service.update_status(10, OPERATOR_CAT_0, ReportStatus.ASSIGNED.value, note=None)