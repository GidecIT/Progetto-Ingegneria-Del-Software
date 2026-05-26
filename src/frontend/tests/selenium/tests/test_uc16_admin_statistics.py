"""
UC-16  Admin views platform-wide statistics.
"""
import pytest
from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, PageHelper


class TestAdminStatistics:
    """UC-16 – Admin statistics panel."""

    def test_uc16_statistics_section_rendered(self, page: PageHelper):
        """UC-16: The admin statistics section is rendered on the admin page."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-statistics-section")
        page.by_id("admin-stats-grid")

    def test_uc16_reports_by_status_metric(self, page: PageHelper):
        """UC-16: The 'Reports by status' metric list is present."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        # The metric list ID is admin-metric-item-Reports by status
        page.by_id("admin-metric-item-Reports by status")

    def test_uc16_reports_by_type_metric(self, page: PageHelper):
        """UC-16: The 'Reports by type' metric list is present."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-metric-item-Reports by type")

    def test_uc16_reports_by_reporter_metric(self, page: PageHelper):
        """UC-16: The 'Reports by reporter' metric list is present."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-metric-item-Reports by reporter")

    def test_uc16_statistics_not_accessible_as_operator(self, page: PageHelper):
        """UC-16: An operator is redirected away from /admin (cannot access
        admin statistics)."""
        from conftest import OPERATOR_EMAIL, OPERATOR_PASSWORD
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go("/admin")
        assert "/admin" not in page.driver.current_url, (
            "Operator should be redirected away from /admin"
        )
