from selenium.webdriver.common.by import By
from conftest import (
    CITIZEN_EMAIL,
    CITIZEN_PASSWORD,
    OPERATOR_EMAIL,
    OPERATOR_PASSWORD,
    PageHelper,
    create_and_assign_report,
    send_report_message,
    unique_suffix,
)

def _messages_list_bodies_xpath() -> str:
    return "//ul[attribute::id='messages-list']//*[contains(attribute::id,'-body')]"

class TestReplyToOperatorMessage:

    def test_thread_with_operator_message_is_available_to_citizen(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        operator_message = f'Please clarify {unique_suffix()}'
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        send_report_message(page, report_id, operator_message)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        assert page.by_id_visible('messages-list').is_displayed()
        assert page.by_id_visible('report-message-form').is_displayed(), 'Citizen must have a reply form'
        page.wait.until(
            lambda d: any(operator_message in el.text for el in d.find_elements(By.XPATH, _messages_list_bodies_xpath())),
            message='Citizen should see the operator message in the thread',
        )

    def test_citizen_reply_reaches_operator(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        send_report_message(page, report_id, f'Operator question {unique_suffix()}')
        reply = f'Citizen reply {unique_suffix()}'
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        send_report_message(page, report_id, reply)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        page.by_id_visible('messages-list')
        page.wait.until(
            lambda d: any(reply in el.text for el in d.find_elements(By.XPATH, _messages_list_bodies_xpath())),
            message='Operator should see the reply sent by the citizen',
        )

    def test_citizen_cannot_send_empty_reply(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        send_report_message(page, report_id, f'Operator note {unique_suffix()}')
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        body = page.by_id_visible('report-message-body')
        page.click('report-message-submit')  # body left empty
        is_valid = page.driver.execute_script("return arguments[0].checkValidity();", body)
        assert is_valid is False, 'Empty required reply body should block submission'
