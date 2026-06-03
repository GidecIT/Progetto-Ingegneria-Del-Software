from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from conftest import PageHelper

def _wait_for_statistics_data(page: PageHelper) -> None:
    page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(attribute::id,'public-category-stat-')]")), message='No public-category-stat-* element found; statistics API response may not have arrived yet')

class TestViewPublicStatistics:

    def test_statistics_section_visible(self, page: PageHelper):
        page.go('/')
        assert page.by_id_visible('public-statistics-card').is_displayed()

    def test_total_reports_metric_shown(self, page: PageHelper):
        page.go('/')
        total = page.by_id('public-total-reports-value')
        assert total.is_displayed()

    def test_reports_by_category_list_present(self, page: PageHelper):
        page.go('/')
        _wait_for_statistics_data(page)
        assert page.by_id('public-category-statistics').is_displayed()
        cat_list = page.by_id('public-category-statistics-list')
        items = cat_list.find_elements(By.TAG_NAME, 'li')
        assert len(items) > 0, 'Category statistics list should contain at least one entry'

    def test_trend_statistics_section_present(self, page: PageHelper):
        page.go('/')
        assert page.by_id('public-trend-statistics').is_displayed()

    def test_granularity_selector_has_day_week_month_options(self, page: PageHelper):
        page.go('/')
        sel = Select(page.by_id('public-stat-granularity'))
        values = [o.get_attribute('value') for o in sel.options]
        assert 'day' in values, 'Day option must be available'
        assert 'week' in values, 'Week option must be available'
        assert 'month' in values, 'Month option must be available'

    def test_changing_granularity_updates_trend_buckets(self, page: PageHelper):
        page.go('/')

        def _trend_bucket_ids() -> set[str]:
            return {
                el.get_attribute('id')
                for el in page.driver.find_elements(By.XPATH, "//li[starts-with(attribute::id,'public-trend-stat-')]")
            }

        page.select_by_value('public-stat-granularity', 'day')
        page.wait.until(lambda d: _trend_bucket_ids(), message='Trend should render at least one day bucket')
        day_buckets = _trend_bucket_ids()
        page.select_by_value('public-stat-granularity', 'month')
        page.wait.until(lambda d: _trend_bucket_ids() != day_buckets, message='Trend buckets should change after switching to month granularity')
        assert _trend_bucket_ids() != day_buckets

    def test_statistics_accessible_without_login(self, page: PageHelper):
        page.go('/')
        assert page.absent('login-page'), 'Statistics should be visible without login'
        assert page.by_id('public-statistics-card').is_displayed()