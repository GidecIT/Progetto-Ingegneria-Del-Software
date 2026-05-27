"""
Shared fixtures and helpers for the Participium Selenium suite.
"""
import os
import tempfile
import time
import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:5173"
WAIT_TIMEOUT = 15  # seconds

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
    drv.implicitly_wait(0)
    yield drv
    drv.quit()


# ---------------------------------------------------------------------------
# PageHelper
# ---------------------------------------------------------------------------
class PageHelper:
    """Thin wrapper that keeps the driver and WebDriverWait together."""

    def __init__(self, driver: webdriver.Chrome, timeout: int = WAIT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go(self, path: str = "") -> None:
        self.driver.get(f"{BASE_URL}{path}")

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
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return True
        except Exception:
            return False

    def absent(self, element_id: str) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return False
        except Exception:
            return True

    def fill(self, element_id: str, value: str) -> None:
        el = self.by_id_visible(element_id)
        el.clear()
        el.send_keys(value)

    def click(self, element_id: str) -> None:
        self.by_id_clickable(element_id).click()

    def select_by_value(self, element_id: str, value: str) -> None:
        from selenium.webdriver.support.ui import Select
        Select(self.by_id(element_id)).select_by_value(value)

    def wait_for_url(self, fragment: str) -> None:
        self.wait.until(
            lambda d: fragment in d.current_url,
            message=f"URL did not contain '{fragment}'",
        )

    def wait_redirect_away_from(self, path: str) -> None:
        """Wait until the URL no longer contains *path*."""
        self.wait.until(
            lambda d: path not in d.current_url,
            message=f"Expected redirect away from {path}",
        )

    def login(self, email: str, password: str, retries: int = 3) -> None:
        """Log in and wait for the logout button to confirm session is ready.
        Retries up to *retries* times with a short pause between attempts to
        handle backend rate-limiting on consecutive logins."""
        for attempt in range(retries):
            self.go("/login")
            ident = self.by_id_visible("login-identifier")
            ident.clear()
            ident.send_keys(email)
            pwd = self.by_id_visible("login-password")
            pwd.clear()
            pwd.send_keys(password)
            self.by_id_clickable("login-submit").click()
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.ID, "logout-button")),
                    message=f"Login failed for {email}",
                )
                return  # success
            except Exception:
                if attempt < retries - 1:
                    time.sleep(2)  # brief pause before retry
                else:
                    raise

    def logout(self) -> None:
        self.by_id_clickable("logout-button").click()
        self.by_id("nav-login")


@pytest.fixture
def page(driver) -> PageHelper:
    return PageHelper(driver)


# ---------------------------------------------------------------------------
# Shared data helpers
# ---------------------------------------------------------------------------

def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]


def wait_for_report_rows(page: PageHelper) -> None:
    """Wait until at least one public-report-row-* element appears in the DOM."""
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[starts-with(@id,'public-report-row-')]")
        ),
        message="No public-report-row-* found; check seed data and backend",
    )


def get_first_public_report_id(page: PageHelper) -> int:
    """Navigate to home, wait for report rows, return the first report's ID."""
    page.go("/")
    wait_for_report_rows(page)
    tbody = page.by_id("public-report-table-body")
    first_row = tbody.find_elements("tag name", "tr")[0]
    open_link = first_row.find_element("tag name", "a")
    href = open_link.get_attribute("href")
    return int(href.rstrip("/").split("/")[-1])


def write_temp_image() -> str:
    """Write a minimal valid 1×1 PNG to a temp file and return its path."""
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


def create_report_and_get_id(page: PageHelper) -> int:
    """Log in as citizen, submit a new report, return its numeric ID."""
    img = write_temp_image()
    try:
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.fill("report-title", f"Test report {unique_suffix()}")
        page.fill("report-description", "Created by Selenium test suite.")
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait.until(
            lambda d: "/reports/" in d.current_url and "/new" not in d.current_url,
            message="New report did not redirect to detail page",
        )
        return int(page.driver.current_url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)