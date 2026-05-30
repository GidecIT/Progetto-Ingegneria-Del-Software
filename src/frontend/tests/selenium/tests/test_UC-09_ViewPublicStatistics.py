"""UC-09  View public statistics.

A visitor consults aggregated statistics about published reports,
including reports by category and time trends by day, week, or month.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from conftest import PageHelper


def _wait_for_statistics_data(page: PageHelper) -> None:
    """Wait until the statistics section has received data from the API.
    The category list <ul> exists in the DOM immediately but has zero height
    until the API response populates it with <li> children."""
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[starts-with(@id,'public-category-stat-')]")
        ),
        message=(
            "No public-category-stat-* element found; "
            "statistics API response may not have arrived yet"
        ),
    )


class TestViewPublicStatistics:
    """UC-09 – Visitor views public statistics on the home page."""

    def test_statistics_section_visible(self, page: PageHelper):
        """UC-09: The public statistics card is visible on the home page."""
        page.go("/")
        assert page.by_id_visible("public-statistics-card").is_displayed()

    def test_total_reports_metric_shown(self, page: PageHelper):
        """UC-09: The total published reports count is displayed."""
        page.go("/")
        total = page.by_id("public-total-reports-value")
        assert total.is_displayed()

    def test_reports_by_category_list_present(self, page: PageHelper):
        """UC-09: The 'Reports by category' breakdown list is shown and contains
        at least one entry once the statistics API response has loaded."""
        page.go("/")
        # The <ul> is rendered immediately but only has children after data loads
        _wait_for_statistics_data(page)
        assert page.by_id("public-category-statistics").is_displayed()
        # After data has loaded the list must contain at least one item
        cat_list = page.by_id("public-category-statistics-list")
        items = cat_list.find_elements(By.TAG_NAME, "li")
        assert len(items) > 0, (
            "Category statistics list should contain at least one entry"
        )

    def test_trend_statistics_section_present(self, page: PageHelper):
        """UC-09: The trend statistics section is shown."""
        page.go("/")
        assert page.by_id("public-trend-statistics").is_displayed()

    def test_granularity_selector_has_day_week_month_options(self, page: PageHelper):
        """UC-09: The visitor can select day, week, or month aggregation for trends."""
        page.go("/")
        sel = Select(page.by_id("public-stat-granularity"))
        values = [o.get_attribute("value") for o in sel.options]
        assert "day" in values, "Day option must be available"
        assert "week" in values, "Week option must be available"
        assert "month" in values, "Month option must be available"

    def test_statistics_accessible_without_login(self, page: PageHelper):
        """UC-09: Public statistics require no authentication."""
        page.go("/")
        assert page.absent("login-page"), "Statistics should be visible without login"
        assert page.by_id("public-statistics-card").is_displayed()