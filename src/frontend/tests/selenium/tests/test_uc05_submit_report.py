"""
UC-05  Submit a new civic report (citizen role).
"""
import os
import tempfile

import pytest
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix


def _write_temp_image() -> str:
    """Create a minimal PNG-like file suitable for upload."""
    # 1×1 white PNG bytes (valid minimal PNG)
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
        b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
        b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    fd, path = tempfile.mkstemp(suffix=".png")
    with os.fdopen(fd, "wb") as fh:
        fh.write(png_bytes)
    return path


class TestSubmitReport:
    """UC-05 – Citizen submits a new report."""

    def test_uc05_new_report_page_renders(self, page: PageHelper):
        """UC-05: /reports/new is accessible after citizen login."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.by_id_visible("new-report-page")
        page.by_id("new-report-form")

    def test_uc05_nav_link_to_new_report_visible(self, page: PageHelper):
        """UC-05: After citizen login the 'New Report' nav link is shown."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.by_id_visible("nav-new-report")

    def test_uc05_submit_new_report_redirects_to_detail(self, page: PageHelper):
        """UC-05: Completing and submitting the new-report form navigates to
        the report detail page for the created report."""
        img_path = _write_temp_image()
        try:
            page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
            page.go("/reports/new")

            title = f"Selenium report {unique_suffix()}"
            page.fill("report-title", title)
            page.fill("report-description", "Automated test report description.")

            # category select – pick whatever is first (already pre-selected)
            # latitude / longitude already pre-filled with defaults

            # upload a photo (required)
            photo_input = page.by_id("report-photos")
            photo_input.send_keys(img_path)

            page.click("new-report-submit")
            page.wait_for_url("/reports/")
            page.by_id("report-detail-page")

            # Confirm title is shown on detail page
            title_el = page.by_id("report-detail-title")
            assert title in title_el.text, "Report title not shown on detail page"
        finally:
            os.unlink(img_path)

    def test_uc05_anonymous_report_option_available(self, page: PageHelper):
        """UC-05: The anonymous-submission checkbox is present on the form."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.by_id("report-anonymous")

    def test_uc05_location_fields_present(self, page: PageHelper):
        """UC-05: Latitude and longitude inputs are available and pre-filled."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        lat = page.by_id("report-latitude")
        lon = page.by_id("report-longitude")
        assert lat.get_attribute("value"), "Latitude should be pre-filled"
        assert lon.get_attribute("value"), "Longitude should be pre-filled"

    def test_uc05_new_report_not_accessible_as_guest(self, page: PageHelper):
        """UC-05: Unauthenticated access to /reports/new redirects to /login."""
        page.go("/reports/new")
        page.wait_for_url("/login")
