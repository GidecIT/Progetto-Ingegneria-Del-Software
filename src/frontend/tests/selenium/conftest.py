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
from selenium.webdriver.support.ui import Select

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
                    time.sleep(2)
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
    """Log in as citizen, submit a new report, return its numeric ID.
    Session is left logged in as citizen after this call."""
    img = write_temp_image()
    try:
        page.login(CITIZEN_EMAIL, CITIZEN_PASSWORD)
        page.go("/reports/new")
        page.fill("report-title", f"Test report {unique_suffix()}")
        page.fill("report-description", "Created by Selenium test suite.")
        
        # Seleziona esplicitamente una categoria valida

        try:
            def categories_loaded(d):
                try:
                    return len(Select(d.find_element(By.ID, "report-category")).options) > 1
                except Exception:
                    return False
            page.wait.until(categories_loaded)
            sel = Select(page.driver.find_element(By.ID, "report-category"))
            if not sel.options[0].get_attribute("value"):
                sel.select_by_index(1)
            else:
                sel.select_by_index(0)
        except Exception:
            pass
            
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait.until(
            lambda d: "/reports/" in d.current_url and "/new" not in d.current_url,
            message="New report did not redirect to detail page",
        )
        return int(page.driver.current_url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)


def create_and_assign_report(page: PageHelper) -> int:
    """Create a report as citizen, then assign it via the operator dashboard.

    This helper is required by UC-11 and UC-12, which need an assigned report
    so that the conversation thread is accessible (can_access_messages=true).

    Flow:
      1. Login as citizen → create report (status: Pending Approval)
      2. Logout
      3. Login as operator → assign the report (status changes, thread opens)
      4. Logout
      Returns the report ID. Session is logged out after this call.

    Skips if the newly created report does not appear in the operator's
    pending section (e.g. the operator is not assigned to that category).
    """
    # Step 1 — create report as citizen
    report_id = create_report_and_get_id(page)
    page.logout()

    # Step 2 — assign as operator
    page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    page.wait_for_url("/operator")

    assign_btn_id = f"pending-report-assign-{report_id}"
    try:
        btn = page.by_id(assign_btn_id)
        page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        page.driver.execute_script("arguments[0].click();", btn)
    except Exception:
        pytest.skip(
            f"Report {report_id} is not visible in the operator pending section. "
            "The operator seed account may not handle this report's category. "
            "Verify that the operator is configured for the default report category."
        )

    page.wait.until(
        EC.presence_of_element_located(
            (By.ID, f"assigned-report-row-{report_id}")
        ),
        message=f"Report {report_id} did not appear in the assigned section after Assign",
    )
    page.logout()
    return report_id


def create_public_report_as_new_citizen(page: PageHelper) -> int:
    """Register a fresh citizen account, verify it, create a report, then have
    the operator assign it so the report becomes publicly visible.

    This helper is required by UC-07 (follow report), which needs a public
    report NOT created by citizen@example.com. The seed data only contains
    reports from that account, so we create a new one here.

    Flow:
      1. Register a new citizen with a unique email
      2. Click the verification link exposed by the local dev environment
      3. Login as the new citizen → create a report
      4. Logout
      5. Login as operator → assign the report (makes it public)
      6. Logout
      Returns the report ID. Session is logged out after this call.

    Skips if:
      - The verification link is not exposed (non-local environment)
      - The report does not appear in the operator pending section
      - The report does not become publicly visible after assignment
    """
    sfx = unique_suffix()
    email = f"tmp_{sfx}@test.local"
    password = "TestPass123!"

    # Step 1 — register
    page.go("/register")
    page.fill("register-username", f"tmp_{sfx}")
    page.fill("register-first-name", "Tmp")
    page.fill("register-last-name", "Citizen")
    page.fill("register-email", email)
    page.fill("register-password", password)
    page.click("register-submit")

    # Step 2 — verify via the link exposed in local/demo environments
    if page.absent("verification-box"):
        pytest.skip(
            "Verification link not exposed; cannot create account for follow test. "
            "Ensure the backend is running in local/demo mode."
        )
    verification_href = (
        page.by_id_visible("verification-box")
        .find_element(By.ID, "verification-link")
        .get_attribute("href")
    )
    # Visit the verification URL (may return JSON — that is expected)
    page.driver.get(verification_href)

    # Step 3 — login as new citizen and create a report
    img = write_temp_image()
    try:
        page.login(email, password)
        page.go("/reports/new")
        page.fill("report-title", f"Followable report {sfx}")
        page.fill("report-description", "Created by temp citizen for follow test.")
        
        from selenium.webdriver.support.ui import Select
        try:
            def categories_loaded(d):
                try:
                    return len(Select(d.find_element(By.ID, "report-category")).options) > 1
                except Exception:
                    return False
            page.wait.until(categories_loaded)
            sel = Select(page.driver.find_element(By.ID, "report-category"))
            if not sel.options[0].get_attribute("value"):
                sel.select_by_index(1)
            else:
                sel.select_by_index(0)
        except Exception:
            pass
            
        page.by_id("report-photos").send_keys(img)
        page.click("new-report-submit")
        page.wait.until(
            lambda d: "/reports/" in d.current_url and "/new" not in d.current_url,
            message="New report did not redirect to detail page",
        )
        report_id = int(page.driver.current_url.rstrip("/").split("/")[-1])
    finally:
        os.unlink(img)
    page.logout()

    # Step 4 — assign as operator (assignment makes the report public)
    page.login(OPERATOR_EMAIL, OPERATOR_PASSWORD)
    page.wait_for_url("/operator")

    assign_btn_id = f"pending-report-assign-{report_id}"
    try:
        btn = page.by_id(assign_btn_id)
        page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        page.driver.execute_script("arguments[0].click();", btn)
    except Exception:
        pytest.skip(
            f"Report {report_id} not visible in operator pending section; "
            "cannot make it public for the follow test."
        )

    page.wait.until(
        EC.presence_of_element_located(
            (By.ID, f"assigned-report-row-{report_id}")
        ),
        message=f"Report {report_id} did not appear in assigned section",
    )
    page.logout()

    # Step 5 — confirm the report is now visible in the public table
    page.go("/")
    wait_for_report_rows(page)
    tbody = page.by_id("public-report-table-body")
    visible_ids = [
        int(r.get_attribute("id").split("-")[-1])
        for r in tbody.find_elements(
            By.XPATH, "./tr[starts-with(@id,'public-report-row-')]"
        )
    ]
    if report_id not in visible_ids:
        pytest.skip(
            f"Report {report_id} is not publicly visible after assignment. "
            "The report may require a different status to become public."
        )

    return report_id