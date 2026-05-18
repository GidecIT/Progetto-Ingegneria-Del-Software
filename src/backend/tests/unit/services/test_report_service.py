from __future__ import annotations

import pytest
from participium.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from participium.models.enums import ReportStatus, Role 

# get_accesible_report
class TestGetAccesibleReport:
    
    def test_report_is_public_returns_report(self, report_service, mock_report):
        """
        Il report è pubblico. L'accesso deve essere consentito a chiunque.
        """
      
        report_service.report_repository.get_by_id.return_value = mock_report
        
        mock_report.status = ReportStatus.RESOLVED 

        result = report_service.get_accessible_report(report_id=100, user=None)

        assert result == mock_report

    def test_private_report_and_no_user_raises_authorization_error(self, report_service, mock_report):
        """
        Il report è privato e l'utente è None. Deve lanciare un AuthorizationError.
        """
        report_service.report_repository.get_by_id.return_value = mock_report


        with pytest.raises(AuthorizationError) as exc_info:
            report_service.get_accessible_report(report_id=100, user=None)
        
        assert "You do not have access to this report." in str(exc_info.value)

    @pytest.mark.parametrize(
        "user_role, user_id, user_category",
        [
            (Role.CITIZEN, 42, 99,),
            (Role.ADMIN, 999, 99, ),
            (Role.ADMIN, 42, 99),
            (Role.OPERATOR, 999, 5, ),
        ]
    )
    def test_get_accessible_report_authorized_users(
        self, report_service, mock_report, mock_user, user_role, user_id, user_category):
        """
        Verifica che tutti gli utenti autorizzati superino i controlli degli if e ottengano correttamente il report.
        """
        
        report_service.report_repository.get_by_id.return_value = mock_report

        mock_user.role = user_role
        mock_user.id = user_id
        mock_user.category_id = user_category

        result = report_service.get_accessible_report(report_id=100, user=mock_user)

        assert result == mock_report

    def test_get_accessible_report_not_found_raises_error(self, report_service):
        """
        Il report cercato non esiste nel database. La funzione deve lanciare NotFoundError.
        """
        report_service.report_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc_info:
            report_service.get_accessible_report(report_id=999, user=None)
        
        assert "Report not found." in str(exc_info.value)

    @pytest.mark.parametrize(
    "user_role, user_id, user_category",
        [
            (Role.CITIZEN, 999, 99),  
            (Role.OPERATOR, 999, 10), 
        ]
    )
    def test_get_accessible_report_logged_user_not_authorized(self, report_service, mock_report, mock_user, user_role, user_id, user_category):
        """
        L'utente è loggato ma non ha nessuno dei requisiti. AuthorizationError .
        """
        report_service.report_repository.get_by_id.return_value = mock_report

        mock_user.role = user_role
        mock_user.id = user_id
        mock_user.category_id = user_category

        with pytest.raises(AuthorizationError) as exc_info:
            report_service.get_accessible_report(report_id=100, user=mock_user)
        
        assert "You do not have access to this report." in str(exc_info.value)




    