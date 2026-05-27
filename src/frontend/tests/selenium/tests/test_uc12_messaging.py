"""UC-12  In-report messaging between citizen and operator."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
        """UC-12: The citizen can send a message when the report has been
        assigned (can_access_messages = true). Skips when the newly created
        report is not yet assigned, which is the normal state in a local
        development environment without an active operator session."""
        report_id = create_report_and_get_id(page)
        page.go(f"/reports/{report_id}")

        # can_access_messages drives visibility of both the form AND the list.
        # If the form is absent the report is not assigned — skip cleanly.
        if page.absent("report-message-form"):
            pytest.skip(
                "Message form not accessible: report has not been assigned yet. "
                "Assign the report via the operator dashboard and re-run."
            )

        # Check that the messages-unavailable notice is NOT shown
        # (extra guard: form present but messages blocked would be a bug)
        assert page.absent("messages-unavailable"), (
            "messages-unavailable element should not appear when form is present"
        )

        msg_text = f"Hello operator {unique_suffix()}"
        page.fill("report-message-body", msg_text)
        page.click("report-message-submit")

        # After submit React reloads the report and repopulates the message list
        page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@id,'message-item-')]")
            ),
            message="No message-item-* appeared after sending a message",
        )
        bodies = page.by_id("messages-list").find_elements(
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
        href = detail_link.get_attribute("href")
        page.driver.get(href)
        page.wait_for_url("/reports/")
        page.by_id("messages-card")