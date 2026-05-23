from __future__ import annotations
from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest

from participium.models.enums import ReportStatus, Role
from participium.models.user import User
from participium.models.message import Message
from participium.models.token import EmailVerificationToken
from participium.core.exceptions import AuthorizationError, NotFoundError, ValidationError

@pytest.mark.integration
class TestListPublicReportsIntegration:

    def test_list_public_reports_excludes_private_statuses(self, report_service, populated_db):
        results = report_service.list_public_reports()
        report_titles = [r.title for r in results]
        assert "Target Cat A" in report_titles
        assert "Privato Approvazione" not in report_titles
        for report in results:
            assert report.status != ReportStatus.PENDING_APPROVAL

    def test_list_public_reports_applies_category_filter(self, report_service, populated_db, test_category):
        results = report_service.list_public_reports(category_id=test_category.id)
        report_titles = [r.title for r in results]
        assert "Target Cat A" in report_titles
        assert "Escluso Cat B" not in report_titles
        assert all(r.category_id == test_category.id for r in results)

    def test_list_public_reports_applies_date_range_filters(self, report_service, populated_db):
        date_from = datetime.utcnow() - timedelta(days=2)
        results = report_service.list_public_reports(date_from=date_from)
        report_titles = [r.title for r in results]
        assert "Target Cat A" in report_titles
        assert "Escluso Cat B" not in report_titles

    def test_list_public_reports_sorting_order(self, report_service, populated_db):
        results_desc = report_service.list_public_reports(sort="desc")
        assert results_desc[0].title == "Target Cat A"
        assert results_desc[1].title == "Escluso Cat B"
        results_asc = report_service.list_public_reports(sort="asc")
        assert results_asc[0].title == "Escluso Cat B"
        assert results_asc[1].title == "Target Cat A"

    def test_list_public_reports_loads_relationships_correctly(self, report_service, populated_db, test_user):
        results = report_service.list_public_reports()
        target_report = next(r for r in results if r.title == "Target Cat A")
        assert target_report.reporter_id == test_user.id
        assert target_report.reporter.email == test_user.email

class TestListUserReports:
    def test_list_user_reports_returns_correct_reports(self, report_service, populated_db, test_user):
        reports = report_service.list_user_reports(test_user)
        assert len(reports) == 3
        assert all(r.reporter_id == test_user.id for r in reports)

    def test_list_user_reports_empty_for_new_user(self, report_service, other_user):
        reports = report_service.list_user_reports(other_user)
        assert len(reports) == 0

class TestGetReport:
    def test_get_existing_report(self, report_service, populated_db):
        report_id = populated_db["report_pubblico_a"].id
        report = report_service.get_report(report_id)
        assert report.id == report_id

    def test_get_non_existent_report_raises_error(self, report_service):
        with pytest.raises(NotFoundError, match="Report not found."):
            report_service.get_report(9999)

class TestGetAccessibleReport:
    def test_public_report_accessible_by_anyone(self, report_service, populated_db):
        report = populated_db["report_pubblico_a"]
        assert report_service.get_accessible_report(report.id) == report

    def test_private_report_accessible_by_owner(self, report_service, populated_db, test_user):
        report = populated_db["report_privato"]
        assert report_service.get_accessible_report(report.id, user=test_user) == report

    def test_private_report_denied_to_stranger(self, report_service, populated_db, other_user):
        report = populated_db["report_privato"]
        with pytest.raises(AuthorizationError):
            report_service.get_accessible_report(report.id, user=other_user)

    def test_admin_can_access_anything(self, report_service, populated_db, admin_user):
        report = populated_db["report_privato"]
        assert report_service.get_accessible_report(report.id, user=admin_user) == report

    def test_private_report_denied_when_user_is_none(self, report_service, populated_db):
        report = populated_db["report_privato"]
        with pytest.raises(AuthorizationError, match="You do not have access to this report."):
            report_service.get_accessible_report(report.id, user=None)

    def test_operator_can_access_report_of_same_category(self, report_service, populated_db, other_user, db_session):
        report = populated_db["report_privato"]
        other_user.role = Role.OPERATOR
        other_user.category_id = report.category_id
        db_session.commit()
        accessible_report = report_service.get_accessible_report(report.id, user=other_user)
        assert accessible_report == report

class TestCreateReport:
    def test_create_report_success(self, report_service, test_user, test_category, mock_file, media_root):
        # Usiamo mock_file() per creare un file reale in memoria
        report = report_service.create_report(
            reporter=test_user,
            category_id=test_category.id,  
            title="Nuova Buca",
            description="Buca pericolosa in mezzo alla carreggiata",
            latitude=45.0,
            longitude=9.0,
            photos=[mock_file(filename="test.jpg")]
        )
        assert report.id is not None
        assert report.status == ReportStatus.PENDING_APPROVAL
        assert len(report.photos) == 1
        # Verifica che il file sia stato effettivamente salvato su disco nella media_root
        assert (media_root / report.photos[0].file_path).exists()

    def test_create_report_validation_errors(self, report_service, test_user, test_category, mock_file):
        with pytest.raises(ValidationError, match="Title and description are required."):
            report_service.create_report(
                reporter=test_user,
                category_id=test_category.id,
                title="", description="",
                latitude=45.0, longitude=9.0,
                photos=[mock_file()]
            )

    def test_create_report_invalid_photos_count(self, report_service, test_user, test_category, mock_file):
        # Usiamo list comprehension con chiamata ()
        too_many_photos = [mock_file(filename=f"test{i}.jpg") for i in range(4)]        
        with pytest.raises(ValidationError, match="at most 3 photos"):
            report_service.create_report(
                reporter=test_user,
                category_id=test_category.id,
                title="Titolo Valido", description="Descrizione Valida",
                latitude=1.0, longitude=1.0,
                photos=too_many_photos
            )

    def test_create_report_invalid_category_id_type(self, report_service, test_user, mock_file):
        with pytest.raises(ValidationError, match="A valid active category is required."):
            report_service.create_report(
                reporter=test_user,
                category_id="not_a_number",
                title="Titolo", description="Descrizione",
                latitude=45.0, longitude=9.0,
                photos=[mock_file()]
            )

    def test_create_report_non_existent_or_inactive_category(self, report_service, test_user, mock_file):
        with pytest.raises(ValidationError, match="A valid active category is required."):
            report_service.create_report(
                reporter=test_user,
                category_id=99999,
                title="Titolo", description="Descrizione",
                latitude=45.0, longitude=9.0,
                photos=[mock_file()]
            )

    def test_create_report_missing_coordinates(self, report_service, test_user, test_category, mock_file):
        with pytest.raises(ValidationError, match="Latitude and longitude are required."):
            report_service.create_report(
                reporter=test_user,
                category_id=test_category.id,
                title="Titolo", description="Descrizione",
                latitude=None, longitude=9.0,
                photos=[mock_file()]
            )

    def test_create_report_invalid_coordinates_type(self, report_service, test_user, test_category, mock_file):
        with pytest.raises(ValidationError, match="Latitude and longitude must be valid numbers."):
            report_service.create_report(
                reporter=test_user,
                category_id=test_category.id,
                title="Titolo", description="Descrizione",
                latitude="stringa", longitude=9.0,
                photos=[mock_file()]
            )

    def test_create_report_empty_photos_list(self, report_service, test_user, test_category):
        with pytest.raises(ValidationError, match="At least one photo is required."):
            report_service.create_report(
                reporter=test_user,
                category_id=test_category.id,
                title="Titolo Valido", description="Descrizione Valida",
                latitude=45.0, longitude=9.0,
                photos=[]  
            )

    def test_create_report_empty_photos_list(self, report_service, test_user, test_category):
        """Copre: if not valid_photos: raise ValidationError("At least one photo is required.")"""
        with pytest.raises(ValidationError, match="At least one photo is required."):
            report_service.create_report(
                reporter=test_user,
                category_id=test_category.id,
                title="Titolo Valido",
                description="Descrizione Valida",
                latitude=45.0,
                longitude=9.0,
                photos=[]  
            )


class TestFollowReport:

    def test_follow_public_report_success(self, report_service, populated_db, other_user, db_session):
        report = populated_db["report_pubblico_a"]
        updated_report = report_service.follow_report(report.id, other_user)
        
        # Rinfreschiamo l'istanza per popolare la relazione dopo il commit del servizio
        db_session.refresh(updated_report)
        assert any(f.user_id == other_user.id for f in updated_report.followers)

    def test_follow_private_report_raises_error(self, report_service, populated_db, other_user):
        report = populated_db["report_privato"]
        with pytest.raises(ValidationError, match="Only published reports can be followed."):
            report_service.follow_report(report.id, other_user)

    def test_follow_already_followed_report_returns_early(self, report_service, populated_db, other_user):
        report = populated_db["report_pubblico_a"]
        report_service.follow_report(report.id, other_user)
        updated_report = report_service.follow_report(report.id, other_user)
        assert updated_report.id == report.id


class TestUnfollowReport:

    def test_unfollow_existing_follower_removes_relationship(self, report_service, populated_db, other_user, db_session):
        report = populated_db["report_pubblico_a"]
        report_service.follow_report(report.id, other_user)
        
        updated_report = report_service.unfollow_report(report.id, other_user)
        db_session.refresh(updated_report)
        
        assert not any(f.user_id == other_user.id for f in updated_report.followers)

    def test_unfollow_non_existent_follower_does_nothing(self, report_service, populated_db, other_user):
        report = populated_db["report_pubblico_a"]
        
        updated_report = report_service.unfollow_report(report.id, other_user)
        
        assert updated_report.id == report.id


class TestListPendingReports:

    def test_list_pending_reports_filters_correctly(self, report_service, populated_db, test_category, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.PENDING_APPROVAL
        report.category_id = test_category.id
        db_session.commit()

        filters = {
            "category_id": test_category.id,
            "date_from": datetime.utcnow() - timedelta(days=1),
            "date_to": datetime.utcnow() + timedelta(days=1)
        }
        
        results = report_service.list_pending_reports(filters)
        
        assert any(r.id == report.id for r in results)


class TestListOperatorReports:

    def test_list_operator_reports_returns_matching_category(self, report_service, populated_db, test_operator, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.ASSIGNED
        report.category_id = test_operator.category_id
        db_session.commit()

        results = report_service.list_operator_reports(test_operator)
        
        assert any(r.id == report.id for r in results)


class TestAssignReport:

    def test_assign_report_success_as_operator(self, report_service, populated_db, test_operator, db_session):
        # Prendiamo un report esistente e impostiamolo in stato di attesa approvazione
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.PENDING_APPROVAL
        report.category_id = test_operator.category_id
        db_session.commit()

        report_service.notification_service.notify_status_change = Mock()
        updated = report_service.assign_report(report.id, test_operator)

        assert updated.status == ReportStatus.ASSIGNED
        report_service.notification_service.notify_status_change.assert_called_once()

    def test_assign_report_invalid_role_raises_error(self, report_service, populated_db, test_user, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.PENDING_APPROVAL
        db_session.commit()
        
        with pytest.raises(AuthorizationError, match="Only operators or admins can assign reports."):
            report_service.assign_report(report.id, test_user)

    def test_assign_report_wrong_category_raises_error(self, report_service, populated_db, test_operator, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.PENDING_APPROVAL
        report.category_id = test_operator.category_id + 999
        db_session.commit()

        with pytest.raises(AuthorizationError, match="This report does not belong to your category."):
            report_service.assign_report(report.id, test_operator)

    def test_assign_non_pending_report_raises_error(self, report_service, populated_db, admin_user, db_session):
        # Impediamo che sia PENDING_APPROVAL per scatenare l'errore di validazione dello stato
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.RESOLVED
        db_session.commit()
        
        with pytest.raises(ValidationError, match="Only pending reports can be assigned."):
            report_service.assign_report(report.id, admin_user)



class TestUpdateStatus:

    def test_update_status_success_operator(self, report_service, populated_db, test_operator, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.ASSIGNED
        report.category_id = test_operator.category_id
        db_session.commit()

        report_service.notification_service.notify_status_change = Mock()
        updated = report_service.update_status(report.id, test_operator, "Resolved")
        
        assert updated.status == ReportStatus.RESOLVED

    def test_update_status_invalid_role_raises_error(self, report_service, populated_db, test_user, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.ASSIGNED
        db_session.commit()
        
        with pytest.raises(AuthorizationError, match="Only operators and admins can update report status."):
            report_service.update_status(report.id, test_user, "RESOLVED")

    def test_update_status_invalid_value_raises_error(self, report_service, populated_db, admin_user, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.ASSIGNED
        db_session.commit()
        
        with pytest.raises(ValidationError, match="Invalid report status."):
            report_service.update_status(report.id, admin_user, "NON_EXISTENT_STATUS")

    def test_update_status_rejection_without_note_raises_error(self, report_service, populated_db, admin_user, db_session):
        report = populated_db["report_pubblico_a"]
        report.status = ReportStatus.PENDING_APPROVAL
        db_session.commit()
        
        with pytest.raises(ValidationError, match="Rejection reason is required."):
            # Passiamo il valore stringa esatto dell'enum: "Rejected"
            report_service.update_status(report.id, admin_user, "Rejected", note="")


class TestExportRows:

    def test_export_rows_correctly_maps_fields(self, report_service, populated_db):
        report = populated_db["report_pubblico_a"]
        
        rows = report_service.export_rows(category_id=report.category_id)
        
        assert len(rows) >= 1
        target_row = next(row for row in rows if row["id"] == report.id)
        assert target_row["title"] == report.title
        assert target_row["category"] == report.category.name
        assert target_row["status"] == report.status.value
        assert target_row["latitude"] == report.latitude
        assert target_row["longitude"] == report.longitude
        assert isinstance(target_row["created_at"], str)



class TestEnsureOperatorCategoryAccess:

    def test_ensure_operator_category_access_raises_if_not_operator_or_admin(self, report_service, populated_db, test_user, db_session):
        report = populated_db["report_pubblico_a"]
        
        # Copre: if operator.role != Role.OPERATOR (quando non è nemmeno ADMIN)
        test_user.role = "USER"  # Forza un ruolo comune non autorizzato a gestire i report
        db_session.commit()

        with pytest.raises(AuthorizationError, match="Only operators and admins can manage reports."):
            report_service._ensure_operator_category_access(test_user, report)