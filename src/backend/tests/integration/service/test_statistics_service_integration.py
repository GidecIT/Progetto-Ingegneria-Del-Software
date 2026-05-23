from __future__ import annotations
from datetime import datetime
import pytest

from participium.models.enums import ReportStatus


class TestPublicStatistics:
    def test_public_statistics_aggregates_only_public_reports(
        self, statistics_service, test_user, test_category, make_historical_report
    ):
        day_date = datetime(2026, 5, 20, 10, 0)
        make_historical_report(test_user.id, test_category.id, day_date, is_public=True)
        make_historical_report(test_user.id, test_category.id, day_date, is_public=True)
        make_historical_report(test_user.id, test_category.id, day_date, is_public=False)

        stats = statistics_service.public_statistics(granularity="day")

        assert stats["total_reports"] == 2
        assert stats["reports_by_category"] == {test_category.name: 2}
        assert stats["trends"] == {"2026-05-20": 2}

    def test_public_statistics_trends_granularity_week(
        self, statistics_service, test_user, test_category, make_historical_report
    ):
        date_in_week = datetime(2026, 5, 20, 12, 0)
        make_historical_report(test_user.id, test_category.id, date_in_week, is_public=True)

        stats = statistics_service.public_statistics(granularity="week")
        assert stats["trends"] == {"2026-W21": 1}

    def test_public_statistics_trends_granularity_month(
        self, statistics_service, test_user, test_category, make_historical_report
    ):
        date_in_month = datetime(2026, 5, 20, 12, 0)
        make_historical_report(test_user.id, test_category.id, date_in_month, is_public=True)

        stats = statistics_service.public_statistics(granularity="month")
        assert stats["trends"] == {"2026-05": 1}


class TestAdminStatistics:
    def test_admin_statistics_includes_private_reports_and_complex_counters(
        self, statistics_service, test_user, test_category, make_historical_report
    ):
        day_date = datetime(2026, 5, 20, 12, 0)
        make_historical_report(
            test_user.id, test_category.id, day_date, is_public=True, status=ReportStatus.PENDING_APPROVAL
        )
        make_historical_report(
            test_user.id, test_category.id, day_date, is_public=False, status=ReportStatus.ASSIGNED
        )

        stats = statistics_service.admin_statistics()

        expected_label = f"{test_user.username} ({test_user.id})"
        assert stats["reports_by_status"] == {ReportStatus.PENDING_APPROVAL.value: 1, ReportStatus.ASSIGNED.value: 1}
        assert stats["reports_by_type"] == {test_category.name: 2}
        assert stats["reports_by_type_and_status"] == {
            f"{test_category.name} | {ReportStatus.PENDING_APPROVAL.value}": 1,
            f"{test_category.name} | {ReportStatus.ASSIGNED.value}": 1,
        }
        assert stats["reports_by_reporter"] == {expected_label: 2}
        assert stats["reports_by_reporter_and_type"] == {f"{expected_label} | {test_category.name}": 2}
        assert stats["reports_by_reporter_type_and_status"] == {
            f"{expected_label} | {test_category.name} | {ReportStatus.PENDING_APPROVAL.value}": 1,
            f"{expected_label} | {test_category.name} | {ReportStatus.ASSIGNED.value}": 1,
        }

    def test_admin_statistics_with_deleted_reporter_label(
        self, statistics_service, db_session, test_user, test_category, make_historical_report
    ):
        day_date = datetime(2026, 5, 20, 12, 0)
        report = make_historical_report(test_user.id, test_category.id, day_date, is_public=True)
        
        report.reporter_id = None
        db_session.commit()

        stats = statistics_service.admin_statistics()
        assert stats["reports_by_reporter"] == {"Deleted Citizen": 1}

    def test_admin_statistics_top_percent_breakdown_calculation(
        self, statistics_service, test_user, other_user, test_category, make_historical_report
    ):
        day_date = datetime(2026, 5, 20, 12, 0)
        
        make_historical_report(test_user.id, test_category.id, day_date)
        make_historical_report(test_user.id, test_category.id, day_date)
        make_historical_report(test_user.id, test_category.id, day_date)
        make_historical_report(other_user.id, test_category.id, day_date)

        stats = statistics_service.admin_statistics()

        assert stats["top_1_percent_by_type"] == {test_category.name: 3}
        assert stats["top_5_percent_by_type"] == {test_category.name: 3}

    def test_admin_statistics_empty_database_returns_empty_dicts(self, statistics_service):
        stats = statistics_service.admin_statistics()
        
        assert stats["reports_by_status"] == {}
        assert stats["top_1_percent_by_type"] == {}
        assert stats["top_5_percent_by_type"] == {}