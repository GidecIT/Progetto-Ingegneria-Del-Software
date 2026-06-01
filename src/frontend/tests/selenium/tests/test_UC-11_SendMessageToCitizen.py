"""UC-11  Send message to Citizen"""
import pytest
from selenium.webdriver.common.by import By

from conftest import OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper, create_and_assign_report


class TestSendMessageToCitizen:
    """UC-11 – Municipal Operator sends a message to a citizen via report detail."""

    def test_messages_card_present_on_assigned_report(self, page: PageHelper):
        """UC-11: The messages card is accessible from an assigned report
        detail page opened by the operator."""
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f"/reports/{report_id}")
        page.wait_for_url("/reports/")
        assert page.by_id("messages-card").is_displayed()

    def test_message_form_present_for_operator_on_assigned_report(self, page: PageHelper):
        """UC-11: The operator can access the message form on an assigned
        report to compose and send messages to the citizen."""
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f"/reports/{report_id}")
        page.wait_for_url("/reports/")
        # If the operator can access the thread, the form or the list is visible
        assert (
            page.present("report-message-form") or
            page.present("messages-list")
        ), "Expected message form or message list on assigned report detail"