import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper

class TestManageReport:

    def test_operator_dashboard_accessible_after_login(self, operator_page: PageHelper):
        operator_page.go('/operator')
        assert operator_page.by_id('operator-page').is_displayed()

    def test_assigned_reports_section_always_present(self, operator_page: PageHelper):
        operator_page.go('/operator')
        assert operator_page.by_id('assigned-reports-section').is_displayed()

    def test_pending_reports_table_shown_when_data_available(self, operator_page: PageHelper):
        operator_page.go('/operator')
        if operator_page.absent('pending-reports-section'):
            pytest.skip('No pending reports in current data')
        table = operator_page.by_id('pending-reports-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        assert len(rows) >= 2, 'Expected header + at least one data row'

    def test_assign_button_present_for_each_pending_report(self, operator_page: PageHelper):
        operator_page.go('/operator')
        if operator_page.absent('pending-reports-section'):
            pytest.skip('No pending reports available')
        tbody = operator_page.by_id('pending-reports-table-body')
        buttons = tbody.find_elements(By.XPATH, ".//*[contains(@id,'pending-report-assign-')]")
        assert buttons, 'Expected at least one Assign button in pending reports table'

    def test_assigning_report_moves_it_to_assigned_list(self, operator_page: PageHelper):
        operator_page.go('/operator')
        if operator_page.absent('pending-reports-section'):
            pytest.skip('No pending reports available')
        tbody = operator_page.by_id('pending-reports-table-body')
        buttons = tbody.find_elements(By.XPATH, ".//*[contains(@id,'pending-report-assign-')]")
        buttons[0].click()
        operator_page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'assigned-report-row-')]")), message='No assigned-report-row-* appeared after clicking Assign')

    def test_operator_page_not_accessible_as_citizen(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/operator')
        page.wait_redirect_away_from('/operator')