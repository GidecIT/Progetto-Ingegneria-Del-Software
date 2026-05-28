from __future__ import annotations
from unittest.mock import Mock
import pytest

from participium.controllers.report_controller import ReportDetailContext
from participium.models.enums import ReportStatus


class TestListAndCreateReports:
    def test_list_public_reports_delegates_to_service(self, report_controller, mock_report):
        mock_reports = [mock_report, mock_report]
        report_controller.report_service.list_public_reports.return_value = mock_reports

        result = report_controller.list_public_reports(
            category_id=1, status=ReportStatus.ASSIGNED, sort="asc"
        )

        assert result == mock_reports
        report_controller.report_service.list_public_reports.assert_called_once_with(
            category_id=1,
            status=ReportStatus.ASSIGNED,
            date_from=None,
            date_to=None,
            sort="asc",
        )

    def test_list_user_reports_delegates_to_service(self, report_controller, mock_user, mock_report):
        mock_reports = [mock_report]
        report_controller.report_service.list_user_reports.return_value = mock_reports

        result = report_controller.list_user_reports(mock_user)

        assert result == mock_reports
        report_controller.report_service.list_user_reports.assert_called_once_with(mock_user)

    def test_create_report_delegates_to_service(self, report_controller, mock_user, mock_report, mock_file):
        report_controller.report_service.create_report.return_value = mock_report

        result = report_controller.create_report( #dati casuali
            reporter=mock_user,
            category_id=2,
            title="Semaforo rotto",
            description="Non funziona",
            latitude=45.0,
            longitude=9.0,
            photos=[mock_file],
            is_anonymous=True,
        )

        assert result == mock_report
        report_controller.report_service.create_report.assert_called_once_with( 
            reporter=mock_user,
            category_id=2,
            title="Semaforo rotto",
            description="Non funziona",
            latitude=45.0,
            longitude=9.0,
            photos=[mock_file],
            is_anonymous=True,
        )


class TestBuildDetailContext:
    def test_build_detail_context_when_access_denied(self, report_controller, mock_user, mock_report):
        report_controller.report_service.get_accessible_report.return_value = mock_report
        report_controller.messaging_service.can_access_thread.return_value = False

        context = report_controller.build_detail_context(report_id=100, user=mock_user)

        assert isinstance(context, ReportDetailContext)
        assert context.report == mock_report
        assert context.can_access_messages is False
        report_controller.notification_service.mark_report_message_notifications_as_read.assert_not_called()

    def test_build_detail_context_anonymous_user_can_access_messages_but_no_notifications(
        self, report_controller, mock_report
    ):
        report_controller.report_service.get_accessible_report.return_value = mock_report
        report_controller.messaging_service.can_access_thread.return_value = True

        context = report_controller.build_detail_context(report_id=100, user=None)

        assert context.can_access_messages is True
        report_controller.notification_service.mark_report_message_notifications_as_read.assert_not_called()

    def test_build_detail_context_success_marks_notifications_as_read(
        self, report_controller, mock_user, mock_report
    ):
        report_controller.report_service.get_accessible_report.return_value = mock_report
        report_controller.messaging_service.can_access_thread.return_value = True

        context = report_controller.build_detail_context(report_id=100, user=mock_user)

        assert context.report == mock_report
        assert context.can_access_messages is True
        report_controller.notification_service.mark_report_message_notifications_as_read.assert_called_once_with(
            mock_user.id, mock_report.id
        )

    def test_build_detail_context_propagates_service_exceptions(self, report_controller, mock_user):
        from participium.core.exceptions import ValidationError
        report_controller.report_service.get_accessible_report.side_effect = ValidationError("Report not found")

        with pytest.raises(ValidationError):
            report_controller.build_detail_context(report_id=999, user=mock_user)


class TestReportInteractionsAndMessaging:
    @pytest.mark.parametrize("action", ["follow", "unfollow"])
    def test_follow_unfollow_delegates_to_service(self, report_controller, mock_user, mock_report, action):
        service_method = getattr(report_controller.report_service, f"{action}_report")
        service_method.return_value = mock_report

        controller_method = getattr(report_controller, f"{action}_report")
        result = controller_method(report_id=100, user=mock_user)

        assert result == mock_report
        service_method.assert_called_once_with(100, mock_user)

    def test_export_rows_delegates_to_service(self, report_controller):
        mock_rows = [{"id": 1, "title": "Test"}]
        report_controller.report_service.export_rows.return_value = mock_rows

        result = report_controller.export_rows(status=ReportStatus.RESOLVED)

        assert result == mock_rows
        report_controller.report_service.export_rows.assert_called_once_with(
            category_id=None, status=ReportStatus.RESOLVED, date_from=None, date_to=None, sort="desc"
        )

    def test_list_messages_delegates_to_messaging_service(self, report_controller, mock_user, mock_report):
        mock_messages = [Mock(), Mock()]
        report_controller.messaging_service.list_messages.return_value = mock_messages

        result = report_controller.list_messages(mock_report, mock_user)

        assert result == mock_messages
        report_controller.messaging_service.list_messages.assert_called_once_with(mock_report, mock_user)

    def test_send_message_delegates_to_messaging_service(self, report_controller, mock_user, mock_report):
        mock_message = Mock()
        report_controller.messaging_service.send_message.return_value = mock_message

        result = report_controller.send_message(mock_report, mock_user, "Testo del messaggio")

        assert result == mock_message
        report_controller.messaging_service.send_message.assert_called_once_with(
            mock_report, mock_user, "Testo del messaggio"
        )