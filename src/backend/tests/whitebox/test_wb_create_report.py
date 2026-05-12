from __future__ import annotations

from unittest.mock import Mock

import pytest

from participium.services.report_service import ReportService
from participium.core.exceptions import ValidationError

pytestmark = pytest.mark.whitebox

def _user(id: int) -> Mock:
    user = Mock()
    user.id = id
    return user

def _photo(filename: str | None = "photo.jpg") -> Mock:
    photo = Mock()
    photo.filename = filename
    photo.content_type = "image/jpeg"
    return photo

@pytest.fixture
def report_service_bundle() -> dict[str, object]:
    """Bundle base con tutti i mock iniettati nel servizio."""
    session = Mock()
    category_repository = Mock()
    report_repository = Mock()
    storage_service = Mock()
    
    service = ReportService(
        session=session,
        category_repository=category_repository,
        report_repository=report_repository,
        storage_service=storage_service,
    )
    service.get_report = Mock()
    
    return {
        "service": service,
        "session": session,
        "category_repository": category_repository,
        "report_repository": report_repository,
        "storage_service": storage_service,
    }

@pytest.fixture
def active_category_bundle(report_service_bundle: dict[str, object]) -> dict[str, object]:
    """Configura CATEGORY_REPOSITORY_ACTIVE per i test dal CRM-04 in poi."""
    category = Mock(id=1, is_active=True)
    report_service_bundle["category_repository"].get_by_id.return_value = category
    return report_service_bundle


def test_crm_01_malformed_category_id(report_service_bundle: dict[str, object]) -> None:
    service = report_service_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="A valid active category is required."):
        service.create_report(
            reporter=reporter,
            category_id="uno",
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_02_none_category_id(report_service_bundle: dict[str, object]) -> None:
    service = report_service_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="A valid active category is required."):
        service.create_report(
            reporter=reporter,
            category_id=None,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_03_inactive_category(report_service_bundle: dict[str, object]) -> None:
    service = report_service_bundle["service"]
    category_repository = report_service_bundle["category_repository"]
    
    category = Mock(id=1, is_active=False)
    category_repository.get_by_id.return_value = category
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="A valid active category is required."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_04_missing_title(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="Title and description are required."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title=None,
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_05_missing_description(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="Title and description are required."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description=None,
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_06_missing_latitude(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="Latitude and longitude are required."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=None,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_07_missing_longitude(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="Latitude and longitude are required."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=None,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_08_malformed_coordinates(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="Latitude and longitude must be valid numbers."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude="Quaranta",
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

def test_crm_09_no_photos(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    with pytest.raises(ValidationError, match="At least one photo is required."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[],
            is_anonymous=True,
        )

def test_crm_10_too_many_photos(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    reporter = _user(id=1)
    
    photos = [
        _photo(), 
        None, 
        _photo(filename=None), 
        _photo(), 
        _photo(), 
        _photo()
    ]
    
    with pytest.raises(ValidationError, match="A report can contain at most 3 photos."):
        service.create_report(
            reporter=reporter,
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=photos,
            is_anonymous=True,
        )

def test_crm_11_success_single_photo_loop(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    session = active_category_bundle["session"]
    report_repository = active_category_bundle["report_repository"]
    storage_service = active_category_bundle["storage_service"]
    
    storage_service.save.return_value = "/img/photo.jpg"
    expected_report = Mock()
    service.get_report.return_value = expected_report
    
    reporter = _user(id=1)
    
    result = service.create_report(
        reporter=reporter,
        category_id=1,
        title="Buca profonda",
        description="Si segnala una buca di ampie dimensioni",
        latitude=45.4642,
        longitude=9.1900,
        photos=[_photo()],
        is_anonymous=True,
    )
    
    assert result == expected_report
    report_repository.add.assert_called_once()
    session.flush.assert_called_once()
    storage_service.save.assert_called_once()
    report_repository.add_photo.assert_called_once()
    report_repository.add_status_entry.assert_called_once()
    session.commit.assert_called_once()

def test_crm_12_success_multiple_photos_loop(active_category_bundle: dict[str, object]) -> None:
    service = active_category_bundle["service"]
    session = active_category_bundle["session"]
    report_repository = active_category_bundle["report_repository"]
    storage_service = active_category_bundle["storage_service"]
    
    storage_service.save.return_value = "/img/photo.jpg"
    expected_report = Mock()
    service.get_report.return_value = expected_report
    
    reporter = _user(id=1)
    
    result = service.create_report(
        reporter=reporter,
        category_id=1,
        title="Buca profonda",
        description="Si segnala una buca di ampie dimensioni",
        latitude=45.4642,
        longitude=9.1900,
        photos=[_photo(), _photo()],
        is_anonymous=True,
    )
    
    assert result == expected_report
    report_repository.add.assert_called_once()
    session.flush.assert_called_once()
    assert storage_service.save.call_count == 2
    assert report_repository.add_photo.call_count == 2
    report_repository.add_status_entry.assert_called_once()
    session.commit.assert_called_once()