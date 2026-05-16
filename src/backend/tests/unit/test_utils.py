from __future__ import annotations

import pytest
from datetime import datetime
from participium.core.utils import build_csv, utcnow, parse_date

pytestmark = pytest.mark.unit

def test_utcnow():
    res = utcnow()
    assert isinstance(res, datetime)

def test_parse_date_logic():
    assert parse_date(None) is None
    assert parse_date("") is None
    assert parse_date("2024-01-01") == datetime(2024, 1, 1)

def test_build_csv_standard():
    rows = [{"id": 1, "name": "Alpha"}, {"id": 2, "name": "Beta"}]
    fields = ["id", "name"]
    res = build_csv(rows, fields)
    assert res == "id,name\r\n1,Alpha\r\n2,Beta\r\n"

def test_build_csv_empty_rows():
    fields = ["id", "name"]
    res = build_csv([], fields)
    assert res == "id,name\r\n"

def test_build_csv_special_chars():
    rows = [{"val": "A,B"}, {"val": '"Quote"'}]
    fields = ["val"]
    res = build_csv(rows, fields)
    assert '"A,B"' in res
    assert '"""Quote"""' in res
