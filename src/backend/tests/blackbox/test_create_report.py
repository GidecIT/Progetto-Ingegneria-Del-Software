from __future__ import annotations

import pytest
from werkzeug.datastructures import FileStorage
from participium.core.exceptions import ValidationError
from participium.models.report import Report
from participium.models.user import User
from participium.services.report_service import ReportService


VALID_REPORTER = User(id=1, username="mario_r", email="mario_r@example.com", is_active=True, is_email_verified=True)
VALID_PHOTO = FileStorage(filename="foto_buca.jpg")
VALID_PHOTO2 = FileStorage(filename="foto_buca2.jpg")
VALID_PHOTO3 = FileStorage(filename="foto_buca3.jpg")
VALID_PHOTO4 = FileStorage(filename="foto_buca4.jpg")
INVALID_PHOTO = FileStorage(filename="") 

@pytest.fixture
def seed_create_report_data(db_session) -> None:
    # Popola il sistema con i dati nessesari per `create_report`.
    #
	# Le categorie 0-8 sono valide
    # categoria 4 è valida e attiva
	# categoria 5 è valida ma inattiva
    pass

@pytest.mark.skip(reason="Disabled")
@pytest.mark.parametrize(
	"reporter, category_id, title, description, latitude, longitude, photos, is_anonymous, expected_exception",
	[
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CR1
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], True, None),   # CR2
		(VALID_REPORTER, 5, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], True, ValidationError),   # CR3
		(VALID_REPORTER, None, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], True, ValidationError),   # CR4
		(VALID_REPORTER, "", "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),   # CR5
		(VALID_REPORTER, "df", "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], True, ValidationError),   # CR6
		(VALID_REPORTER, 4, "", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),   # CR7
		(VALID_REPORTER, 4, "Buca profonda", None , 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),   # CR8
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710 , "", [VALID_PHOTO], True , ValidationError),   # CR9
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", "Quarantacinque" , 7.6856, [VALID_PHOTO], False , ValidationError),   # CR10
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710 , 7.6856, [], False , ValidationError),   # CR11
        # Boundary cases per category_id
		(VALID_REPORTER, 0, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CRB01
		(VALID_REPORTER, 8, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CRB02
		(VALID_REPORTER, -1, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB04
		(VALID_REPORTER, 9, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB05
		# Boundary cases per title e description
		(VALID_REPORTER, 4, "a", "a", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CRB06
		(VALID_REPORTER, 4, "", "a", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB07
		(VALID_REPORTER, 4, "a", "", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB08
		# Boundary cases per latitude/longitude
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 0.0, 0.0, [VALID_PHOTO], False, None),  # CRB09
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", "", 0.0, [VALID_PHOTO], False, ValidationError),  # CRB10
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, "", [VALID_PHOTO], False, ValidationError),  # CRB11
		# Boundary cases per photos
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CR01
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [], False, ValidationError),  # CR11
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO, VALID_PHOTO2, VALID_PHOTO3], False, None),  # CRB12
		(VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO, VALID_PHOTO2, VALID_PHOTO3, VALID_PHOTO4], False, ValidationError),  # CRB13
	],
)
def test_create_report(reporter, category_id, title, description, latitude, longitude, photos, is_anonymous, expected_exception, seed_create_report_data):
	report_service = ReportService()
	if expected_exception:
		with pytest.raises(expected_exception):
			report_service.create_report(reporter, category_id, title, description, latitude, longitude, photos, is_anonymous)
	else:
		result = report_service.create_report(reporter, category_id, title, description, latitude, longitude, photos, is_anonymous)
		assert isinstance(result, Report)