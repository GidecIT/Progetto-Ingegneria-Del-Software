"""UC-16  Admin views platform-wide statistics."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


class TestAdminStatistics:
    """UC-16 – Admin statistics panel."""

    def test_statistics_section_rendered(self, page: PageHelper):
        """UC-16: The admin statistics section is rendered on the admin page."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-statistics-section")
        page.by_id("admin-stats-grid")

    def test_reports_by_status_metric(self, page: PageHelper):
        """UC-16: The 'Reports by status' metric column is present.
        The ID is built by prefixedDomId(adminMetricItem, 'Reports by status')
        which produces 'admin-metric-item-Reports-by-status' (spaces -> hyphens)."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        # Wait for statistics to load then find by partial ID match
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'admin-metric-item-')]")
            ),
            message="No admin-metric-item-* element found; statistics may not have loaded",
        )
        grid = page.by_id("admin-stats-grid")
        metric_cols = grid.find_elements(
            By.XPATH, ".//*[contains(@id,'admin-metric-item-')]"
        )
        assert len(metric_cols) >= 3, (
            f"Expected at least 3 metric columns, found {len(metric_cols)}"
        )

    def test_each_metric_has_a_list(self, page: PageHelper):
        """UC-16: Every metric column contains at least one list item."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'admin-metric-item-')]")
            ),
        )
        grid = page.by_id("admin-stats-grid")
        metric_cols = grid.find_elements(
            By.XPATH, ".//*[contains(@id,'admin-metric-item-')]"
        )
        for col in metric_cols:
            items = col.find_elements(By.TAG_NAME, "li")
            assert items, f"Metric column '{col.get_attribute('id')}' has no list items"

    def test_statistics_not_accessible_as_operator(self, page: PageHelper):
        """UC-16: An operator is redirected away from /admin."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go("/admin")
        assert "/admin" not in page.driver.current_url, (
            "Operator should be redirected away from /admin"
        )