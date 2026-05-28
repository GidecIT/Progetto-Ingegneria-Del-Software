"""UC-02  Filter published reports by category, status, date and sort order."""
from selenium.webdriver.support.ui import Select

from conftest import PageHelper


class TestFilterReports:

    def test_filter_form(self, page: PageHelper):
        page.go("/")
        page.by_id("public-filter-form")
        page.by_id("public-filter-category")
        page.by_id("public-filter-status")
        page.by_id("public-filter-date-from")
        page.by_id("public-filter-date-to")
        page.by_id("public-filter-sort")

    def test_apply_filters(self, page: PageHelper):
        page.go("/")
        page.by_id_visible("public-filter-form")
        page.click("public-filter-submit")
        page.by_id("public-report-table")

    def test_sort_order_toggle(self, page: PageHelper):
        """UC-02: Switching to 'Oldest first' and applying keeps the table intact."""
        page.go("/")
        page.select_by_value("public-filter-sort", "asc")
        page.click("public-filter-submit")
        page.by_id_visible("public-report-table-body")

    def test_export_csv_link_present(self, page: PageHelper):
        """UC-02: The Export CSV link is present and has a valid href."""
        page.go("/")
        link = page.by_id("public-export-link")
        assert link.get_attribute("href"), "Export CSV link has no href"

    def test_granularity_selector_options(self, page: PageHelper):
        """UC-02: The trend-granularity selector has day, week and month options."""
        page.go("/")
        sel = Select(page.by_id("public-stat-granularity"))
        values = [o.get_attribute("value") for o in sel.options]
        assert "day" in values
        assert "week" in values
        assert "month" in values