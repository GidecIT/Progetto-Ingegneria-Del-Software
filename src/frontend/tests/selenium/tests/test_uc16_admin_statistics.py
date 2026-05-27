"""UC-16  Admin views platform-wide statistics."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


def _wait_for_metric_lists(page: PageHelper):
    """Wait until at least one admin-metric-list-* element is present.
    These are the container divs for each metric column, distinct from
    the *-title heading elements that share the same id prefix."""
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(@id,'admin-metric-list-')]")
        ),
        message="No admin-metric-list-* element found; statistics may not have loaded",
    )


class TestAdminStatistics:
    """UC-16 – Admin statistics panel."""

    def test_statistics_section_rendered(self, page: PageHelper):
        """UC-16: The admin statistics section is rendered on the admin page."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.by_id("admin-statistics-section")
        page.by_id("admin-stats-grid")

    def test_metric_columns_present(self, page: PageHelper):
        """UC-16: The statistics grid contains at least 3 metric columns."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'admin-metric-item-')]")
            ),
            message="No admin-metric-item-* element found",
        )
        grid = page.by_id("admin-stats-grid")
        # Count only the top-level metric item containers, not nested children
        metric_items = grid.find_elements(
            By.XPATH,
            "./div[contains(@id,'admin-metric-item-')]"
        )
        assert len(metric_items) >= 3, (
            f"Expected at least 3 metric columns, found {len(metric_items)}"
        )

    def test_each_metric_has_list_items(self, page: PageHelper):
        """UC-16: Every metric column contains at least one entry."""
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url("/admin")
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'admin-metric-item-')]")
            ),
        )
        grid = page.by_id("admin-stats-grid")
        metric_items = grid.find_elements(
            By.XPATH,
            "./div[contains(@id,'admin-metric-item-')]"
        )
        for item in metric_items:
            entries = item.find_elements(By.XPATH, ".//*[contains(@id,'-entry-')]")
            if not entries:
                # Fallback: accept any <li> child
                entries = item.find_elements(By.TAG_NAME, "li")
            assert entries, (
                f"Metric '{item.get_attribute('id')}' has no entries; "
                "statistics may not have loaded yet"
            )

    def test_statistics_not_accessible_as_operator(self, page: PageHelper):
        """UC-16: An operator is redirected away from /admin."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go("/admin")
        # ProtectedRoute redirects asynchronously after session check
        page.wait_redirect_away_from("/admin")