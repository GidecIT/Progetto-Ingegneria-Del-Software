"""
Shared fixtures and helpers for the Participium Selenium suite.

Helpers kept here are used by more than one test file:
  - driver / page fixtures
  - PageHelper wrapper
  - seeded credentials
  - unique_suffix()
  - wait_for_report_rows()
  - get_first_public_report_id()
  - write_temp_image()
  - create_report_and_get_id()
"""
import os
import tempfile
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
    drv.implicitly_wait(0)  # rely on explicit waits only
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

    # --- navigation ---------------------------------------------------------

    def go(self, path: str = "") -> None:
        self.driver.get(f"{BASE_URL}{path}")

    # --- element locators ---------------------------------------------------

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

    # --- interactions -------------------------------------------------------

    def fill(self, element_id: str, value: str) -> None:
        el = self.by_id_visible(element_id)
        el.clear()
        el.send_keys(value)

    def click(self, element_id: str) -> None:
        self.by_id_clickable(element_id).click()

    def select_by_value(self, element_id: str, value: str) -> None:
        from selenium.webdriver.support.ui import Select
        Select(self.by_id(element_id)).select_by_value(value)

    # --- navigation helpers -------------------------------------------------

    def wait_for_url(self, fragment: str) -> None:
        self.wait.until(
            lambda d: fragment in d.current_url,
            message=f"URL did not contain '{fragment}'",
        )

    # --- auth shortcuts -----------------------------------------------------

    def login(self, email: str, password: str) -> None:
        self.go("/login")
        self.by_id_visible("login-identifier").clear()
        self.by_id_visible("login-identifier").send_keys(email)
        self.by_id_visible("login-password").clear()
        self.by_id_visible("login-password").send_keys(password)
        self.by_id_clickable("login-submit").click()
        self.wait.until(
            lambda d: "/login" not in d.current_url,
            message="Login did not redirect away from /login",
        )

    def logout(self) -> None:
        self.by_id_clickable("logout-button").click()
        self.by_id("nav-login")


@pytest.fixture
def page(driver) -> PageHelper:
    return PageHelper(driver)


# ---------------------------------------------------------------------------
# Shared data helpers  (used by multiple test files)
# ---------------------------------------------------------------------------

def unique_suffix() -> str:
    """Return a short random hex string to make test data unique across runs."""
    return uuid.uuid4().hex[:8]


def wait_for_report_rows(page: PageHelper) -> None:
    """Wait until at least one public-report-row-* element appears in the DOM.
    The home page loads reports asynchronously, so this explicit wait must be
    called before reading the table body."""
    page.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[starts-with(@id,'public-report-row-')]")
        ),
        message="No public-report-row-* found; check seed data and backend",
    )


def get_first_public_report_id(page: PageHelper) -> int:
    """Navigate to the home page, wait for report rows, and return the numeric
    ID of the first listed public report."""
    page.go("/")
    wait_for_report_rows(page)
    tbody = page.by_id("public-report-table-body")
    first_row = tbody.find_elements("tag name", "tr")[0]
    open_link = first_row.find_element("tag name", "a")
    href = open_link.get_attribute("href")
    return int(href.rstrip("/").split("/")[-1])


def write_temp_image() -> str:
    """Write a minimal valid 1×1 PNG to a temp file and return its path.
    The caller is responsible for deleting the file after use."""
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
    """Log in as citizen, submit a new report, and return its numeric ID.
    Used by tests that need an existing report to work with (e.g. messaging)."""
    img = write_temp_image()
    try:
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.fill("report-title", f"Test report {unique_suffix()}")
        page.fill("report-description", "Created by Selenium test suite.")
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait_for_url("/reports/")
        return int(page.driver.current_url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)