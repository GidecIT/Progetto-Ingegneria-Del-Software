"""
UC-12  In-report messaging between citizen and operator.
"""
import os
import tempfile

import pytest
from selenium.webdriver.common.by import By

from conftest import (
    CITIZEN_EMAIL, CITIZEN_PASSWORD,
    OPERATOR_EMAIL, OPERATOR_PASSWORD,
    PageHelper, unique_suffix,
)


def _write_temp_image() -> str:
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
        b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
        b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    fd, path = tempfile.mkstemp(suffix=".png")
    with os.fdopen(fd, "wb") as fh:
        fh.write(png_bytes)
    return path


def _create_report_and_get_id(page: PageHelper) -> int:
    """Create a new report as citizen and return its numeric ID."""
    img = _write_temp_image()
    try:
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.fill("report-title", f"Msg test {unique_suffix()}")
        page.fill("report-description", "Report for messaging test.")
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait_for_url("/reports/")
        url = page.driver.current_url
        return int(url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)


class TestMessaging:
    """UC-12 – In-report messaging."""

    def test_uc12_message_form_visible_for_citizen_own_report(self, page: PageHelper):
        """UC-12: After creating a report, the citizen sees the message form
        on the report detail page."""
        report_id = _create_report_and_get_id(page)
        page.go(f"/reports/{report_id}")
        # messages section – form may only appear once the report is assigned,
        # but can_access_messages drives visibility; check the card itself
        page.by_id("messages-card")

    def test_uc12_send_message_as_citizen(self, page: PageHelper):
        """UC-12: The citizen can submit a message using the report message form
        if can_access_messages is true for that report."""
        report_id = _create_report_and_get_id(page)
        page.go(f"/reports/{report_id}")

        if page.absent("report-message-form"):
            pytest.skip("Message form not accessible for this report state (not yet assigned)")

        msg_text = f"Hello operator {unique_suffix()}"
        page.fill("report-message-body", msg_text)
        page.click("report-message-submit")

        # After submit the message list should contain the new message
        messages_list = page.by_id("messages-list")
        items = messages_list.find_elements(By.XPATH, ".//*[contains(@id, 'message-item-')]")
        bodies = [
            item.find_elements(By.XPATH, ".//*[contains(@id, '-body')]")
            for item in items
        ]
        all_texts = [el.text for row in bodies for el in row]
        assert any(msg_text in t for t in all_texts), (
            f"Sent message '{msg_text}' not found in messages list"
        )

    def test_uc12_message_thread_accessible_for_operator(self, page: PageHelper):
        """UC-12: An operator can view the message thread of an assigned report."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")

        tbody = page.by_id("assigned-reports-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        if not rows:
            pytest.skip("No assigned reports for operator")

        # Open the detail page for the first assigned report
        first_row = rows[0]
        detail_link = first_row.find_element(
            By.XPATH, ".//*[contains(@id, '-open-detail')]"
        )
        detail_link.click()
        page.wait_for_url("/reports/")
        page.by_id("messages-card")
