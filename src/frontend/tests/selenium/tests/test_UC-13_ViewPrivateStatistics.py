from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import ADMIN_EMAIL, ADMIN_PASSWORD, CITIZEN_EMAIL, CITIZEN_PASSWORD, OPERATOR_EMAIL, OPERATOR_PASSWORD, PageHelper

class TestViewPrivateStatistics:

    def test_statistics_section_rendered_for_admin(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url('/admin')
        assert page.by_id_visible('admin-statistics-section').is_displayed()
        assert page.by_id_visible('admin-stats-grid').is_displayed()

    def test_at_least_three_metric_columns_present(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url('/admin')
        page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(attribute::id,'admin-metric-item-')]")), message='No admin-metric-item-* element found')
        grid = page.by_id('admin-stats-grid')
        metric_items = grid.find_elements(By.XPATH, "./div[contains(attribute::id,'admin-metric-item-')]")
        assert len(metric_items) >= 3, f'Expected at least 3 metric columns, found {len(metric_items)}'

    def test_each_metric_column_renders_even_when_empty(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url('/admin')
        page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(attribute::id,'admin-metric-item-')]")), message='No admin-metric-item-* element found')
        grid = page.by_id('admin-stats-grid')
        metric_items = grid.find_elements(By.XPATH, "./div[contains(attribute::id,'admin-metric-item-')]")
        assert metric_items, 'Statistics grid rendered no metric columns'
        for item in metric_items:
            item_id = item.get_attribute('id')
            assert item.is_displayed(), f"Metric column '{item_id}' is not displayed"
            assert item.find_elements(By.TAG_NAME, 'h3'), f"Metric column '{item_id}' has no title"
            assert item.find_elements(By.XPATH, ".//ul[contains(attribute::id,'-list')]"), f"Metric column '{item_id}' has no list container"

    def test_private_statistics_not_accessible_as_operator(self, page: PageHelper):
        page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
        page.go('/admin')
        page.wait_redirect_away_from('/admin')

    def test_private_statistics_not_accessible_as_citizen(self, page: PageHelper):
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go('/admin')
        page.wait_redirect_away_from('/admin')

    def test_all_breakdown_columns_render_including_reporters(self, page: PageHelper):
        page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        page.wait_for_url('/admin')
        expected_columns = [
            'admin-metric-item-reports-by-status',
            'admin-metric-item-reports-by-type',
            'admin-metric-item-reports-by-reporter',
            'admin-metric-item-top-1-percent-by-type',
            'admin-metric-item-top-5-percent-by-type',
        ]
        for column_id in expected_columns:
            assert page.by_id_visible(column_id).is_displayed(), f'Breakdown column {column_id} should render'