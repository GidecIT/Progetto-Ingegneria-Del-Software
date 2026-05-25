import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, request
from participium.routes.api import _payload, _as_bool, _parse_report_status, _report_filters
from participium.core.exceptions import ValidationError
from participium.models.enums import ReportStatus

def test_payload():
    app = Flask(__name__)
    with app.test_request_context(json={"key": "value"}):
        assert _payload() == {"key": "value"}
    
    with app.test_request_context():
        # Quando non c'è JSON, request.get_json() ritorna None
        assert _payload() == {}

def test_as_bool():
    assert _as_bool("true") is True
    assert _as_bool("1") is True
    assert _as_bool("yes") is True
    assert _as_bool(True) is True
    assert _as_bool("false") is False
    assert _as_bool("0") is False
    assert _as_bool(None) is False
    assert _as_bool(None, default=True) is True

def test_parse_report_status():
    assert _parse_report_status("Pending Approval") == ReportStatus.PENDING_APPROVAL
    # Test case sensitivity: Il costruttore di Enum in Python è case-sensitive
    # se non diversamente implementato. _parse_report_status chiama ReportStatus(status_value)
    # quindi "PENDING APPROVAL" fallirà se il valore è "Pending Approval"
    with pytest.raises(ValidationError):
        _parse_report_status("PENDING APPROVAL")
    with pytest.raises(ValidationError):
        _parse_report_status("invalid")
    assert _parse_report_status(None) is None
    assert _parse_report_status("") is None

def test_report_filters():
    app = Flask(__name__)
    with app.test_request_context(query_string="status=Pending Approval&category_id=1"):
        filters = _report_filters()
        assert filters["status"] == ReportStatus.PENDING_APPROVAL
        assert filters["category_id"] == 1
    
    with app.test_request_context(query_string="category_id=invalid"):
        filters = _report_filters()
        assert filters["category_id"] is None
