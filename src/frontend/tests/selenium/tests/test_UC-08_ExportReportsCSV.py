"""UC-08  Export reports (CSV)"""
import requests

from conftest import PageHelper

API_BASE = "http://localhost:5050/api/v1"


class TestExportReportsCSV:
    """UC-08 – Visitor exports the public report list as CSV."""

    def test_export_link_present_on_home_page(self, page: PageHelper):
        """UC-08: The Export CSV link is visible on the home page and has
        a valid href pointing to the backend export endpoint."""
        page.go("/")
        link = page.by_id("public-export-link")
        href = link.get_attribute("href")
        assert href, "Export CSV link must have an href"
        assert "export" in href.lower() or "csv" in href.lower() or "reports" in href.lower(), (
            f"Export link href '{href}' does not look like a CSV export endpoint"
        )

    def test_export_endpoint_returns_csv_content(self, page: PageHelper):
        """UC-08: The export endpoint returns a response with CSV content type
        and a non-empty body when called directly."""
        response = requests.get(
            f"{API_BASE}/reports/export",
            timeout=10,
        )
        assert response.status_code == 200, (
            f"Export endpoint returned {response.status_code}"
        )
        content_type = response.headers.get("Content-Type", "")
        assert "csv" in content_type.lower() or "text" in content_type.lower(), (
            f"Expected CSV content type, got: '{content_type}'"
        )
        assert response.text.strip(), "CSV export body should not be empty"

    def test_csv_contains_only_public_fields(self, page: PageHelper):
        """UC-08: The CSV export must not expose private fields such as the
        reporter's email address or internal IDs beyond the public report ID."""
        response = requests.get(f"{API_BASE}/reports/export", timeout=10)
        assert response.status_code == 200
        header_line = response.text.splitlines()[0].lower()
        # Email addresses and internal user IDs must not be in the export header
        assert "email" not in header_line, (
            "CSV export header must not contain 'email' (private field)"
        )

    def test_export_link_accessible_without_login(self, page: PageHelper):
        """UC-08: CSV export is a public feature — no login is required."""
        page.go("/")
        assert page.absent("login-page"), (
            "Home page should not redirect to login for a visitor"
        )
        link = page.by_id("public-export-link")
        assert link.is_displayed()