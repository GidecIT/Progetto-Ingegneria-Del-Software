from __future__ import annotations
from datetime import datetime, timedelta
import pytest

from participium.models.enums import ReportStatus, Role
from participium.controllers.report_controller import ReportController, ReportDetailContext
from participium.config.constants import PUBLIC_VISIBLE_STATUSES


class TestReportControllerIntegration:

    def test_list_public_reports_filters_and_sorting(
        self, report_controller, test_user, test_category, make_report, db_session
    ):
        public_status = next(iter(PUBLIC_VISIBLE_STATUSES))
        
        report_old = make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=public_status
        )
        report_old.created_at = datetime(2026, 1, 1, 12, 0)
        
        report_new = make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=public_status
        )
        report_new.created_at = datetime(2026, 5, 28, 12, 0)
        
        db_session.commit()

        reports_desc = report_controller.list_public_reports(
            category_id=test_category.id,
            status=public_status,
            date_from=datetime(2025, 1, 1),
            sort="desc"
        )
        assert len(reports_desc) >= 2
        assert reports_desc[0].id == report_new.id

        reports_asc = report_controller.list_public_reports(category_id=test_category.id, sort="asc")
        assert reports_asc[0].id == report_old.id

    def test_list_user_reports(self, report_controller, test_user, test_category, make_report, db_session):
        report = make_report(reporter_id=test_user.id, category_id=test_category.id)
        db_session.commit()

        user_reports = report_controller.list_user_reports(test_user)
        assert any(r.id == report.id for r in user_reports)

    def test_build_detail_context_authenticated_with_notifications(
        self, report_controller, test_user, test_category, make_report, make_notification, db_session
    ):
        report = make_report(reporter_id=test_user.id, category_id=test_category.id, status=ReportStatus.ASSIGNED)
        db_session.commit()

        notification = make_notification(user_id=test_user.id, report_id=report.id, is_read=False)
        db_session.commit()

        context = report_controller.build_detail_context(report.id, test_user)

        assert isinstance(context, ReportDetailContext)
        assert context.report.id == report.id
        assert context.can_access_messages is True
        
        db_session.refresh(notification)
        assert notification.is_read is True

    def test_build_detail_context_anonymous_user(
        self, report_controller, test_user, test_category, make_report, db_session
    ):
        public_status = next(iter(PUBLIC_VISIBLE_STATUSES))
        report = make_report(reporter_id=test_user.id, category_id=test_category.id, status=public_status)
        db_session.commit()

        context = report_controller.build_detail_context(report.id, user=None)

        assert isinstance(context, ReportDetailContext)
        assert context.report.id == report.id
        assert context.can_access_messages is False

    def test_create_report_with_photos(self, report_controller, test_user, test_category, mock_file, db_session):
        photo_file = mock_file(filename="buco_strada.jpg", content=b"image_bytes")
        
        report = report_controller.create_report(
            reporter=test_user,
            category_id=test_category.id,
            title="Nuovo Report Integrato",
            description="Dettagliata descrizione del problema riscontrato",
            latitude=41.8902,
            longitude=12.4922,
            photos=[photo_file],
            is_anonymous=True
        )
        db_session.commit()

        assert report.id is not None
        assert report.title == "Nuovo Report Integrato"
        assert report.is_anonymous is True
        assert len(report.photos) == 1
        assert report.photos[0].original_filename == "buco_strada.jpg"

    def test_follow_and_unfollow_report(self, report_controller, test_user, test_category, make_report, db_session):
        public_status = next(iter(PUBLIC_VISIBLE_STATUSES))
        report = make_report(reporter_id=test_user.id, category_id=test_category.id, status=public_status)
        db_session.commit()

        followed_report = report_controller.follow_report(report.id, test_user)
        db_session.commit()
        
        db_session.refresh(followed_report)
        assert any(f.user_id == test_user.id for f in followed_report.followers)

        unfollowed_report = report_controller.unfollow_report(report.id, test_user)
        db_session.commit()
        
        db_session.refresh(unfollowed_report)
        assert not any(f.user_id == test_user.id for f in unfollowed_report.followers)

    def test_export_rows(self, report_controller, test_user, test_category, make_report, db_session):
        public_status = next(iter(PUBLIC_VISIBLE_STATUSES))
        make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            title="Export Target",
            status=public_status
        )
        db_session.commit()

        rows = report_controller.export_rows(category_id=test_category.id, status=public_status)
        assert len(rows) >= 1
        assert any(row["title"] == "Export Target" for row in rows)

    def test_messaging_list_and_send_message(
        self, report_controller, test_user, test_category, make_report, db_session
    ):
        report = make_report(reporter_id=test_user.id, category_id=test_category.id, status=ReportStatus.PENDING_APPROVAL)
        db_session.commit()

        from participium.core.security import hash_password
        from participium.models.user import User
        
        operator = User(
            username="operator_reply_test",
            email="op_reply@ex.com",
            first_name="Luca",
            last_name="Verdi",
            password_hash=hash_password("password_di_test"),
            role=Role.OPERATOR,
            category_id=test_category.id,
            is_active=True,
            is_email_verified=True,
        )
        db_session.add(operator)
        db_session.commit()

        from participium.controllers.operator_controller import OperatorController
        from participium.services.report_service import ReportService
        from participium.services.notification_service import NotificationService
        
        rep_service = ReportService(
            session=db_session,
            report_repository=report_controller.report_service.report_repository,
            category_repository=report_controller.report_service.category_repository,
            storage_service=report_controller.report_service.storage_service,
            notification_service=report_controller.report_service.notification_service,
        )
        notif_service = NotificationService(
            session=db_session,
            notification_repository=report_controller.notification_service.notification_repository,
            email_gateway=report_controller.notification_service.email_gateway,
        )
        
        op_controller = OperatorController(report_service=rep_service, notification_service=notif_service)
        assigned_report = op_controller.assign_report(report.id, operator)
        db_session.commit()
        
        db_session.refresh(assigned_report)
        db_session.refresh(test_user)

        message = report_controller.send_message(
            report=assigned_report,
            sender=test_user,
            body="Messaggio di test d'integrazione per la discussione."
        )
        db_session.commit()

        assert message.id is not None
        assert message.body == "Messaggio di test d'integrazione per la discussione."

        messages_list = report_controller.list_messages(assigned_report, test_user)
        assert any(m.id == message.id for m in messages_list)