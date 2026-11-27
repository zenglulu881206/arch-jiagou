"""Browser acceptance entry point shared by project E2E scripts."""
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

STEP_MS = 800


@contextmanager
def open_page(url: str, headless: bool = False, step_ms: int = STEP_MS):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            channel="chrome",
            headless=headless,
            slow_mo=step_ms,
            args=["--start-maximized"],
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.goto(url)
        try:
            yield page
        finally:
            browser.close()
