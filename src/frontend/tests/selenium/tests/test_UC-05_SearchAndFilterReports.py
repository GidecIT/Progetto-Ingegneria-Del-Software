"""UC-05  Search and filter reports"""
import pytest
import requests
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from conftest import PageHelper, create_and_assign_report, wait_for_report_rows

API_BASE = "http://localhost:5050/api/v1"


def _get_reports_from_api(sort: str) -> list[dict]:
    """Call the public reports API and return the list in the given sort order."""
    response = requests.get(f"{API_BASE}/reports", params={"sort": sort}, timeout=10)
    response.raise_for_status()
    return response.json()


class TestSearchAndFilterReports:
    """UC-05 – Visitor filters and sorts the public report list."""

    def test_filter_form_present_with_all_fields(self, page: PageHelper):
        """UC-05: The filter form has category, status, date-from, date-to,
        and sort-order fields."""
        page.go("/")
        assert page.by_id("public-filter-form").is_displayed()
        assert page.by_id("public-filter-category").is_displayed()
        assert page.by_id("public-filter-status").is_displayed()
        assert page.by_id("public-filter-date-from").is_displayed()
        assert page.by_id("public-filter-date-to").is_displayed()
        assert page.by_id("public-filter-sort").is_displayed()

    def test_applying_filters_keeps_table_visible(self, page: PageHelper):
        """UC-05: Submitting the filter form keeps the report table on screen."""
        page.go("/")
        page.by_id_visible("public-filter-form")
        page.click("public-filter-submit")
        assert page.by_id("public-report-table").is_displayed()

    def test_api_returns_reports_in_ascending_date_order(self, page: PageHelper):
        """UC-05: The backend returns reports with created_at non-decreasing
        when sort=asc is requested."""
        reports = _get_reports_from_api("asc")
        assert reports, "API should return at least one public report"
        dates = [datetime.fromisoformat(r["created_at"]) for r in reports]
        for i in range(len(dates) - 1):
            assert dates[i] <= dates[i + 1], (
                f"Sort order wrong at position {i}: "
                f"{dates[i]} > {dates[i + 1]} in 'oldest first' mode"
            )

    def test_api_returns_reports_in_descending_date_order(self, page: PageHelper):
        """UC-05: The backend returns reports with created_at non-increasing
        when sort=desc is requested."""
        reports = _get_reports_from_api("desc")
        assert reports, "API should return at least one public report"
        dates = [datetime.fromisoformat(r["created_at"]) for r in reports]
        for i in range(len(dates) - 1):
            assert dates[i] >= dates[i + 1], (
                f"Sort order wrong at position {i}: "
                f"{dates[i]} < {dates[i + 1]} in 'newest first' mode"
            )

    def test_switching_sort_order_changes_first_row_in_ui(self, page: PageHelper):
        reports_desc = _get_reports_from_api("desc")
        reports_asc = _get_reports_from_api("asc")

        # Se il database è vuoto o l'ordinamento asc/desc restituisce lo stesso
        # primo elemento (poiché i timestamp coincidono o c'è un solo report),
        # creiamo forzatamente nuovi report per avere una differenza garantita.
        if len(reports_desc) < 2 or reports_desc[0]["id"] == reports_asc[0]["id"]:
            create_and_assign_report(page)
            # Create another one. The creation time will be different naturally.
            create_and_assign_report(page)
            
            reports_desc = _get_reports_from_api("desc")
            reports_asc = _get_reports_from_api("asc")

        if reports_desc[0]["id"] == reports_asc[0]["id"]:
            pytest.skip("Impossibile garantire report con timestamp differenti nel seed.")

        page.go("/")
        wait_for_report_rows(page)

        tbody = page.by_id("public-report-table-body")
        first_id_desc = int(
            tbody.find_elements(
                By.XPATH, "./tr[starts-with(@id,'public-report-row-')]"
            )[0].get_attribute("id").split("-")[-1]
        )

        page.select_by_value("public-filter-sort", "asc")
        page.click("public-filter-submit")

        page.wait.until(
            lambda d: int(
                d.find_elements(
                    By.XPATH,
                    "//tbody[@id='public-report-table-body']"
                    "/tr[starts-with(@id,'public-report-row-')]"
                )[0].get_attribute("id").split("-")[-1]
            ) != first_id_desc,
            message="First row did not change after switching to 'Oldest first'",
        )

    def test_granularity_selector_has_three_options(self, page: PageHelper):
        """UC-05: The trend-granularity selector offers day, week, and month."""
        page.go("/")
        sel = Select(page.by_id("public-stat-granularity"))
        values = [o.get_attribute("value") for o in sel.options]
        assert "day" in values
        assert "week" in values
        assert "month" in values