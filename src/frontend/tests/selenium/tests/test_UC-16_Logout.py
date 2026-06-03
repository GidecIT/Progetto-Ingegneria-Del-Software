from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper

class TestLogout:

    def test_successful_logout(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        page.click('logout-button')
        assert page.by_id_visible('nav-login').is_displayed(), 'Login link should be visible after logout'
        assert page.absent('logout-button'), 'Logout button should not be visible after logout'

    def test_restricted_functions_inaccessible_after_logout(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.logout()
        page.go('/reports/new')
        page.wait_for_url('/login')
        assert '/login' in page.driver.current_url, 'User should be redirected to login when accessing a restricted area after logout'

    def test_logout_returns_to_non_restricted_area(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        page.click('logout-button')
        page.by_id_visible('nav-login')
        assert '/dashboard' not in page.driver.current_url, 'Logout should leave the restricted dashboard'
        page.go('/')
        assert page.absent('login-page'), 'A non-restricted area (home) must be accessible after logout'

    def test_operator_logout(self, page: PageHelper):
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.click('logout-button')
        assert page.by_id_visible('nav-login').is_displayed(), 'Login link should be visible after operator logout'
        assert page.absent('logout-button'), 'Logout button should not be visible after operator logout'

    def test_admin_logout(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.click('logout-button')
        assert page.by_id_visible('nav-login').is_displayed(), 'Login link should be visible after admin logout'
        assert page.absent('logout-button'), 'Logout button should not be visible after admin logout'

    def test_expired_session_redirects_to_login(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url('/dashboard')
        page.driver.delete_all_cookies()
        page.driver.execute_script('window.localStorage.clear(); window.sessionStorage.clear();')
        page.driver.refresh()
        page.wait_for_url('/login')
        assert '/login' in page.driver.current_url, 'User with an expired/cleared session should be redirected away from restricted pages'
        assert page.absent('logout-button')