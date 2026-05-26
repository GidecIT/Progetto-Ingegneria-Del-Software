"""
UC-01  Browse the public portal and view published reports.
UC-02  Filter published reports by category / status / date.
"""
import pytest
from conftest import PageHelper


class TestPublicHome:
    """UC-01 – Public home page loads and lists published reports."""

    def test_uc01_home_page_renders(self, page: PageHelper):
        """UC-01: The home page is reachable without authentication and shows
        the public report table and map card."""
        page.go("/")
        page.by_id_visible("home-page")
        page.by_id("public-report-table")
        page.by_id("public-map-card")

    def test_uc01_statistics_shown(self, page: PageHelper):
        """UC-01: Public statistics section is visible with a total-reports metric."""
        page.go("/")
        page.by_id_visible("public-statistics-card")
        page.by_id("public-total-reports-value")

    def test_uc01_report_rows_present(self, page: PageHelper):
        """UC-01: The public report table body is rendered (seed data provides rows)."""
        page.go("/")
        tbody = page.by_id("public-report-table-body")
        # At least one row must appear with seed data
        rows = tbody.find_elements("tag name", "tr")
        assert len(rows) > 0, "Expected at least one public report row in seed data"

    def test_uc01_open_report_detail_from_table(self, page: PageHelper):
        """UC-01: Clicking the 'Open' link on the first public report navigates
        to the report detail page."""
        page.go("/")
        tbody = page.by_id("public-report-table-body")
        first_row = tbody.find_elements("tag name", "tr")[0]
        open_link = first_row.find_element("tag name", "a")
        open_link.click()
        page.wait_for_url("/reports/")
        page.by_id("report-detail-page")


class TestPublicFilter:
    """UC-02 – Filter published reports."""

    def test_uc02_filter_form_present(self, page: PageHelper):
        """UC-02: The filter form is rendered with category, status, date fields."""
        page.go("/")
        page.by_id("public-filter-form")
        page.by_id("public-filter-category")
        page.by_id("public-filter-status")
        page.by_id("public-filter-date-from")
        page.by_id("public-filter-date-to")
        page.by_id("public-filter-sort")

    def test_uc02_apply_filters_does_not_crash(self, page: PageHelper):
        """UC-02: Submitting the filter form keeps the page coherent."""
        page.go("/")
        page.by_id_visible("public-filter-form")
        page.click("public-filter-submit")
        # Table should still be visible after filter application
        page.by_id("public-report-table")

    def test_uc02_sort_order_toggle(self, page: PageHelper):
        """UC-02: Changing sort order from 'Newest first' to 'Oldest first'
        and applying filters keeps the table intact."""
        page.go("/")
        page.select_by_value("public-filter-sort", "asc")
        page.click("public-filter-submit")
        page.by_id("public-report-table-body")

    def test_uc02_export_csv_link_present(self, page: PageHelper):
        """UC-02: The Export CSV link is present on the home page."""
        page.go("/")
        link = page.by_id("public-export-link")
        assert link.get_attribute("href"), "Export CSV link has no href"

    def test_uc02_granularity_selector_present(self, page: PageHelper):
        """UC-02: The trend-granularity selector exists and has day/week/month options."""
        page.go("/")
        from selenium.webdriver.support.ui import Select
        sel = Select(page.by_id("public-stat-granularity"))
        values = [o.get_attribute("value") for o in sel.options]
        assert "day" in values
        assert "week" in values
        assert "month" in values
