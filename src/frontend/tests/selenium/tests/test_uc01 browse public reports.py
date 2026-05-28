"""UC-01  Browse the public portal and view published reports."""
from selenium.webdriver.common.by import By

from conftest import PageHelper, get_first_public_report_id, wait_for_report_rows


class TestBrowsePublicReports:

    def test_home_page_renders(self, page: PageHelper):
        page.go("/")
        page.by_id_visible("home-page")
        page.by_id("public-report-table")
        page.by_id("public-map-card")

    def test_statistics_shown(self, page: PageHelper):
        page.go("/")
        page.by_id_visible("public-statistics-card")
        page.by_id("public-total-reports-value")

    def test_report_rows_present(self, page: PageHelper):
        page.go("/")
        wait_for_report_rows(page)
        tbody = page.by_id("public-report-table-body")
        rows = tbody.find_elements("tag name", "tr")
        assert len(rows) > 0, "Expected at least one public report row in seed data"

    def test_open_report_detail_from_table(self, page: PageHelper):
        report_id = get_first_public_report_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("report-detail-page")
        page.by_id("report-detail-title")