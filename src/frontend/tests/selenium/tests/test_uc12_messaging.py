"""UC-12  In-report messaging between citizen and operator."""
import pytest
from selenium.webdriver.common.by import By

from conftest import (
    OPERATOR_EMAIL, OPERATOR_PASSWORD,
    PageHelper, unique_suffix, create_report_and_get_id,
)


class TestMessaging:
    """UC-12 – In-report messaging."""

    def test_messages_card_present_on_detail(self, page: PageHelper):
        """UC-12: The messages card is rendered on the report detail page."""
        report_id = create_report_and_get_id(page)
        page.go(f"/reports/{report_id}")
        page.by_id("messages-card")

    def test_send_message_as_citizen(self, page: PageHelper):
        """UC-12: The citizen can send a message when can_access_messages is true."""
        report_id = create_report_and_get_id(page)
        page.go(f"/reports/{report_id}")
        if page.absent("report-message-form"):
            pytest.skip("Message form not accessible for this report state (not yet assigned)")
        msg_text = f"Hello operator {unique_suffix()}"
        page.fill("report-message-body", msg_text)
        page.click("report-message-submit")
        messages_list = page.by_id("messages-list")
        bodies = messages_list.find_elements(
            By.XPATH, ".//*[contains(@id,'-body')]"
        )
        assert any(msg_text in el.text for el in bodies), (
            f"Sent message '{msg_text}' not found in messages list"
        )

    def test_message_thread_accessible_for_operator(self, page: PageHelper):
        """UC-12: An operator can open the messages card of an assigned report."""
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.wait_for_url("/operator")
        tbody = page.by_id("assigned-reports-table-body")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        if not rows:
            pytest.skip("No assigned reports for operator")
        detail_link = rows[0].find_element(
            By.XPATH, ".//*[contains(@id,'-open-detail')]"
        )
        detail_link.click()
        page.wait_for_url("/reports/")
        page.by_id("messages-card")