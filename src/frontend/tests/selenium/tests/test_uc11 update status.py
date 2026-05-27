"""UC-11  Operator updates the status of an assigned report."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper


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
        """UC-11: Selecting a new status, adding a note and clicking Update
        completes without showing an error message."""
        report_id = _login_and_get_first_assigned_id(page)
        sel = Select(page.by_id(f"assigned-report-status-{report_id}"))
        options = [o.get_attribute("value") for o in sel.options]
        sel.select_by_value(options[1] if len(options) > 1 else options[0])

        note = page.by_id(f"assigned-report-note-{report_id}")
        note.clear()
        note.send_keys("Automated test note")

        page.click(f"assigned-report-update-{report_id}")
        assert page.absent("operator-error"), (
            "Operator error should not appear after a valid status update"
        )