from __future__ import annotations
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from participium.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from participium.models.enums import Role, ReportStatus

def _user(id: int) -> Mock:
        user = Mock()
        user.id = id
        return user


def _photo(filename: str | None = "photo.jpg") -> Mock:
    photo = Mock()
    photo.filename = filename
    photo.content_type = "image/jpeg"
    return photo

class TestListUserReports:
    def test_list_user_reports(self, report_service, mock_report, mock_user):

        fake_reports_list = [mock_report, Mock(id=101, title="Secondo Report")]
        report_service.report_repository.list_user_reports.return_value = fake_reports_list

        result = report_service.list_user_reports(mock_user)
        report_service.report_repository.list_user_reports.assert_called_once_with(mock_user.id)
        assert result == fake_reports_list
        assert len(result) == 2


class TestGetReport:
    def test_get_report_not_found(self, report_service):
        """Il report non viene trovato"""
        report_service.report_repository.get_by_id.return_value = None

        ID_INESISTENTE = 999
        with pytest.raises(NotFoundError) as exc_info:
            report_service.get_report(ID_INESISTENTE)
        assert str(exc_info.value) == "Report not found."
        report_service.report_repository.get_by_id.assert_called_once_with(ID_INESISTENTE)

    def test_get_report_found(self, report_service, mock_report):
        """Il report viene trovato e restituito"""
        report_service.report_repository.get_by_id.return_value = mock_report
        result = report_service.get_report(mock_report.id)

        assert result == mock_report
        report_service.report_repository.get_by_id.assert_called_once_with(mock_report.id)

class TestCreateReport:   
    @pytest.mark.parametrize(
    "category_id, title, description, latitude, longitude, photos, expected_error",
    [
        ("uno", "Titolo", "Desc", 45.4, 9.1, [_photo()], "A valid active category is required."),
        (None, "Titolo", "Desc", 45.4, 9.1, [_photo()], "A valid active category is required."),
        (1, None, "Desc", 45.4, 9.1, [_photo()], "Title and description are required."),
        (1, "Titolo", None, 45.4, 9.1, [_photo()], "Title and description are required."),
        (1, "Titolo", "Desc", None, 9.1, [_photo()], "Latitude and longitude are required."),
        (1, "Titolo", "Desc", "Quaranta", 9.1, [_photo()], "Latitude and longitude must be valid numbers."),
        (1, "Titolo", "Desc", 45.4, 9.1, [], "At least one photo is required."),
    ]
    )
    def test_create_report_validation_errors(
        self,report_service_with_active_category, category_id, title, description, latitude, longitude, photos, expected_error
    ):
        with pytest.raises(ValidationError, match=expected_error):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=category_id,
                title=title,
                description=description,
                latitude=latitude,
                longitude=longitude,
                photos=photos,
                is_anonymous=True,
            )

    def test_crm_10_too_many_photos(self,report_service_with_active_category) -> None:
        photos = [
            _photo(),
            None,
            _photo(filename=None),
            _photo(),
            _photo(),
            _photo(),
        ]

        with pytest.raises(ValidationError, match="A report can contain at most 3 photos."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=9.1900,
                photos=photos,
                is_anonymous=True,
            )


    def test_crm_11_success_single_photo_loop(self,report_service_with_active_category) -> None:
        expected_report = Mock()
        report_service_with_active_category.storage_service.save.return_value = "/img/photo.jpg"
        report_service_with_active_category.get_report = Mock(return_value=expected_report)

        result = report_service_with_active_category.create_report(
            reporter=_user(id=1),
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo()],
            is_anonymous=True,
        )

        assert result == expected_report
        report_service_with_active_category.report_repository.add.assert_called_once()
        report_service_with_active_category.session.flush.assert_called_once()
        report_service_with_active_category.storage_service.save.assert_called_once()
        report_service_with_active_category.report_repository.add_photo.assert_called_once()
        report_service_with_active_category.report_repository.add_status_entry.assert_called_once()
        report_service_with_active_category.session.commit.assert_called_once()


    def test_crm_12_success_multiple_photos_loop(self,report_service_with_active_category) -> None:
        expected_report = Mock()
        report_service_with_active_category.storage_service.save.return_value = "/img/photo.jpg"
        report_service_with_active_category.get_report = Mock(return_value=expected_report)

        result = report_service_with_active_category.create_report(
            reporter=_user(id=1),
            category_id=1,
            title="Buca profonda",
            description="Si segnala una buca di ampie dimensioni",
            latitude=45.4642,
            longitude=9.1900,
            photos=[_photo(), _photo()],
            is_anonymous=True,
        )

        assert result == expected_report
        report_service_with_active_category.report_repository.add.assert_called_once()
        report_service_with_active_category.session.flush.assert_called_once()
        assert report_service_with_active_category.storage_service.save.call_count == 2
        assert report_service_with_active_category.report_repository.add_photo.call_count == 2
        report_service_with_active_category.report_repository.add_status_entry.assert_called_once()
        report_service_with_active_category.session.commit.assert_called_once()


class TestGetAccessibleReport:

    def test_report_is_public_returns_report(self, report_service, mock_report):
        """
        Il report è pubblico. L'accesso deve essere consentito a chiunque.
        """
        mock_report.status = ReportStatus.ASSIGNED
        report_service.report_repository.get_by_id.return_value = mock_report

        result = report_service.get_accessible_report(report_id=mock_report.id, user=None)

        assert result == mock_report

    def test_private_report_and_no_user_raises_authorization_error(self, report_service, mock_report):
        """
        Il report è privato (PENDING_APPROVAL di default) e l'utente è None.
        Deve lanciare un AuthorizationError.
        """
        report_service.report_repository.get_by_id.return_value = mock_report

        with pytest.raises(AuthorizationError) as exc_info:
            report_service.get_accessible_report(report_id=mock_report.id, user=None)

        assert "You do not have access to this report." in str(exc_info.value)

    @pytest.mark.parametrize(
        "user_role, user_id, user_category",
        [
            (Role.CITIZEN, 42, 99),
            (Role.ADMIN, 999, 99),
            (Role.ADMIN, 42, 99),
            (Role.OPERATOR, 999, 5),
        ]
    )
    def test_get_accessible_report_authorized_users(
            self, report_service, mock_report, mock_user, user_role, user_id, user_category):
        """
        Verifica che tutti gli utenti autorizzati superino i controlli degli if
        e ottengano correttamente il report.
        """
        mock_user.role = user_role
        mock_user.id = user_id
        mock_user.category_id = user_category
        report_service.report_repository.get_by_id.return_value = mock_report

        result = report_service.get_accessible_report(report_id=mock_report.id, user=mock_user)

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
    def test_get_accessible_report_logged_user_not_authorized(
            self, report_service, mock_report, mock_user, user_role, user_id, user_category):
        """
        L'utente è loggato ma non ha nessuno dei requisiti. AuthorizationError.
        """
        mock_user.role = user_role
        mock_user.id = user_id
        mock_user.category_id = user_category
        report_service.report_repository.get_by_id.return_value = mock_report

        with pytest.raises(AuthorizationError) as exc_info:
            report_service.get_accessible_report(report_id=mock_report.id, user=mock_user)

        assert "You do not have access to this report." in str(exc_info.value)


class TestFollowReport:
    def test_report_is_not_public_ValidationError(self, report_service, mock_report):
        """
        Il report non è pubblico (PENDING_APPROVAL di default). ValidationError.
        """
        report_service.report_repository.get_by_id.return_value = mock_report

        with pytest.raises(ValidationError) as exc_info:
            report_service.follow_report(report_id=mock_report.id, user=None)

        assert "Only published reports can be followed." in str(exc_info.value)

    def test_follow_report_not_found_raises_error(self, report_service):
        """Il report non esiste. NotFoundError."""
        report_service.report_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc_info:
            report_service.follow_report(report_id=999, user=None)

        assert "Report not found." in str(exc_info.value)

    def test_follow_report_already_following_returns_report(self, report_service, mock_report, mock_user):
        """L'utente segue già il report. Ritorna il report."""
        mock_report.status = ReportStatus.ASSIGNED
        report_service.report_repository.get_by_id.return_value = mock_report
        report_service.report_repository.get_follower.return_value = Mock()

        result = report_service.follow_report(report_id=mock_report.id, user=mock_user)

        assert result == mock_report
        report_service.report_repository.add_follower.assert_not_called()

    def test_follow_report(self, report_service, mock_report, mock_user):
        """L'utente non segue già il report. Aggiunge follow."""
        mock_report.status = ReportStatus.ASSIGNED
        report_service.report_repository.get_by_id.return_value = mock_report
        report_service.report_repository.get_follower.return_value = None

        result = report_service.follow_report(report_id=mock_report.id, user=mock_user)

        assert result == mock_report

        report_service.report_repository.add_follower.assert_called_once()
        called_args, _ = report_service.report_repository.add_follower.call_args
        report_follower_passed = called_args[0]
        assert report_follower_passed.report_id == mock_report.id
        assert report_follower_passed.user_id == mock_user.id

        report_service.session.commit.assert_called_once()
        assert report_service.report_repository.get_by_id.call_count == 2


class TestUnfollowReport:
    def test_unfollow_report_not_found_raises_error(self, report_service):
        """
        Il report cercato non esiste nel database. La funzione deve lanciare NotFoundError.
        """
        report_service.report_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc_info:
            report_service.unfollow_report(report_id=999, user=None)

        assert "Report not found." in str(exc_info.value)

    def test_unfollow_report_not_following(self, report_service, mock_user, mock_report):
        """L'utente non segue il report, non fa modifiche e ritorna il report."""
        report_service.report_repository.get_by_id.return_value = mock_report
        report_service.report_repository.get_follower.return_value = None  #false


        result = report_service.unfollow_report(report_id=mock_report.id, user=mock_user)
        assert result == mock_report
        report_service.report_repository.remove_follower.assert_not_called()
        report_service.session.commit.assert_not_called()

    def test_unfollow_report(self, report_service, mock_user, mock_report):
        """L'utente segue il report, e avviene unfollow."""
        mock_follower = Mock()
        report_service.report_repository.get_follower.return_value = mock_follower
        report_service.report_repository.get_by_id.return_value = mock_report

        result = report_service.unfollow_report(report_id=mock_report.id, user=mock_user)
        assert result == mock_report
        report_service.report_repository.get_follower.assert_called_once_with(mock_report.id, mock_user.id)
        report_service.report_repository.remove_follower.assert_called_once_with(mock_follower)

        report_service.session.commit.assert_called_once()
        assert report_service.report_repository.get_by_id.call_count == 2

class TestListPendingReports:
    def test_list_pending_reports_with_all_filters(self, report_service):
        """Verifica che tutti i filtri vengano estratti"""
        fake_reports = [Mock(id=1, title="Report Pendente 1"), Mock(id=2, title="Report Pendente 2")]
        report_service.report_repository.list_pending.return_value = fake_reports

        filtri_input = {
            "category_id": 5,
            "date_from": "2026-01-01",
            "date_to": "2026-01-31",
            "extra_field": "daignorare"
        }
        result = report_service.list_pending_reports(filtri_input)

        assert result == fake_reports
        assert len(result) == 2
        
        report_service.report_repository.list_pending.assert_called_once_with(
            category_id=5,
            date_from="2026-01-01",
            date_to="2026-01-31"
        )

    def test_list_pending_reports_with_empty_filters(self, report_service):
        """Verifica il comportamento quando il dizionarioè vuoto"""
        report_service.report_repository.list_pending.return_value = []

        result = report_service.list_pending_reports({})

        assert result == []
        report_service.report_repository.list_pending.assert_called_once_with(
            category_id=None,
            date_from=None,
            date_to=None
        )

class TestListOperatorReports:
    def test_list_operator_report(self, report_service, mock_operator):
        """verifica che ruolo e categoria vengano passati correttamente"""
        fake_reports = [Mock(id=201, title="Report Operatore 1")]
        report_service.report_repository.list_operator_reports.return_value = fake_reports

        result = report_service.list_operator_reports(mock_operator)
        assert result == fake_reports
        report_service.report_repository.list_operator_reports.assert_called_once_with(
            Role.OPERATOR, 
            mock_operator.category_id
        )


class TestAssignReport:
    def test_assign_report_user_AuthorizationError(self, mock_user, report_service, mock_report):
        """Il ruolo è cittadino quindi lancia AuthorizationError"""
        with pytest.raises(AuthorizationError) as exc_info:
            report_service.assign_report(mock_report.id, mock_user)
        assert str(exc_info.value) == "Only operators or admins can assign reports."
    
    def test_assign_report_not_pending_approval(self, report_service, mock_operator, mock_report):
        """Il report NON è pending approval, lancia ValidationError"""
        mock_report.status = ReportStatus.ASSIGNED
        report_service.get_report = Mock(return_value=mock_report)
        report_service._ensure_operator_category_access = Mock()
        
        with pytest.raises(ValidationError) as exc_info:
            report_service.assign_report(mock_report.id, mock_operator)
            
        assert str(exc_info.value) == "Only pending reports can be assigned."
        report_service.get_report.assert_called_once_with(mock_report.id)
        report_service._ensure_operator_category_access.assert_called_once_with(mock_operator, mock_report)

    def test_assign_report_success_operator(self, report_service, mock_operator, mock_report):
        """Caso felice con Operatore: lo stato cambia, logga la storia, notifica e committa"""        
        mock_report.category.name = "Verde Pubblico"

        fake_recipients = ["user1@example.com"]
        report_service.get_report = Mock(return_value=mock_report)
        report_service._ensure_operator_category_access = Mock()
        report_service._recipients = Mock(return_value=fake_recipients)
        
        result = report_service.assign_report(mock_report.id, mock_operator)
        
        assert mock_report.status == ReportStatus.ASSIGNED
        report_service.report_repository.add_status_entry.assert_called_once()
        called_args, _ = report_service.report_repository.add_status_entry.call_args
        history_entry = called_args[0]
        assert history_entry.report_id == mock_report.id
        assert history_entry.previous_status == ReportStatus.PENDING_APPROVAL
        assert history_entry.new_status == ReportStatus.ASSIGNED
        assert history_entry.note == "Accepted for category 'Verde Pubblico'."
        assert history_entry.changed_by_id == mock_operator.id
        report_service.notification_service.notify_status_change.assert_called_once_with(
            recipients=fake_recipients,
            report=mock_report,
            body=f"Report #{mock_report.id} has been assigned for handling in category 'Verde Pubblico'."
        )
        
        report_service.session.commit.assert_called_once()
        assert report_service.get_report.call_count == 2
        assert result == mock_report
class TestUpdateStatus:
    def test_update_status_not_in_operator_roles(self, report_service, mock_user, mock_report):
        """L'utente è un cittadino, lancia AuthorizationError"""
        with pytest.raises(AuthorizationError) as exc_info:
            report_service.update_status(mock_report.id, mock_user, "ASSIGNED")
        assert str(exc_info.value) == "Only operators and admins can update report status."
    
    def test_update_status_not_valid_status(self, report_service, mock_operator, mock_report):
        """Lo stato passato come stringa non esiste nell'enum, lancia ValidationError"""
        report_service.get_report = Mock(return_value=mock_report)
        report_service._ensure_operator_category_access = Mock()  
        
        with pytest.raises(ValidationError) as exc_info:
            report_service.update_status(mock_report.id, mock_operator, "NON VALIDO")
        assert str(exc_info.value) == "Invalid report status."

    def test_update_status_rejected_not_note(self, report_service, mock_operator, mock_report):
        """Stato REJECTED ma manca la nota , lancia ValidationError"""
        report_service.get_report = Mock(return_value=mock_report)
        report_service._ensure_operator_category_access = Mock()  
        
        with pytest.raises(ValidationError) as exc_info:
            report_service.update_status(mock_report.id, mock_operator, ReportStatus.REJECTED.value, note=None)
        assert str(exc_info.value) == "Rejection reason is required."

    def test_update_status_sets_rejection_reason_when_rejected(self, report_service, mock_operator, mock_report):
        """ stato è REJECTED, rejection_reason salva la nota"""
        report_service.get_report = Mock(return_value=mock_report)
        report_service._ensure_operator_category_access = Mock()  
        report_service._recipients = Mock(return_value=[])
        
        rejection_note = "Foto non chiara"
        
        with patch("participium.services.report_service.ensure_transition_allowed"):# Sostituiamo provvisoriamente per saltaree il controllo
            report_service.update_status(mock_report.id, mock_operator, ReportStatus.REJECTED.value, note=rejection_note)
            
        assert mock_report.status == ReportStatus.REJECTED
        assert mock_report.rejection_reason == rejection_note
        report_service.session.commit.assert_called_once()

    def test_update_status_resets_rejection_reason_when_not_rejected(self, report_service, mock_operator, mock_report):
        """stato NON è REJECTED, rejection_reason viene resettato a None"""
        mock_report.rejection_reason = "Vecchio rifiuto da sovrascrivere"
        
        report_service.get_report = Mock(return_value=mock_report)
        report_service._ensure_operator_category_access = Mock()  
        report_service._recipients = Mock(return_value=[])
        
        with patch("participium.services.report_service.ensure_transition_allowed"):
            report_service.update_status(mock_report.id, mock_operator, ReportStatus.ASSIGNED.value, note="Preso in carico")
            
        assert mock_report.status == ReportStatus.ASSIGNED
        assert mock_report.rejection_reason is None
        report_service.session.commit.assert_called_once()
    
class TestExportRows:
    def test_export_rows_success(self, report_service, mock_report):
        """I report vengono estratti, formattati correttamente in dict e restituiti"""
        faked_date = datetime(2026, 5, 19, 12, 0, 0)
        mock_report.created_at = faked_date
        mock_report.category.name = "Strade"
        report_service.list_public_reports = Mock(return_value=[mock_report])

        result = report_service.export_rows(
            category_id=5,
            status=ReportStatus.PENDING_APPROVAL,
            date_from=faked_date,
            sort="asc"
        )

        report_service.list_public_reports.assert_called_once_with(
            category_id=5,
            status=ReportStatus.PENDING_APPROVAL,
            date_from=faked_date,
            date_to=None,
            sort="asc"
        )
        assert len(result) == 1
        expected_row = {
            "id": mock_report.id,
            "title": mock_report.title,
            "category": "Strade",
            "status": "Pending Approval",
            "created_at": "2026-05-19T12:00:00", 
            "latitude": mock_report.latitude,
            "longitude": mock_report.longitude,
        }
        assert result[0] == expected_row

    def test_export_rows_empty(self, report_service):
        """Se non ci sono report estratti, restituisce una lista vuota"""
        report_service.list_public_reports = Mock(return_value=[])

        result = report_service.export_rows(category_id=1)


        assert result == []
        report_service.list_public_reports.assert_called_once()


class TestIsPublic:
    def test_is_public_true(self, mock_report, report_service):
        """Restituisce True se lo stato è tra quelli pubblici"""
        mock_report.status = ReportStatus.ASSIGNED
        
        result = report_service.is_public(mock_report)
        assert result is True

    def test_is_public_false(self, mock_report,report_service):
        """Restituisce False se lo stato NON è tra quelli pubblici"""
        
        result = report_service.is_public(mock_report)
        assert result is False


class TestRecipients:
    def test_recipients_includes_reporter_and_followers(self, report_service, mock_report, mock_user):
        mock_report.reporter = mock_user
        
        mock_follower_1 = Mock(user=Mock(id=10, email="follower1@test.com"))
        mock_follower_2 = Mock(user=Mock(id=11, email="follower2@test.com"))
        mock_report.followers = [mock_follower_1, mock_follower_2]

        result = report_service._recipients(mock_report)

        assert len(result) == 3
        assert mock_user in result
        assert mock_follower_1.user in result
        assert mock_follower_2.user in result

    def test_recipients_filters_out_none_values(self, report_service, mock_report):
        mock_report.reporter = None

        mock_follower_valido = Mock(user=Mock(id=10, email="valido@test.com"))
        mock_follower_corrotto = Mock(user=None)
        
        mock_report.followers = [mock_follower_valido, mock_follower_corrotto]

        result = report_service._recipients(mock_report)

        assert len(result) == 1
        assert result[0] == mock_follower_valido.user

class TestEnsureOperatorCategoryAccess:
    def test_access_granted_for_admin(self, report_service, mock_admin, mock_report):
        """Un utente con ruolo ADMIN ha sempre accesso, a prescindere dalla categoria."""

        report_service._ensure_operator_category_access(mock_admin, mock_report)

    def test_access_denied_for_non_operator_roles(self, report_service, mock_user, mock_report):
        """Un utente CITIZEN lancia AuthorizationError."""
        with pytest.raises(AuthorizationError) as exc_info:
            report_service._ensure_operator_category_access(mock_user, mock_report)

        assert "Only operators and admins can manage reports." in str(exc_info.value)

    def test_access_denied_for_operator_with_different_category(self, report_service, mock_operator, mock_report):
        """Un operator con categoria diversa """
        mock_operator.category_id = 6  # category id del report invece 5 DEFAULT

        with pytest.raises(AuthorizationError) as exc_info:
            report_service._ensure_operator_category_access(mock_operator, mock_report)

        assert "This report does not belong to your category." in str(exc_info.value)

    def test_access_granted_for_operator_with_same_category(self, report_service, mock_operator, mock_report):
        """ operator con la stessa categoria del report """
        mock_operator.category_id = 5
        mock_report.category_id = 5

        report_service._ensure_operator_category_access(mock_operator, mock_report)

class TestListPublicReports:
    def test_list_public_reports_with_all_filters(self, report_service, mock_report):
        """Verifica che tutti i filtri e l'ordinamento vengano passati correttamente al repository con public_only=True."""
        fake_reports = [mock_report]
        report_service.report_repository.list_reports.return_value = fake_reports

        faked_date_from = datetime(2026, 1, 1, 0, 0, 0)
        faked_date_to = datetime(2026, 1, 31, 23, 59, 59)

        result = report_service.list_public_reports(
            category_id=5,
            status=ReportStatus.ASSIGNED,
            date_from=faked_date_from,
            date_to=faked_date_to,
            sort="asc"
        )

        assert result == fake_reports
        report_service.report_repository.list_reports.assert_called_once_with(public_only=True,category_id=5,status=ReportStatus.ASSIGNED,date_from=faked_date_from,date_to=faked_date_to,sort="asc"
        )

    def test_list_public_reports_with_defaults(self, report_service):
        """Verifica il comportamento con i parametri di default (nessun filtro e sort desc)."""
        report_service.report_repository.list_reports.return_value = []

        result = report_service.list_public_reports()

        assert result == []
        report_service.report_repository.list_reports.assert_called_once_with(public_only=True,category_id=None,status=None,date_from=None,date_to=None,sort="desc"
        )


    

   
