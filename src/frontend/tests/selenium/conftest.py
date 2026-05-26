"""
Shared fixtures and page-object helpers for the Participium Selenium suite.
"""
import time
import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:5173"
WAIT_TIMEOUT = 10  # seconds

CITIZEN_EMAIL = "citizen@example.com"
CITIZEN_PASSWORD = "Citizen123!"

OPERATOR_EMAIL = "operator@example.com"
OPERATOR_PASSWORD = "Operator123!"

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"


# ---------------------------------------------------------------------------
# Driver fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def driver():
    """Headless Chrome driver, one instance per test."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--log-level=3")
    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(0)  # rely on explicit waits
    yield drv
    drv.quit()


# ---------------------------------------------------------------------------
# Page-object helpers
# ---------------------------------------------------------------------------
class PageHelper:
    """Thin wrapper that keeps the driver + explicit wait in one place."""

    def __init__(self, driver: webdriver.Chrome, timeout: int = WAIT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- navigation ---------------------------------------------------------

    def go(self, path: str = "") -> None:
        self.driver.get(f"{BASE_URL}{path}")

    # --- element access -----------------------------------------------------

    def by_id(self, element_id: str):
        return self.wait.until(
            EC.presence_of_element_located((By.ID, element_id)),
            message=f"Element #{element_id} not found",
        )

    def by_id_visible(self, element_id: str):
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, element_id)),
            message=f"Element #{element_id} not visible",
        )

    def by_id_clickable(self, element_id: str):
        return self.wait.until(
            EC.element_to_be_clickable((By.ID, element_id)),
            message=f"Element #{element_id} not clickable",
        )

    def present(self, element_id: str) -> bool:
        """Return True if the element is present in the DOM (not necessarily visible)."""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return True
        except Exception:
            return False

    def absent(self, element_id: str) -> bool:
        """Return True if the element is NOT in the DOM."""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return False
        except Exception:
            return True

    # --- common flows -------------------------------------------------------

    def login(self, email: str, password: str) -> None:
        self.go("/login")
        self.by_id_visible("login-identifier").clear()
        self.by_id_visible("login-identifier").send_keys(email)
        self.by_id_visible("login-password").clear()
        self.by_id_visible("login-password").send_keys(password)
        self.by_id_clickable("login-submit").click()
        # wait for navigation away from /login
        self.wait.until(lambda d: "/login" not in d.current_url or self.present("dashboard-page") or self.present("operator-page") or self.present("admin-page"))

    def logout(self) -> None:
        self.by_id_clickable("logout-button").click()
        self.by_id("nav-login")  # confirms we're back on a public page

    def wait_for_url(self, fragment: str) -> None:
        self.wait.until(lambda d: fragment in d.current_url, message=f"URL did not contain '{fragment}'")

    def wait_for_id(self, element_id: str):
        return self.by_id(element_id)

    def fill(self, element_id: str, value: str) -> None:
        el = self.by_id_visible(element_id)
        el.clear()
        el.send_keys(value)

    def select_by_value(self, element_id: str, value: str) -> None:
        from selenium.webdriver.support.ui import Select
        el = self.by_id(element_id)
        Select(el).select_by_value(value)

    def click(self, element_id: str) -> None:
        self.by_id_clickable(element_id).click()


@pytest.fixture
def page(driver) -> PageHelper:
    return PageHelper(driver)


# ---------------------------------------------------------------------------
# Unique data helpers
# ---------------------------------------------------------------------------
def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]
