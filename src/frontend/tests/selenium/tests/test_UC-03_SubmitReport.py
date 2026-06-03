import os
from selenium.webdriver.support.ui import Select
from conftest import OPERATOR_CATEGORY, PageHelper, select_operator_category, unique_suffix, write_temp_image

class TestSubmitReport:

    def test_submit_form_accessible_after_login(self, citizen_page: PageHelper):
        assert citizen_page.by_id_visible('nav-new-report').is_displayed(), 'New Report nav link should be visible for citizens'
        citizen_page.go('/reports/new')
        assert citizen_page.by_id_visible('new-report-page').is_displayed()
        assert citizen_page.by_id('new-report-form').is_displayed()

    def test_location_fields_pre_filled(self, citizen_page: PageHelper):
        citizen_page.go('/reports/new')
        lat = citizen_page.by_id('report-latitude').get_attribute('value')
        lon = citizen_page.by_id('report-longitude').get_attribute('value')
        assert lat, 'Latitude should be pre-filled'
        assert lon, 'Longitude should be pre-filled'

    def test_anonymous_option_available(self, citizen_page: PageHelper):
        citizen_page.go('/reports/new')
        assert citizen_page.by_id('report-anonymous').is_displayed()

    def test_successful_submission_creates_report_with_pending_status(self, citizen_page: PageHelper):
        img = write_temp_image()
        try:
            citizen_page.go('/reports/new')
            title = f'Selenium report {unique_suffix()}'
            citizen_page.fill('report-title', title)
            citizen_page.fill('report-description', 'Automated test report description.')
            citizen_page.by_id('report-photos').send_keys(img)
            citizen_page.click('new-report-submit')
            citizen_page.wait_for_url('/reports/')
            assert citizen_page.by_id('report-detail-page').is_displayed()
            assert title in citizen_page.by_id('report-detail-title').text, 'Report title should appear on the detail page'
            status_el = citizen_page.by_id('report-detail-status')
            assert 'Pending' in status_el.text, f"New report should have Pending Approval status, got: '{status_el.text}'"
        finally:
            os.unlink(img)

    def test_submit_page_not_accessible_as_guest(self, page: PageHelper):
        page.go('/reports/new')
        page.wait_for_url('/login')
        assert '/login' in page.driver.current_url

    def test_category_dropdown_populated_and_selectable(self, citizen_page: PageHelper):
        citizen_page.go('/reports/new')
        select = Select(citizen_page.by_id('report-category'))
        assert len(select.options) >= 1, 'Category dropdown should be populated from configured categories'
        select_operator_category(citizen_page)
        assert select.first_selected_option.text.strip() == OPERATOR_CATEGORY

    def test_missing_location_blocks_submission(self, citizen_page: PageHelper):
        citizen_page.go('/reports/new')
        citizen_page.fill('report-title', f'No location {unique_suffix()}')
        citizen_page.fill('report-description', 'Location-not-selected scenario.')
        latitude = citizen_page.by_id_visible('report-latitude')
        citizen_page._set_value(latitude, '')  # simulate no position chosen on the map
        img = write_temp_image()
        try:
            citizen_page.by_id('report-photos').send_keys(img)
            citizen_page.click('new-report-submit')
            is_valid = citizen_page.driver.execute_script("return arguments[0].checkValidity();", latitude)
            assert is_valid is False, 'Empty required latitude should block submission'
            assert citizen_page.driver.current_url.rstrip('/').endswith('/reports/new'), 'Form must not navigate away without a location'
        finally:
            os.unlink(img)

    def test_missing_required_field_blocks_submission(self, citizen_page: PageHelper):
        citizen_page.go('/reports/new')
        citizen_page.fill('report-description', 'Missing-title scenario.')  # title left empty
        img = write_temp_image()
        try:
            citizen_page.by_id('report-photos').send_keys(img)
            citizen_page.click('new-report-submit')
            title = citizen_page.by_id('report-title')
            is_valid = citizen_page.driver.execute_script("return arguments[0].checkValidity();", title)
            assert is_valid is False, 'Empty required title should block submission'
            assert citizen_page.driver.current_url.rstrip('/').endswith('/reports/new'), 'Form must not submit while a required field is missing'
        finally:
            os.unlink(img)

    def test_more_than_three_photos_are_capped(self, citizen_page: PageHelper):
  
        citizen_page.go('/reports/new')
        paths = [write_temp_image() for _ in range(4)]
        try:
            citizen_page.by_id('report-photos').send_keys('\n'.join(paths))
            error = citizen_page.by_id_visible('new-report-error')
            assert '3' in error.text and 'photo' in error.text.lower(), f"Expected a max-3-photos warning, got: '{error.text}'"
            selected = citizen_page.by_id('new-report-selected-photos')
            assert 'Selected photos: 3' in selected.text, f"Only 3 photos should be kept, got: '{selected.text}'"
        finally:
            for path in paths:
                os.unlink(path)
