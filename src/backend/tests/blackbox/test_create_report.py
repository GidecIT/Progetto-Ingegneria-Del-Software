from __future__ import annotations

from unittest.mock import Mock
import pytest
from werkzeug.datastructures import FileStorage

from participium.core.exceptions import ValidationError
from participium.models.report import Report
from participium.models.user import User
from participium.services.report_service import ReportService

VALID_REPORTER = User(id=1, username="mario_r", email="mario_r@example.com", is_active=True, is_email_verified=True)
VALID_PHOTO = FileStorage(filename="foto_buca.jpg", content_type="image/jpeg")
VALID_PHOTO2 = FileStorage(filename="foto_buca2.jpg", content_type="image/jpeg")
VALID_PHOTO3 = FileStorage(filename="foto_buca3.jpg", content_type="image/jpeg")
VALID_PHOTO4 = FileStorage(filename="foto_buca4.jpg", content_type="image/jpeg")


@pytest.fixture
def mock_dependencies():
    """Crea i Mock per le dipendenze interne del servizio senza sovrascrivere il servizio stesso."""
    category_repo = Mock()
    report_repo = Mock()
    storage_service = Mock()
    session = Mock()

    # Configura il comportamento di category_repository.get_by_id
    # Categorie 1-9 esistenti. 5 è inattiva, le altre attive.
    def mock_get_category(cat_id):
        if cat_id is None or not isinstance(cat_id, int):
            return None
        if 1 <= cat_id <= 9:
            category = Mock()
            category.id = cat_id
            category.is_active = (cat_id != 5)
            return category
        return None

    category_repo.get_by_id.side_effect = mock_get_category
    
    # Configura lo storage service per simulare il salvataggio delle foto
    storage_service.save.return_value = "uploads/foto_buca_saved.jpg"

    return {
        "session": session,
        "report_repository": report_repo,
        "category_repository": category_repo,
        "storage_service": storage_service
    }


@pytest.fixture
def report_service(mock_dependencies) -> ReportService:
    """Inizializza il ReportService REALE iniettando i finti repository."""
    service = ReportService(
        session=mock_dependencies["session"],
        report_repository=mock_dependencies["report_repository"],
        category_repository=mock_dependencies["category_repository"],
        storage_service=mock_dependencies["storage_service"]
    )
    
    # Mockiamo l'ultimo metodo interno del servizio (get_report) chiamato prima del return
    # in modo da fargli restituire un oggetto Report finale finto senza crashare
    def mock_get_report(report_id):
        return Report(id=report_id, title="Mocked", description="Mocked", latitude=0.0, longitude=0.0)
        
    service.get_report = mock_get_report
    return service


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
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710 , None, [VALID_PHOTO], True , ValidationError),   # CR9 
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", "Quarantacinque" , 7.6856, [VALID_PHOTO], False , ValidationError),   # CR10
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710 , 7.6856, [], False , ValidationError),   # CR11 

        # Boundary cases per category_id
        (VALID_REPORTER, 1, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CRB01 
        (VALID_REPORTER, 9, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CRB02 
        (VALID_REPORTER, 0, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB03 
        (VALID_REPORTER, 10, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB04 

        # Boundary cases per title e description
        (VALID_REPORTER, 4, "a", "a", 45.0710, 7.6856, [VALID_PHOTO], False, None),  # CRB05 
        (VALID_REPORTER, 4, "", "a", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB06
        (VALID_REPORTER, 4, "a", "", 45.0710, 7.6856, [VALID_PHOTO], False, ValidationError),  # CRB07

        # Boundary cases per latitude/longitude
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 0.0, 0.0, [VALID_PHOTO], False, None),  # CRB08
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", "", 0.0, [VALID_PHOTO], False, ValidationError),  # CRB09
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, "", [VALID_PHOTO], False, ValidationError),  # CRB10

        # Boundary cases per photos
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO, VALID_PHOTO2, VALID_PHOTO3], False, None),  # CRB11 
        (VALID_REPORTER, 4, "Buca profonda", "Buca profonda in piazza Castello", 45.0710, 7.6856, [VALID_PHOTO, VALID_PHOTO2, VALID_PHOTO3, VALID_PHOTO4], False, ValidationError),  # CRB12 
    ],
)
def test_create_report(report_service, mock_dependencies, reporter, category_id, title, description, latitude, longitude, photos, is_anonymous, expected_exception):
    """Esegue la FUNZIONE REALE passando i parametri del test case."""
    
    if expected_exception:
        with pytest.raises(expected_exception):
            # Questa chiamata ora attraversa TUTTA la logica reale del tuo file sorgente
            report_service.create_report(
                reporter=reporter,
                category_id=category_id,
                title=title,
                description=description,
                latitude=latitude,
                longitude=longitude,
                photos=photos,
                is_anonymous=is_anonymous
            )
    else:
        result = report_service.create_report(
            reporter=reporter,
            category_id=category_id,
            title=title,
            description=description,
            latitude=latitude,
            longitude=longitude,
            photos=photos,
            is_anonymous=is_anonymous
        )
        
        # Verifichiamo che l'interazione con l'infrastruttura sottostante sia avvenuta correttamente
        assert mock_dependencies["report_repository"].add.called
        assert mock_dependencies["session"].flush.called
        assert mock_dependencies["session"].commit.called
        assert mock_dependencies["storage_service"].save.call_count == len(photos)