from selenium.webdriver.common.by import By
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

    def test_toggling_email_notifications_persists(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        checkbox = page.by_id('profile-email-notifications')
        initial = checkbox.is_selected()
        checkbox.click()
        page.click('profile-save')
        page.by_id_visible('profile-success')
        page.go('/dashboard')
        page.wait_for_url('/dashboard')
        page.wait.until(
            lambda d: d.find_element(By.ID, 'profile-email-notifications').is_selected() == (not initial),
            message='Email-notification preference should persist after toggling',
        )

    def test_canceling_changes_without_saving_keeps_profile(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        original = page.by_id('profile-first-name').get_attribute('value')
        page.fill('profile-first-name', f'Discarded{unique_suffix()}')  # do NOT save
        page.go('/')  # navigate away without saving
        page.go('/dashboard')
        page.wait_for_url('/dashboard')
        page.wait.until(
            lambda d: d.find_element(By.ID, 'profile-first-name').get_attribute('value') == original,
            message='Unsaved profile change must be discarded',
        )

    def test_dashboard_not_accessible_as_guest(self, page: PageHelper):
        page.go('/dashboard')
        page.wait_for_url('/login')
        assert '/login' in page.driver.current_url