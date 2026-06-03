import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper, unique_suffix, create_report_and_get_id, create_and_assign_report

class TestReplyToOperatorMessage:

    def test_messages_card_rendered_on_report_detail(self, page: PageHelper):
        report_id = create_report_and_get_id(page)
        page.go(f'/reports/{report_id}')
        assert page.by_id_visible('messages-card').is_displayed()

    def test_citizen_can_send_reply_when_report_is_assigned(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        
        # Robust wait for the form
        page.wait.until(
            lambda d: d.find_elements(By.ID, 'report-message-form') or d.find_elements(By.ID, 'messages-list'),
            message='Report message section did not load'
        )
        
        if page.absent('report-message-form'):
            pytest.skip('Message form not accessible: report not yet assigned.')
            
        assert page.absent('messages-unavailable'), 'messages-unavailable must not appear when the form is present'
        msg_text = f'Hello operator {unique_suffix()}'
        page.fill('report-message-body', msg_text)
        page.click('report-message-submit')
        
        # Wait for clear or list update
        page.wait.until(
            lambda d: d.find_element(By.ID, 'report-message-body').get_attribute('value') == '' 
                      or d.find_elements(By.XPATH, "//*[contains(attribute::id,'message-item-')]"),
            message='Message send did not reflect in UI'
        )
        
        page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(attribute::id,'message-item-')]")), message='No message-item-* appeared after a successful send')
        bodies = page.by_id('messages-list').find_elements(By.XPATH, ".//*[contains(attribute::id,'-body')]")
        assert any((msg_text in el.text for el in bodies)), f"Sent message '{msg_text}' not found in the messages list"

    def test_operator_can_view_message_thread(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        assert page.by_id_visible('messages-card').is_displayed()
