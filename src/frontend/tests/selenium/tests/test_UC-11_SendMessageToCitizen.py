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

class TestSendMessageToCitizen:

    def test_messages_card_present_on_assigned_report(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        assert page.by_id_visible('messages-card').is_displayed()

    def test_compose_form_present_for_operator_on_assigned_report(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        assert page.by_id_visible('report-message-form').is_displayed()
        assert page.by_id('report-message-body').is_displayed()
        assert page.by_id('report-message-submit').is_displayed()

    def test_operator_message_is_delivered_to_citizen(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        message = f'Operator update {unique_suffix()}'
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        send_report_message(page, report_id, message)
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go(f'/reports/{report_id}')
        page.by_id_visible('messages-list')
        page.wait.until(
            lambda d: any(
                message in el.text
                for el in d.find_elements(By.XPATH, "//ul[attribute::id='messages-list']//*[contains(attribute::id,'-body')]")
            ),
            message='Citizen should see the message sent by the operator',
        )

    def test_operator_cannot_send_empty_message(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go(f'/reports/{report_id}')
        body = page.by_id_visible('report-message-body')
        page.click('report-message-submit')  # body left empty
        is_valid = page.driver.execute_script("return arguments[0].checkValidity();", body)
        assert is_valid is False, 'Empty required message body should block submission'
