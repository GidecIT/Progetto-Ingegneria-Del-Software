import csv
import io
import pytest
import requests
from conftest import PageHelper
API_BASE = 'http://localhost:5050/api/v1'

PUBLIC_CSV_FIELDS = ['id', 'title', 'category', 'status', 'created_at', 'latitude', 'longitude']
PRIVATE_CSV_FIELDS = {'email', 'reporter', 'description', 'username', 'first_name', 'last_name', 'password', 'is_anonymous'}

def _export_csv(**params) -> list[dict]:
    response = requests.get(f'{API_BASE}/reports/export', params=params, timeout=10)
    response.raise_for_status()
    return list(csv.DictReader(io.StringIO(response.text)))

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

    def test_csv_header_is_exactly_the_public_field_set(self, page: PageHelper):
        response = requests.get(f'{API_BASE}/reports/export', timeout=10)
        assert response.status_code == 200
        header = [h.strip().lower() for h in next(csv.reader(io.StringIO(response.text)))]
        assert header == PUBLIC_CSV_FIELDS, f'Unexpected CSV header: {header}'
        leaked = set(header) & PRIVATE_CSV_FIELDS
        assert not leaked, f'CSV header must not expose private fields, found: {leaked}'

    def test_export_respects_active_category_filter(self, page: PageHelper):
        all_reports = requests.get(f'{API_BASE}/reports', timeout=10).json()
        if not all_reports:
            pytest.skip('No public reports available to derive a category filter')
        category = all_reports[0]['category']
        category_id, category_name = category['id'], category['name']
        filtered_list = requests.get(f'{API_BASE}/reports', params={'category_id': category_id}, timeout=10).json()
        expected_ids = {str(r['id']) for r in filtered_list}
        rows = _export_csv(category_id=category_id)
        exported_ids = {row['id'] for row in rows}
        assert exported_ids == expected_ids, f'Filtered export ids {exported_ids} should match filtered list ids {expected_ids}'
        assert all(row['category'] == category_name for row in rows), 'Every exported row should belong to the filtered category'

    def test_export_with_no_matches_returns_header_only(self, page: PageHelper):
        response = requests.get(f'{API_BASE}/reports/export', params={'date_from': '2999-01-01'}, timeout=10)
        assert response.status_code == 200
        lines = response.text.splitlines()
        assert lines and [h.strip().lower() for h in lines[0].split(',')] == PUBLIC_CSV_FIELDS, 'Header should still be present'
        assert list(csv.DictReader(io.StringIO(response.text))) == [], 'Export should contain no data rows when nothing matches'

    def test_export_sets_content_disposition_attachment(self, page: PageHelper):
        response = requests.get(f'{API_BASE}/reports/export', timeout=10)
        disposition = response.headers.get('Content-Disposition', '')
        assert 'attachment' in disposition.lower(), f'Expected an attachment download, got: {disposition!r}'
        assert 'participium_reports.csv' in disposition, f'Expected the CSV filename, got: {disposition!r}'

    def test_export_link_accessible_without_login(self, page: PageHelper):
        page.go('/')
        assert page.absent('login-page'), 'Home page should not redirect to login for a visitor'
        link = page.by_id('public-export-link')
        assert link.is_displayed()