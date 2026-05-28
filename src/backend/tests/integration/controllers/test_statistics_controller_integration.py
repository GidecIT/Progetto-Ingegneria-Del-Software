from __future__ import annotations
import pytest

from participium.models.enums import ReportStatus


class TestStatisticsControllerIntegration:

    def test_public_statistics_default_granularity(
        self, statistics_controller, test_user, test_category, make_report, db_session
    ):
        make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.ASSIGNED
        )
        make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.ASSIGNED
        )
        db_session.commit()

        stats = statistics_controller.public_statistics()

        assert isinstance(stats, dict)
        assert "total_reports" in stats or "by_status" in stats or "trends" in stats
        
        if "total_reports" in stats:
            assert stats["total_reports"] >= 2

    def test_public_statistics_custom_granularity(
        self, statistics_controller, test_user, test_category, make_report, db_session
    ):
        make_report(
            reporter_id=test_user.id,
            category_id=test_category.id,
            status=ReportStatus.ASSIGNED
        )
        db_session.commit()

        stats_month = statistics_controller.public_statistics(granularity="month")

        assert isinstance(stats_month, dict)
        
        stats_day = statistics_controller.public_statistics(granularity="day")
        assert isinstance(stats_day, dict)