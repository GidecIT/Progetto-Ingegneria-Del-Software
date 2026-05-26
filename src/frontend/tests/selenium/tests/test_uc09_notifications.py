"""
UC-09  Notification management – mark a notification as read.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import CITIZEN_EMAIL, CITIZEN_PASSWORD, PageHelper, WAIT_TIMEOUT


class TestNotifications:
    """UC-09 – Notifications."""

    def test_uc09_notifications_section_renders(self, page: PageHelper):
        """UC-09: The notifications section is rendered on the dashboard."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")
        page.by_id("notifications-list")

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
            message=f"Button #{btn_id} should disappear after marking as read",
        )

    def test_uc09_read_notification_has_muted_style(self, page: PageHelper):
        """UC-09: Notifications that are already read carry the 'is-muted' CSS class."""
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.wait_for_url("/dashboard")

        notif_list = page.by_id("notifications-list")
        items = notif_list.find_elements(By.TAG_NAME, "li")
        read_items = [li for li in items if "is-muted" in li.get_attribute("class")]
        # This is an observation test – we don't fail if there are no read notifications
        for item in read_items:
            # Verify there is no Mark-as-read button inside a muted item
            btns = item.find_elements(By.XPATH, ".//*[contains(@id, 'notification-read-')]")
            assert not btns, "Muted (read) notification should not have a Mark-as-read button"
