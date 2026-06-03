import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import (
    CITIZEN_EMAIL,
    CITIZEN_PASSWORD,
    OPERATOR_EMAIL,
    OPERATOR_PASSWORD,
    PageHelper,
    create_and_assign_report,
    create_report_and_get_id,
    update_report_status_as_operator,
)

class TestManageReport:

    def test_operator_dashboard_accessible_after_login(self, operator_page: PageHelper):
        operator_page.go('/operator')
        assert operator_page.by_id_visible('operator-page').is_displayed()

    def test_assigned_reports_section_always_present(self, operator_page: PageHelper):
        operator_page.go('/operator')
        assert operator_page.by_id_visible('assigned-reports-section').is_displayed()

    def test_pending_reports_table_shown_when_data_available(self, operator_page: PageHelper):
        operator_page.go('/operator')
        # If no pending reports, try to create one to make the test deterministic
        if operator_page.absent('pending-reports-section', timeout=3):
            create_report_and_get_id(operator_page)
            operator_page.go('/operator')
        
        table = operator_page.by_id_visible('pending-reports-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        assert len(rows) >= 2, 'Expected header + at least one data row'

    def test_assign_button_present_for_each_pending_report(self, operator_page: PageHelper):
        operator_page.go('/operator')
        if operator_page.absent('pending-reports-section', timeout=3):
            create_report_and_get_id(operator_page)
            operator_page.go('/operator')
            
        tbody = operator_page.by_id_visible('pending-reports-table-body')
        buttons = tbody.find_elements(By.XPATH, ".//*[contains(attribute::id,'pending-report-assign-')]")
        assert buttons, 'Expected at least one Assign button in pending reports table'

    def test_assigning_report_moves_it_to_assigned_list(self, operator_page: PageHelper):
        operator_page.go('/operator')
        if operator_page.absent('pending-reports-section', timeout=3):
            create_report_and_get_id(operator_page)
            operator_page.go('/operator')
            
        tbody = operator_page.by_id_visible('pending-reports-table-body')
        buttons = tbody.find_elements(By.XPATH, ".//*[contains(attribute::id,'pending-report-assign-')]")
        btn_id = buttons[0].get_attribute('id')
        operator_page.click(btn_id)
        operator_page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(attribute::id,'assigned-report-row-')]")), message='No assigned-report-row-* appeared after clicking Assign')

    def test_operator_page_not_accessible_as_citizen(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/operator')
        page.wait_redirect_away_from('/operator')

    def test_operator_updates_status_from_assigned_to_in_progress(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        update_report_status_as_operator(page, report_id, 'In Progress')
        page.go(f'/reports/{report_id}')
        page.wait.until(
            lambda d: 'In Progress' in d.find_element(By.ID, 'report-detail-status').text,
            message='Report status should become In Progress after the operator update',
        )

    def test_rejecting_without_motivation_is_blocked(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go('/operator')
        page.by_id_visible(f'assigned-report-row-{report_id}')
        page.select_by_value(f'assigned-report-status-{report_id}', 'Rejected')  # note left empty
        page.click(f'assigned-report-update-{report_id}')
        error = page.by_id_visible('operator-error')
        assert 'reason' in error.text.lower() or 'motiv' in error.text.lower(), f"Expected a rejection-reason error, got: '{error.text}'"
        page.go(f'/reports/{report_id}')
        assert 'Rejected' not in page.by_id_visible('report-detail-status').text, 'Report must not be rejected without a motivation'

    def test_status_change_notifies_reporter(self, page: PageHelper):
        report_id = create_and_assign_report(page)
        update_report_status_as_operator(page, report_id, 'In Progress')
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/dashboard')
        page.by_id_visible('notifications-card')
        page.wait.until(
            lambda d: any(
                f'#{report_id}' in el.text
                for el in d.find_elements(By.XPATH, "//*[contains(attribute::id,'notification-item-') and contains(attribute::id,'-body')]")
            ),
            message=f'Reporter should receive a status-change notification for report #{report_id}',
        )
