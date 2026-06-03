from conftest import PageHelper, register_account, submit_login

class TestRegisterAccount:

    def test_register_page_renders(self, page: PageHelper):
        page.go('/register')
        assert page.by_id_visible('register-page').is_displayed()
        assert page.by_id('register-form').is_displayed()

    def test_successful_registration_shows_success_message(self, page: PageHelper):
        register_account(page)
        success = page.by_id_visible('register-success')
        assert success.text.strip(), 'Success message should not be empty'

    def test_verification_link_exposed_in_local_env(self, page: PageHelper):
        register_account(page)
        box = page.by_id_visible('verification-box')
        link = box.find_element('id', 'verification-link')
        href = link.get_attribute('href')
        assert href and 'verify' in href.lower(), f"Verification link href '{href}' does not look valid"

    def test_duplicate_email_shows_error(self, page: PageHelper):
        register_account(page, email='citizen@example.com')
        error = page.by_id_visible('register-error')
        assert 'email' in error.text.lower(), f"Expected an email-related error, got: '{error.text}'"

    def test_duplicate_username_shows_error(self, page: PageHelper):
        register_account(page, username='citizen')
        error = page.by_id_visible('register-error')
        assert 'username' in error.text.lower(), f"Expected a username-related error, got: '{error.text}'"

    def test_missing_required_field_blocks_submission(self, page: PageHelper):
        register_account(page, username='')  # username left empty on purpose
        username = page.by_id('register-username')
        is_valid = page.driver.execute_script("return arguments[0].checkValidity();", username)
        assert is_valid is False, 'Empty required username should be invalid and block submission'
        assert page.absent('register-success'), 'Form must not submit while a required field is missing'

    def test_expired_or_invalid_verification_link_keeps_account_inactive(self, page: PageHelper):
        creds = register_account(page)
        if page.present('verification-box', timeout=2):
            href = page.by_id_visible('verification-box').find_element('id', 'verification-link').get_attribute('href')
            invalid_href = href.rsplit('/', 1)[0] + '/expired-or-invalid-token'
            page.driver.get(invalid_href)
        submit_login(page, creds['email'], creds['password'])
        error = page.by_id_visible('login-error')
        assert 'verif' in error.text.lower(), f"Expected a verification-required error, got: '{error.text}'"
        assert page.absent('logout-button'), 'Account must remain inactive after an invalid/unused verification link'
