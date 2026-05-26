"""
UC-10  Operator assigns a pending report.
UC-11  Operator updates the status of an assigned report.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from conftest import OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


class TestOperatorAssign:
    """UC-10 – Operator assigns a pending report."""

    def test_uc10_operator_page_renders(self, page: PageHelper):
        """UC-10: Operator dashboard page is accessible after operator login."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        page.by_id("operator-page")

    def test_uc10_assigned_reports_section_present(self, page: PageHelper):
        """UC-10: The assigned reports section is always shown."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        page.by_id("assigned-reports-section")

    def test_uc10_pending_reports_section_shown_when_available(self, page: PageHelper):
        """UC-10: If there are pending reports the pending-reports section is rendered."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")

        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports in current data; skipping assign test")

        table = page.by_id("pending-reports-table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        # header + at least one data row
        assert len(rows) >= 2, "Expected at least one pending report row"

    def test_uc10_assign_button_present(self, page: PageHelper):
        """UC-10: An Assign button with the correct prefixed ID is present
        for each row in the pending reports table."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")

        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports available")

        tbody = page.by_id("pending-reports-table-body")
        assign_buttons = tbody.find_elements(
            By.XPATH, ".//*[contains(@id, 'pending-report-assign-')]"
        )
        assert assign_buttons, "Expected at least one assign button in pending reports"

    def test_uc10_assign_report_moves_to_assigned(self, page: PageHelper):
        """UC-10: Clicking Assign on a pending report removes it from the pending
        list and adds it to the assigned list."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")

        if page.absent("pending-reports-section"):
            pytest.skip("No pending reports available")

        tbody_pending = page.by_id("pending-reports-table-body")
        assign_buttons = tbody_pending.find_elements(
            By.XPATH, ".//*[contains(@id, 'pending-report-assign-')]"
        )
        first_btn_id = assign_buttons[0].get_attribute("id")
        report_id = first_btn_id.split("-")[-1]

        assign_buttons[0].click()

        # The assigned reports table should now contain this report
        page.by_id(f"assigned-report-row-{report_id}")


class TestOperatorUpdateStatus:
    """UC-11 – Operator updates the status of an assigned report."""

    def _get_first_assigned_row_id(self, page: PageHelper) -> str:
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        tbody = page.by_id("assigned-reports-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        if not rows:
            pytest.skip("No assigned reports for operator in seed data")
        row_id_attr = rows[0].get_attribute("id")  # e.g. assigned-report-row-5
        return row_id_attr.split("-")[-1]

    def test_uc11_assigned_report_has_status_select(self, page: PageHelper):
        """UC-11: Each assigned report row contains a status drop-down."""
        report_id = self._get_first_assigned_row_id(page)
        status_select = page.by_id(f"assigned-report-status-{report_id}")
        options = Select(status_select).options
        assert len(options) > 0, "Status selector should have options"

    def test_uc11_update_status_button_present(self, page: PageHelper):
        """UC-11: An Update button exists for each assigned report."""
        report_id = self._get_first_assigned_row_id(page)
        page.by_id(f"assigned-report-update-{report_id}")

    def test_uc11_update_status_with_note(self, page: PageHelper):
        """UC-11: Selecting a status, entering a note and clicking Update
        does not produce an error message."""
        report_id = self._get_first_assigned_row_id(page)

        status_select = page.by_id(f"assigned-report-status-{report_id}")
        sel = Select(status_select)
        options = [o.get_attribute("value") for o in sel.options]
        # pick the second option to change the status
        target_status = options[1] if len(options) > 1 else options[0]
        sel.select_by_value(target_status)

        note_input = page.by_id(f"assigned-report-note-{report_id}")
        note_input.clear()
        note_input.send_keys("Automated test note")

        page.click(f"assigned-report-update-{report_id}")

        # No operator error should appear
        assert page.absent("operator-error"), (
            "Operator error element should not be present after a valid update"
        )

    def test_uc11_operator_page_not_accessible_as_citizen(self, page: PageHelper):
        """UC-11: Citizens are redirected away from /operator."""
        from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/operator")
        assert "/operator" not in page.driver.current_url, (
            "Citizen should be redirected away from the operator page"
        )
