import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix

def _wait_for_category_rows(page: PageHelper) -> None:
    page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'admin-category-row-')]")), message='No admin-category-row-* found; categories may not have loaded')

def _get_first_non_admin_user_id(page: PageHelper) -> str:
    page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url('/admin')
    page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'admin-user-row-')]")), message='No admin-user-row-* found; admin users may not have loaded')
    tbody = page.by_id('admin-users-table-body')
    for row in tbody.find_elements(By.TAG_NAME, 'tr'):
        row_id = row.get_attribute('id')
        uid = row_id.split('-')[-1]
        role_els = row.find_elements(By.ID, f'admin-user-role-{uid}')
        if role_els:
            role = Select(role_els[0]).first_selected_option.get_attribute('value')
            if role != 'admin':
                return uid
    pytest.skip('No non-admin user found in the admin users table')

class TestManageCategoriesAndConfiguration:

    def test_categories_table_rendered(self, admin_page: PageHelper):
        admin_page.go('/admin')
        assert admin_page.by_id('admin-categories-section').is_displayed()
        assert admin_page.by_id('admin-categories-table').is_displayed()

    def test_create_category_form_present(self, admin_page: PageHelper):
        admin_page.go('/admin')
        assert admin_page.by_id('admin-category-form').is_displayed()
        assert admin_page.by_id('admin-new-category-name').is_displayed()
        assert admin_page.by_id('admin-new-category-submit').is_displayed()

    def test_create_new_category_shows_success_and_appears_in_table(self, admin_page: PageHelper):
        cat_name = f'Cat{unique_suffix()}'
        admin_page.go('/admin')
        admin_page.fill('admin-new-category-name', cat_name)
        admin_page.click('admin-new-category-submit')
        msg = admin_page.by_id_visible('admin-success')
        assert msg.text.strip(), 'Expected a non-empty success message'
        tbody = admin_page.by_id('admin-categories-table-body')
        name_inputs = tbody.find_elements(By.XPATH, f".//input[@value='{cat_name}']")
        assert name_inputs, f"Newly created category '{cat_name}' not found in table"

    def test_edit_category_name_saves_successfully(self, admin_page: PageHelper):
        admin_page.go('/admin')
        _wait_for_category_rows(admin_page)
        tbody = admin_page.by_id('admin-categories-table-body')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        assert rows, 'Expected at least one category row'
        cat_id = rows[0].get_attribute('id').split('-')[-1]
        name_input = admin_page.by_id(f'admin-category-name-{cat_id}')
        name_input.clear()
        name_input.send_keys(f'Edited{unique_suffix()}')
        admin_page.click(f'admin-category-save-{cat_id}')
        msg = admin_page.by_id_visible('admin-success')
        assert msg.text.strip(), 'Expected a non-empty success message after edit'

    def test_toggle_category_active_flag_saves(self, admin_page: PageHelper):
        admin_page.go('/admin')
        _wait_for_category_rows(admin_page)
        tbody = admin_page.by_id('admin-categories-table-body')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        assert rows, 'Expected at least one category row'
        cat_id = rows[0].get_attribute('id').split('-')[-1]
        admin_page.by_id(f'admin-category-active-{cat_id}').click()
        admin_page.click(f'admin-category-save-{cat_id}')
        msg = admin_page.by_id_visible('admin-success')
        assert msg.text.strip()

    def test_admin_creates_operator_user(self, admin_page: PageHelper):
        sfx = unique_suffix()
        email = f'operator_{sfx}@test.local'
        admin_page.go('/admin')
        admin_page.fill('admin-new-user-username', f'operator_{sfx}')
        admin_page.fill('admin-new-user-first-name', 'Op')
        admin_page.fill('admin-new-user-last-name', 'Test')
        admin_page.fill('admin-new-user-email', email)
        admin_page.fill('admin-new-user-password', 'TestPass123!')
        admin_page.select_by_value('admin-new-user-role', 'operator')
        admin_page.click('admin-new-user-submit')
        msg = admin_page.by_id_visible('admin-success')
        assert msg.text.strip()
        tbody = admin_page.by_id('admin-users-table-body')
        admin_page.wait.until(lambda d: any((el.get_property('value') == email for el in tbody.find_elements(By.XPATH, ".//input[@type='email']"))), message=f'Created user {email} not found in users table')

    def test_admin_edits_user_first_name(self, admin_page: PageHelper):
        uid = _get_first_non_admin_user_id(admin_page)
        admin_page.go('/admin')
        fn = admin_page.by_id(f'admin-user-first-name-{uid}')
        fn.clear()
        fn.send_keys(f'Edited{unique_suffix()}')
        admin_page.click(f'admin-user-save-{uid}')
        msg = admin_page.by_id_visible('admin-success')
        assert msg.text.strip(), 'Expected a non-empty success message after edit'

    def test_configuration_not_accessible_as_citizen(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/admin')
        page.wait_redirect_away_from('/admin')