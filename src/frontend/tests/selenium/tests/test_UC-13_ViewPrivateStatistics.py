"""UC-13  View private statistics"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


class TestViewPrivateStatistics:
    """UC-13 – Administrator views private statistics."""

    def test_statistics_section_rendered_for_admin(self, page: PageHelper):
        """UC-13: The private statistics section is rendered on the admin page."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        assert page.by_id_visible("admin-statistics-section").is_displayed()
        assert page.by_id_visible("admin-stats-grid").is_displayed()

    def test_at_least_three_metric_columns_present(self, page: PageHelper):
        """UC-13: The statistics grid contains at least 3 metric columns
        (by status, by type/category, by reporter)."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'admin-metric-item-')]")
            ),
            message="No admin-metric-item-* element found",
        )
        grid = page.by_id("admin-stats-grid")
        metric_items = grid.find_elements(
            By.XPATH, "./div[contains(@id,'admin-metric-item-')]"
        )
        assert len(metric_items) >= 3, (
            f"Expected at least 3 metric columns, found {len(metric_items)}"
        )

    def test_each_metric_column_contains_entries(self, page: PageHelper):
        """UC-13: Every metric column contains at least one data entry."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'admin-metric-item-')]")
            ),
        )
        grid = page.by_id("admin-stats-grid")
        metric_items = grid.find_elements(
            By.XPATH, "./div[contains(@id,'admin-metric-item-')]"
        )
        for item in metric_items:
            entries = item.find_elements(By.XPATH, ".//*[contains(@id,'-entry-')]")
            if not entries:
                entries = item.find_elements(By.TAG_NAME, "li")
            assert entries, (
                f"Metric '{item.get_attribute('id')}' has no entries"
            )

    def test_private_statistics_not_accessible_as_operator(self, page: PageHelper):
        """UC-13: Operators are redirected away from /admin (role-based access)."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go("/admin")
        page.wait_redirect_away_from("/admin")