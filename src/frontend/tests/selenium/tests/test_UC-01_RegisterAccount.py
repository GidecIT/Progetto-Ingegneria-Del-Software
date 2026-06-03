from conftest import PageHelper, unique_suffix

class TestRegisterAccount:

    def test_register_page_renders(self, page: PageHelper):
        page.go('/register')
        assert page.by_id_visible('register-page').is_displayed()
        assert page.by_id('register-form').is_displayed()

    def test_successful_registration_shows_success_message(self, page: PageHelper):
        sfx = unique_suffix()
        page.go('/register')
        page.fill('register-username', f'user_{sfx}')
        page.fill('register-first-name', 'Test')
        page.fill('register-last-name', 'Citizen')
        page.fill('register-email', f'user_{sfx}@test.local')
        page.fill('register-password', 'TestPass123!')
        page.click('register-submit')
        success = page.by_id_visible('register-success')
        assert success.text.strip(), 'Success message should not be empty'

    def test_verification_link_exposed_in_local_env(self, page: PageHelper):
        sfx = unique_suffix()
        page.go('/register')
        page.fill('register-username', f'ver_{sfx}')
        page.fill('register-first-name', 'Ver')
        page.fill('register-last-name', 'Test')
        page.fill('register-email', f'ver_{sfx}@test.local')
        page.fill('register-password', 'TestPass123!')
        page.click('register-submit')
        box = page.by_id_visible('verification-box')
        link = box.find_element('id', 'verification-link')
        href = link.get_attribute('href')
        assert href and 'verify' in href.lower(), f"Verification link href '{href}' does not look valid"

    def test_duplicate_email_shows_error(self, page: PageHelper):
        page.go('/register')
        page.fill('register-username', f'dup_{unique_suffix()}')
        page.fill('register-first-name', 'Dup')
        page.fill('register-last-name', 'User')
        page.fill('register-email', 'citizen@example.com')
        page.fill('register-password', 'TestPass123!')
        page.click('register-submit')
        error = page.by_id_visible('register-error')
        assert 'email' in error.text.lower(), f"Expected an email-related error, got: '{error.text}'"

    def test_duplicate_username_shows_error(self, page: PageHelper):
        # UC-01 ext 4a: username already taken -> system asks for a different one.
        # 'citizen' is the seeded account username; the email is unique so only the
        # username collides.
        page.go('/register')
        page.fill('register-username', 'citizen')
        page.fill('register-first-name', 'Dup')
        page.fill('register-last-name', 'User')
        page.fill('register-email', f'dupuser_{unique_suffix()}@test.local')
        page.fill('register-password', 'TestPass123!')
        page.click('register-submit')
        error = page.by_id_visible('register-error')
        assert 'username' in error.text.lower(), f"Expected a username-related error, got: '{error.text}'"

    def test_missing_required_field_blocks_submission(self, page: PageHelper):
        # UC-01 ext 4c: a required field is missing -> the form is not submitted and
        # the empty field is flagged. Every input is HTML5 `required`, so the browser
        # blocks submission natively: no backend call, no success message.
        page.go('/register')
        page.fill('register-first-name', 'Missing')  # username intentionally left empty
        page.fill('register-last-name', 'Field')
        page.fill('register-email', f'missing_{unique_suffix()}@test.local')
        page.fill('register-password', 'TestPass123!')
        page.click('register-submit')
        username = page.by_id('register-username')
        is_valid = page.driver.execute_script("return arguments[0].checkValidity();", username)
        assert is_valid is False, 'Empty required username should be invalid and block submission'
        assert page.absent('register-success'), 'Form must not submit while a required field is missing'

    def test_expired_or_invalid_verification_link_keeps_account_inactive(self, page: PageHelper):
        # UC-01 ext 5a: an expired/unused verification link leaves the account
        # inactive (ends with failure). A real 48h expiry cannot be forced from the
        # UI, so we exercise the same guarantee by tampering the token (when the link
        # is exposed) and/or simply never using a valid link, then prove the account
        # is still unverified because login is rejected.
        sfx = unique_suffix()
        email = f'unverified_{sfx}@test.local'
        password = 'TestPass123!'
        page.go('/register')
        page.fill('register-username', f'unverified_{sfx}')
        page.fill('register-first-name', 'Unverified')
        page.fill('register-last-name', 'Citizen')
        page.fill('register-email', email)
        page.fill('register-password', password)
        page.click('register-submit')
        if page.present('verification-box', timeout=2):
            href = page.by_id_visible('verification-box').find_element('id', 'verification-link').get_attribute('href')
            invalid_href = href.rsplit('/', 1)[0] + '/expired-or-invalid-token'
            page.driver.get(invalid_href)
        page.go('/login')
        page.fill('login-identifier', email)
        page.fill('login-password', password)
        page.click('login-submit')
        error = page.by_id_visible('login-error')
        assert 'verif' in error.text.lower(), f"Expected a verification-required error, got: '{error.text}'"
        assert page.absent('logout-button'), 'Account must remain inactive after an invalid/unused verification link'