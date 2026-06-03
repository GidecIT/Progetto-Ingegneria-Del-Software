import pytest
from selenium.webdriver.common.by import By
from conftest import OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper, create_and_assign_report

class TestSendMessageToCitizen:

    def test_messages_card_present_on_assigned_report(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        # Wait for the card specifically, which might take a moment to load
        assert page.by_id_visible('messages-card').is_displayed()

    def test_message_form_present_for_operator_on_assigned_report(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        # Wait for either form or list, giving it a bit of time
        page.wait.until(
            lambda d: d.find_elements(By.ID, 'report-message-form') or d.find_elements(By.ID, 'messages-list'),
            message='Neither report-message-form nor messages-list appeared'
        )
        assert page.present('report-message-form') or page.present('messages-list')
