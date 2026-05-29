"""UC-10  Manage report.

A Municipal Operator reviews pending reports, assigns them to their office,
and the system updates the report status accordingly.
Citizens cannot access the operator page.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


class TestManageReport:
    """UC-10 – Municipal Operator manages the report lifecycle."""

    def test_operator_dashboard_accessible_after_login(self, page: PageHelper):
        """UC-10: The operator dashboard is accessible after operator login."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        assert page.by_id("operator-page").is_displayed()

    def test_assigned_reports_section_always_present(self, page: PageHelper):
        """UC-10: The assigned reports section is always shown on the operator page."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        assert page.by_id("assigned-reports-section").is_displayed()

    def test_pending_reports_table_shown_when_data_available(self, page: PageHelper):
        """UC-10: When pending reports exist, the pending table is rendered
        with at least one data row."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports in current data")
        table = page.by_id("pending-reports-table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        assert len(rows) >= 2, "Expected header + at least one data row"

    def test_assign_button_present_for_each_pending_report(self, page: PageHelper):
        """UC-10: Each pending report row has an Assign button."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports available")
        tbody = page.by_id("pending-reports-table-body")
        buttons = tbody.find_elements(
            By.XPATH, ".//*[contains(@id,'pending-report-assign-')]"
        )
        assert buttons, "Expected at least one Assign button in pending reports table"

    def test_assigning_report_moves_it_to_assigned_list(self, page: PageHelper):
        """UC-10: Clicking Assign on a pending report adds it to the assigned
        list, confirming the status transition was saved."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports available")
        tbody = page.by_id("pending-reports-table-body")
        buttons = tbody.find_elements(
            By.XPATH, ".//*[contains(@id,'pending-report-assign-')]"
        )
        buttons[0].click()
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'assigned-report-row-')]")
            ),
            message="No assigned-report-row-* appeared after clicking Assign",
        )

    def test_operator_page_not_accessible_as_citizen(self, page: PageHelper):
        """UC-10: Citizens are redirected away from /operator (role-based access)."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/operator")
        page.wait_redirect_away_from("/operator")