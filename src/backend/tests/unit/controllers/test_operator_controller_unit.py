from __future__ import annotations
import pytest

from participium.controllers.operator_controller import OperatorDashboardContext


class TestOperatorDashboard:
    def test_build_dashboard_for_admin(self, operator_controller, mock_admin, mock_report):
        mock_pending = [mock_report]
        mock_assigned = [mock_report, mock_report]
        mock_unread = {100: 2}

        operator_controller.report_service.list_pending_reports.return_value = mock_pending
        operator_controller.report_service.list_operator_reports.return_value = mock_assigned
        operator_controller.notification_service.count_unread_message_notifications_by_report.return_value = mock_unread

        context = operator_controller.build_dashboard(operator=mock_admin, filters={"sort": "desc"})

        assert isinstance(context, OperatorDashboardContext)
        assert context.pending_reports == mock_pending
        assert context.assigned_reports == mock_assigned
        assert context.unread_message_counts == mock_unread

        operator_controller.report_service.list_pending_reports.assert_called_once_with({"sort": "desc"})
        operator_controller.report_service.list_operator_reports.assert_called_once_with(mock_admin)
        operator_controller.notification_service.count_unread_message_notifications_by_report.assert_called_once_with(
            mock_admin.id
        )

    def test_build_dashboard_for_operator_injects_category_filter(self, operator_controller, mock_operator, mock_report):
        mock_pending = [mock_report]
        operator_controller.report_service.list_pending_reports.return_value = mock_pending
        operator_controller.report_service.list_operator_reports.return_value = []
        operator_controller.notification_service.count_unread_message_notifications_by_report.return_value = {}

        context = operator_controller.build_dashboard(operator=mock_operator, filters={"sort": "desc"})

        assert context.pending_reports == mock_pending
        operator_controller.report_service.list_pending_reports.assert_called_once_with(
            {"sort": "desc", "category_id": mock_operator.category_id}
        )

    def test_build_dashboard_with_none_filters_initializes_empty_dict(self, operator_controller, mock_admin):
        operator_controller.report_service.list_pending_reports.return_value = []
        operator_controller.report_service.list_operator_reports.return_value = []
        operator_controller.notification_service.count_unread_message_notifications_by_report.return_value = {}

        operator_controller.build_dashboard(operator=mock_admin, filters=None)

        operator_controller.report_service.list_pending_reports.assert_called_once_with({})

    def test_build_dashboard_for_operator_with_none_filters(self, operator_controller, mock_operator):
        operator_controller.report_service.list_pending_reports.return_value = []
        operator_controller.report_service.list_operator_reports.return_value = []
        operator_controller.notification_service.count_unread_message_notifications_by_report.return_value = {}

        operator_controller.build_dashboard(operator=mock_operator, filters=None)

        operator_controller.report_service.list_pending_reports.assert_called_once_with(
            {"category_id": mock_operator.category_id}
        )

    def test_build_dashboard_for_citizen_returns_empty_pending_reports(self, operator_controller, mock_user):
        """Test per chiudere il cerchio della Branch Coverage (utente che non è ADMIN né OPERATOR)."""
        operator_controller.report_service.list_pending_reports.return_value = []
        operator_controller.report_service.list_operator_reports.return_value = []
        operator_controller.notification_service.count_unread_message_notifications_by_report.return_value = {}

        context = operator_controller.build_dashboard(operator=mock_user, filters=None)

        assert context.pending_reports == []
        operator_controller.report_service.list_pending_reports.assert_not_called()


class TestOperatorActions:
    def test_assign_report_delegates_to_service(self, operator_controller, mock_operator, mock_report):
        operator_controller.report_service.assign_report.return_value = mock_report

        result = operator_controller.assign_report(report_id=100, operator=mock_operator)

        assert result == mock_report
        operator_controller.report_service.assign_report.assert_called_once_with(100, mock_operator)

    def test_update_status_delegates_to_service(self, operator_controller, mock_operator, mock_report):
        operator_controller.report_service.update_status.return_value = mock_report

        result = operator_controller.update_status(
            report_id=100, operator=mock_operator, next_status_value="RESOLVED", note="Lavoro completato"
        )

        assert result == mock_report
        operator_controller.report_service.update_status.assert_called_once_with(
            100, mock_operator, "RESOLVED", "Lavoro completato"
        )