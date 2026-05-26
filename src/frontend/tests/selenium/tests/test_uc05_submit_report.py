"""UC-05  Submit a new civic report (citizen role)."""
import pytest
from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, unique_suffix, write_temp_image
import os


class TestSubmitReport:
    """UC-05 – Citizen submits a new report."""

    def test_new_report_page_renders(self, page: PageHelper):
        """UC-05: /reports/new is accessible after citizen login."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.by_id_visible("new-report-page")
        page.by_id("new-report-form")

    def test_nav_link_visible_for_citizen(self, page: PageHelper):
        """UC-05: After citizen login the 'New Report' nav link is shown."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.by_id_visible("nav-new-report")

    def test_submit_redirects_to_detail(self, page: PageHelper):
        """UC-05: Completing and submitting the form navigates to the report detail page."""
        img = write_temp_image()
        try:
            page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
            page.go("/reports/new")
            title = f"Selenium report {unique_suffix()}"
            page.fill("report-title", title)
            page.fill("report-description", "Automated test report description.")
            page.by_id("report-photos").send_keys(img)
            page.click("new-report-submit")
            page.wait_for_url("/reports/")
            page.by_id("report-detail-page")
            assert title in page.by_id("report-detail-title").text
        finally:
            os.unlink(img)

    def test_anonymous_option_available(self, page: PageHelper):
        """UC-05: The anonymous-submission checkbox is present on the form."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.by_id("report-anonymous")

    def test_location_fields_pre_filled(self, page: PageHelper):
        """UC-05: Latitude and longitude inputs are present and pre-filled."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        assert page.by_id("report-latitude").get_attribute("value")
        assert page.by_id("report-longitude").get_attribute("value")

    def test_not_accessible_as_guest(self, page: PageHelper):
        """UC-05: Unauthenticated access to /reports/new redirects to /login."""
        page.go("/reports/new")
        page.wait_for_url("/login")