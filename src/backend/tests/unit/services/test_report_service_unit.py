from __future__ import annotations
from unittest.mock import Mock

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
    def test_crm_01_malformed_category_id(self, report_service) -> None:
        with pytest.raises(ValidationError, match="A valid active category is required."):
            report_service.create_report(
                reporter=_user(id=1),
                category_id="uno",
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_02_none_category_id(self,report_service) -> None:
        with pytest.raises(ValidationError, match="A valid active category is required."):
            report_service.create_report(
                reporter=_user(id=1),
                category_id=None,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_03_inactive_category(self,report_service) -> None:
        report_service.category_repository.get_by_id.return_value = Mock(id=1, is_active=False)

        with pytest.raises(ValidationError, match="A valid active category is required."):
            report_service.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_04_missing_title(self,report_service_with_active_category) -> None:
        with pytest.raises(ValidationError, match="Title and description are required."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title=None,
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_05_missing_description(self,report_service_with_active_category) -> None:
        with pytest.raises(ValidationError, match="Title and description are required."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description=None,
                latitude=45.4642,
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_06_missing_latitude(self,report_service_with_active_category) -> None:
        with pytest.raises(ValidationError, match="Latitude and longitude are required."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=None,
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_07_missing_longitude(self,report_service_with_active_category) -> None:
        with pytest.raises(ValidationError, match="Latitude and longitude are required."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=None,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_08_malformed_coordinates(self,report_service_with_active_category) -> None:
        with pytest.raises(ValidationError, match="Latitude and longitude must be valid numbers."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude="Quaranta",
                longitude=9.1900,
                photos=[_photo(), _photo()],
                is_anonymous=True,
            )


    def test_crm_09_no_photos(self,report_service_with_active_category) -> None:
        with pytest.raises(ValidationError, match="At least one photo is required."):
            report_service_with_active_category.create_report(
                reporter=_user(id=1),
                category_id=1,
                title="Buca profonda",
                description="Si segnala una buca di ampie dimensioni",
                latitude=45.4642,
                longitude=9.1900,
                photos=[],
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
        report_service_with_active_category.report_repository.get_by_id.return_value = expected_report

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
        report_service_with_active_category.report_repository.get_by_id.return_value = expected_report

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


