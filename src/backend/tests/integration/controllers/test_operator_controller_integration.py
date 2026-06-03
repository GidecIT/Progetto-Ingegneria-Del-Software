from __future__ import annotations
import pytest

from participium.models.enums import Role, ReportStatus
from participium.controllers.operator_controller import OperatorController, OperatorDashboardContext


class TestOperatorControllerIntegration:

    def test_build_dashboard_for_operator_filters_by_category(
        self, operator_controller, test_operator, test_user, test_category, other_category, make_report, db_session
    ):
        report_matching = make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.PENDING_APPROVAL
        )
        report_other_cat = make_report(
            reporter_id=test_user.id,
            category_id=other_category.id,
            status=ReportStatus.PENDING_APPROVAL
        )
        report_to_assign = make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.PENDING_APPROVAL
        )
        db_session.commit()
        
        operator_controller.assign_report(report_to_assign.id, test_operator)
        db_session.commit()

        context = operator_controller.build_dashboard(test_operator)

        assert isinstance(context, OperatorDashboardContext)
        assert any(r.id == report_matching.id for r in context.pending_reports)
        assert not any(r.id == report_other_cat.id for r in context.pending_reports)
        assert any(r.id == report_to_assign.id for r in context.assigned_reports)

    def test_build_dashboard_for_admin_sees_all_pending(
        self, operator_controller, test_user, test_category, other_category, make_report, db_session
    ):
        admin_user = test_user
        admin_user.role = Role.ADMIN
        db_session.commit()

        report_a = make_report(reporter_id=admin_user.id, category_id=test_category.id, status=ReportStatus.PENDING_APPROVAL)
        report_b = make_report(reporter_id=admin_user.id, category_id=other_category.id, status=ReportStatus.PENDING_APPROVAL)
        db_session.commit()

        context = operator_controller.build_dashboard(admin_user)

        assert any(r.id == report_a.id for r in context.pending_reports)
        assert any(r.id == report_b.id for r in context.pending_reports)

    def test_build_dashboard_implicit_final_branch_and_filters(
        self, operator_controller, test_user, test_category, make_report, db_session
    ):
        test_user.role = Role.CITIZEN
        db_session.commit()

        make_report(reporter_id=test_user.id, category_id=test_category.id, status=ReportStatus.PENDING_APPROVAL)
        db_session.commit()

        custom_filters = {"is_anonymous": False}
        context = operator_controller.build_dashboard(test_user, filters=custom_filters)

        assert len(context.pending_reports) == 0

    def test_assign_report_success(
        self, operator_controller, test_operator, test_user, test_category, make_report, db_session
    ):
        report = make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.PENDING_APPROVAL
        )
        db_session.commit()

        updated_report = operator_controller.assign_report(report.id, test_operator)

        db_session.refresh(updated_report)
        assert updated_report.status == ReportStatus.ASSIGNED

    def test_update_status_success(
        self, operator_controller, test_operator, test_user, test_category, make_report, db_session
    ):
        report = make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.PENDING_APPROVAL
        )
        db_session.commit()

        operator_controller.assign_report(report.id, test_operator)
        db_session.commit()

        next_status = ReportStatus.RESOLVED.value
        updated_report = operator_controller.update_status(
            report_id=report.id,
            operator=test_operator,
            next_status_value=next_status,
            note="Problema risolto con successo."
        )

        db_session.refresh(updated_report)
        assert updated_report.status == ReportStatus.RESOLVED