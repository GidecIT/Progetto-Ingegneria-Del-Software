from __future__ import annotations

import pytest

from datetime import datetime
from participium.core.utils import parse_date

def test_dt01_valid_date() -> None:
    result = parse_date("2002-12-31")
    assert isinstance(result, datetime)
    assert result == datetime(2002, 12, 31)

def test_dt02_value_none() -> None:
    assert parse_date(None) is None

def test_dt03_value_empty_string() -> None:
    assert parse_date("") is None

def test_dt04_invalid_month_too_high() -> None:
    with pytest.raises(ValueError):
        parse_date("2056-31-04")

def test_dt05_invalid_month_zero() -> None:
    with pytest.raises(ValueError):
        parse_date("1980-00-04")

def test_dt06_wrong_separator() -> None:
    with pytest.raises(ValueError):
        parse_date("1998/03/04")

def test_dt07_invalid_day_too_high() -> None:
    with pytest.raises(ValueError):
        parse_date("2020-02-34")

def test_dtb01_leap_year_valid() -> None:
    result = parse_date("2024-02-29")
    assert result == datetime(2024, 2, 29)

def test_dtb02_leap_year_invalid_above() -> None:
    with pytest.raises(ValueError):
        parse_date("2024-02-30")

def test_dtb03_non_leap_year_invalid() -> None:
    with pytest.raises(ValueError):
        parse_date("2023-02-29")

def test_dtb04_last_day_of_year() -> None:
    result = parse_date("2024-12-31")
    assert result == datetime(2024, 12, 31)

def test_dtb05_month_overflow() -> None:
    with pytest.raises(ValueError):
        parse_date("2024-13-01")

def test_dtb06_month_underflow() -> None:
    with pytest.raises(ValueError):
        parse_date("2024-00-01")

def test_dtb07_month_with_30_days_exact() -> None:
    result = parse_date("2024-04-30")
    assert result == datetime(2024, 4, 30)

def test_dtb08_month_with_30_days_above() -> None:
    with pytest.raises(ValueError):
        parse_date("2024-04-31")

def test_dtb09_day_zero() -> None:
    with pytest.raises(ValueError):
        parse_date("2024-04-00")