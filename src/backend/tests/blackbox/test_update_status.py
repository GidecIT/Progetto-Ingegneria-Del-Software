from __future__ import annotations

import pytest

from participium.core.exceptions import AuthorizationError, ValidationError, NotFoundError
from participium.models.report import Report
from participium.models.user import User
from participium.models.enums import Role

from participium.services.report_service import ReportService

@pytest.fixture
def report_service() -> ReportService:
    return ReportService()

@pytest.fixture
def op_cat_1() -> User:
    return User(id=100, username="op1", role=Role.OPERATOR, category_id=1)

@pytest.fixture
def op_cat_2() -> User:
    return User(id=101, username="op2", role=Role.OPERATOR, category_id=2)

@pytest.fixture
def user_no_perm() -> User:
    return User(id=102, username="user_low", role=Role.USER)

def test_us01_success_with_note(report_service: ReportService, op_cat_1: User) -> None:
    report = report_service.update_status(10, op_cat_1, "Assigned", note="Tutto ok")
    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == "Assigned"
    assert report.reporter == op_cat_1
    assert report.reporter_id == op_cat_1.id

def test_us02_success_no_note(report_service: ReportService, op_cat_1: User) -> None:
    report = report_service.update_status(10, op_cat_1, "Assigned", note=None)
    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == "Assigned"
    assert report.reporter == op_cat_1
    assert report.reporter_id == op_cat_1.id

def test_us03_not_found(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(NotFoundError):
        report_service.update_status(999, op_cat_1, "Assigned", note=None)

def test_us04_unauthorized_role(report_service: ReportService, user_no_perm: User) -> None:
    with pytest.raises(AuthorizationError):
        report_service.update_status(10, user_no_perm, "Assigned", note=None)

def test_us05_wrong_category(report_service: ReportService, op_cat_2: User) -> None:
    with pytest.raises(AuthorizationError):
        report_service.update_status(10, op_cat_2, "Assigned", note="Tutto ok")

def test_us06_rejection_without_note(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Rejected", note=None)

def test_us07_invalid_workflow(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Rejected", note="Lo stato non mi piace")

def test_usb01_exact_boundary(report_service: ReportService, op_cat_1: User) -> None:
    report = report_service.update_status(1, op_cat_1, "Assigned", note=None)
    assert isinstance(report, Report)
    assert report.id == 1
    assert report.status == "Assigned"
    assert report.reporter == op_cat_1
    assert report.reporter_id == op_cat_1.id

def test_usb02_immediately_below_boundary(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(NotFoundError):
        report_service.update_status(-1, op_cat_1, "Assigned", note=None)

def test_usb03_exact_boundary_next_status_and_note(report_service: ReportService, op_cat_1: User) -> None:
    report = report_service.update_status(10, op_cat_1, "Rejected", note="N")
    assert isinstance(report, Report)
    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == "Rejected"
    assert report.reporter == op_cat_1
    assert report.reporter_id == op_cat_1.id

def test_usb04_immediately_below_note_none(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Rejected", note=None)

def test_usb05_immediately_below_note_empty(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Rejected", note="")

def test_usb06_exact_boundary_category(report_service: ReportService, op_cat_1: User) -> None:
    report = report_service.update_status(0, op_cat_1, "Assigned", note=None)
    assert isinstance(report, Report)
    assert report.id == 10
    assert report.status == "Assigned"
    assert report.reporter == op_cat_1
    assert report.reporter_id == op_cat_1.id

def test_usb07_immediately_below_operator_category(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Assigned", note=None)

def test_usb08_immediately_below_report_category(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Assigned", note=None)

def test_usb09_immediately_above_category(report_service: ReportService, op_cat_1: User) -> None:
    with pytest.raises(ValidationError):
        report_service.update_status(10, op_cat_1, "Assigned", note=None)
