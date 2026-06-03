import requests
from conftest import PageHelper
API_BASE = 'http://localhost:5050/api/v1'

class TestExportReportsCSV:

    def test_export_link_present_on_home_page(self, page: PageHelper):
        page.go('/')
        link = page.by_id('public-export-link')
        href = link.get_attribute('href')
        assert href, 'Export CSV link must have an href'
        assert 'export' in href.lower() or 'csv' in href.lower() or 'reports' in href.lower(), f"Export link href '{href}' does not look like a CSV export endpoint"

    def test_export_endpoint_returns_csv_content(self, page: PageHelper):
        response = requests.get(f'{API_BASE}/reports/export', timeout=10)
        assert response.status_code == 200, f'Export endpoint returned {response.status_code}'
        content_type = response.headers.get('Content-Type', '')
        assert 'csv' in content_type.lower() or 'text' in content_type.lower(), f"Expected CSV content type, got: '{content_type}'"
        assert response.text.strip(), 'CSV export body should not be empty'

    def test_csv_contains_only_public_fields(self, page: PageHelper):
        response = requests.get(f'{API_BASE}/reports/export', timeout=10)
        assert response.status_code == 200
        header_line = response.text.splitlines()[0].lower()
        assert 'email' not in header_line, "CSV export header must not contain 'email' (private field)"

    def test_export_link_accessible_without_login(self, page: PageHelper):
        page.go('/')
        assert page.absent('login-page'), 'Home page should not redirect to login for a visitor'
        link = page.by_id('public-export-link')
        assert link.is_displayed()