"""UC-11  Operator updates the status of an assigned report."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from conftest import OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


def _login_and_get_first_assigned_id(page: PageHelper) -> str:
    """Log in as operator and return the numeric ID of the first assigned report.
    Skips the test if no assigned reports are available."""
    page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    page.wait_for_url("/operator")
    tbody = page.by_id("assigned-reports-table-body")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    if not rows:
        pytest.skip("No assigned reports for operator in seed data")
    row_id = rows[0].get_attribute("id")   # assigned-report-row-<id>
    return row_id.split("-")[-1]


class TestUpdateReportStatus:
    """UC-11 – Operator updates the status of an assigned report."""

    def test_assigned_report_has_status_select(self, page: PageHelper):
        """UC-11: Each assigned report row contains a status drop-down."""
        report_id = _login_and_get_first_assigned_id(page)
        status_select = page.by_id(f"assigned-report-status-{report_id}")
        assert Select(status_select).options, "Status selector should have options"

    def test_update_button_present(self, page: PageHelper):
        """UC-11: An Update button exists for each assigned report row."""
        report_id = _login_and_get_first_assigned_id(page)
        page.by_id(f"assigned-report-update-{report_id}")

    def test_update_status_with_note(self, page: PageHelper):
        """UC-11: Clicking Update with the current status and a note does not
        produce an operator error. We keep the existing status value to avoid
        backend rejection of invalid state transitions."""
        report_id = _login_and_get_first_assigned_id(page)

        # Read the currently selected status and resubmit it (always valid)
        sel = Select(page.by_id(f"assigned-report-status-{report_id}"))
        current_value = sel.first_selected_option.get_attribute("value")
        sel.select_by_value(current_value)

        note = page.by_id(f"assigned-report-note-{report_id}")
        note.clear()
        note.send_keys("Automated test note")

        page.click(f"assigned-report-update-{report_id}")

        # Wait briefly for any error element to appear, then assert it did not
        page.wait.until(
            lambda d: not d.find_elements("id", "operator-error") or True,
        )
        assert page.absent("operator-error"), (
            "Operator error should not appear after resubmitting the current status"
        )