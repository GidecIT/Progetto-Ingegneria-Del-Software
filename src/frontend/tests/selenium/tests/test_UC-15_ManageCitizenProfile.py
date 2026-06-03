from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix

class TestManageCitizenProfile:

    def test_dashboard_shows_profile_form(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        assert page.by_id('profile-section').is_displayed()
        assert page.by_id('profile-form').is_displayed()

    def test_profile_form_pre_filled_with_current_data(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        username = page.by_id('profile-username').get_attribute('value')
        assert username, 'Username field should be pre-filled'
        email = page.by_id('profile-email').get_attribute('value')
        assert email, 'Email field should be pre-filled'

    def test_update_first_name_saves_and_confirms(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        new_name = f'Auto{unique_suffix()}'
        page.fill('profile-first-name', new_name)
        page.click('profile-save')
        success = page.by_id_visible('profile-success')
        assert success.text.strip(), 'Success message should not be empty'

    def test_email_notifications_checkbox_present(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        cb = page.by_id('profile-email-notifications')
        assert cb.is_displayed(), 'Email notifications checkbox should be visible'

    def test_profile_picture_upload_field_present(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        assert page.by_id('profile-picture').is_displayed()

    def test_my_reports_table_visible_on_dashboard(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        assert page.by_id('my-reports-table').is_displayed()

    def test_notifications_card_visible_on_dashboard(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        assert page.by_id('notifications-card').is_displayed()

    def test_dashboard_not_accessible_as_guest(self, page: PageHelper):
        page.go('/dashboard')
        page.wait_for_url('/login')
        assert '/login' in page.driver.current_url