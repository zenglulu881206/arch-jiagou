"""
浏览器验收统一启动入口：所有 E2E / 闭环脚本都从这里拿浏览器，禁止脚本各自 launch。

默认有头、本机 Chrome、窗口最大化、每步间隔 STEP_MS 毫秒；CI 等无界面环境传 headless=True。
用法：
    from e2e_launch import open_page
    with open_page("http://127.0.0.1:5173") as page:
        page.get_by_text("问候示例").click()
"""
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

STEP_MS = 800


@contextmanager
def open_page(url: str, headless: bool = False, step_ms: int = STEP_MS):
    """打开浏览器并进入 url，产出 page；退出 with 时关闭浏览器。"""
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
