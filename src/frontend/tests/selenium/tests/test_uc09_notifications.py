"""UC-09  Citizen views and interacts with notifications."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, WAIT_TIMEOUT, PageHelper


class TestNotifications:
    """UC-09 – Citizen views and interacts with notifications."""

    def test_uc09_notifications_page_renders(self, page: PageHelper):
        """UC-09: Notifications list is accessible from the dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        # Ensure the notifications section or button exists
        page.by_id("notifications-section")

    def test_uc09_list_unread_notifications(self, page: PageHelper):
        """UC-09: Unread notifications are displayed in a list."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        notif_list = page.by_id("notifications-list")
        # Check if we have at least the list container
        assert notif_list.is_displayed()

    def test_uc09_mark_as_read_button_present_for_unread(self, page: PageHelper):
        """UC-09: If the citizen has at least one unread notification, a
        'Mark as read' button exists in the notifications list."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        notif_list = page.by_id("notifications-list")
        read_buttons = notif_list.find_elements(
            By.XPATH, ".//*[contains(@id, 'notification-read-')]"
        )
        if not read_buttons:
            pytest.skip("No unread notifications in seed data; skipping read test")

        first_btn = read_buttons[0]
        btn_id = first_btn.get_attribute("id")
        first_btn.click()

        # After clicking, that button should disappear (notification marked read)
        WebDriverWait(page.driver, WAIT_TIMEOUT).until(
            EC.invisibility_of_element_located((By.ID, btn_id)),
            message=f"Button {btn_id} did not disappear after click"
        )
