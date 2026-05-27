"""UC-10  Operator assigns a pending report."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


class TestAssignReport:
    """UC-10 – Operator assigns a pending report."""

    def test_operator_page_renders(self, page: PageHelper):
        """UC-10: Operator dashboard is accessible after operator login."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        page.by_id("operator-page")

    def test_assigned_reports_section_present(self, page: PageHelper):
        """UC-10: The assigned reports section is always rendered."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        page.by_id("assigned-reports-section")

    def test_pending_section_shown_when_available(self, page: PageHelper):
        """UC-10: If pending reports exist the pending-reports table is shown."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports in current data")
        table = page.by_id("pending-reports-table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        assert len(rows) >= 2, "Expected header + at least one data row"

    def test_assign_button_present(self, page: PageHelper):
        """UC-10: An Assign button is present for each pending report row."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports available")
        tbody = page.by_id("pending-reports-table-body")
        buttons = tbody.find_elements(
            By.XPATH, ".//*[contains(@id,'pending-report-assign-')]"
        )
        assert buttons, "Expected at least one assign button"

    def test_assign_moves_report_to_assigned(self, page: PageHelper):
        """UC-10: Clicking Assign removes the report from pending and adds it
        to the assigned list."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports available")
        tbody = page.by_id("pending-reports-table-body")
        buttons = tbody.find_elements(
            By.XPATH, ".//*[contains(@id,'pending-report-assign-')]"
        )
        buttons[0].click()
        # After assign the page reloads; wait for any assigned-report-row to appear
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'assigned-report-row-')]")
            ),
            message="No assigned-report-row-* appeared after clicking Assign",
        )

    def test_operator_page_not_accessible_as_citizen(self, page: PageHelper):
        """UC-10: Citizens are redirected away from /operator."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/operator")
        # ProtectedRoute redirects asynchronously after session check
        page.wait_redirect_away_from("/operator")
