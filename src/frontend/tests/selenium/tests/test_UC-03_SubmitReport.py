import os
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix, write_temp_image

class TestSubmitReport:

    def test_submit_form_accessible_after_login(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        assert page.by_id_visible('nav-new-report').is_displayed(), 'New Report nav link should be visible for citizens'
        page.go('/reports/new')
        assert page.by_id_visible('new-report-page').is_displayed()
        assert page.by_id('new-report-form').is_displayed()

    def test_location_fields_pre_filled(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/reports/new')
        lat = page.by_id('report-latitude').get_attribute('value')
        lon = page.by_id('report-longitude').get_attribute('value')
        assert lat, 'Latitude should be pre-filled'
        assert lon, 'Longitude should be pre-filled'

    def test_anonymous_option_available(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/reports/new')
        assert page.by_id('report-anonymous').is_displayed()

    def test_successful_submission_creates_report_with_pending_status(self, page: PageHelper):
        img = write_temp_image()
        try:
            page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
            page.go('/reports/new')
            title = f'Selenium report {unique_suffix()}'
            page.fill('report-title', title)
            page.fill('report-description', 'Automated test report description.')
            page.by_id('report-photos').send_keys(img)
            page.click('new-report-submit')
            page.wait_for_url('/reports/')
            assert page.by_id('report-detail-page').is_displayed()
            assert title in page.by_id('report-detail-title').text, 'Report title should appear on the detail page'
            status_el = page.by_id('report-detail-status')
            assert 'Pending' in status_el.text, f"New report should have Pending Approval status, got: '{status_el.text}'"
        finally:
            os.unlink(img)

    def test_submit_page_not_accessible_as_guest(self, page: PageHelper):
        page.go('/reports/new')
        page.wait_for_url('/login')
        assert '/login' in page.driver.current_url