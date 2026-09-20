from playwright.sync_api import sync_playwright

SESSION_COOKIE = ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    context.add_cookies([
        {
            "name": "no_session",
            "value": SESSION_COOKIE,
            "domain": "tools.nativeoffice.online",
            "path": "/",
            "secure": True,
        }
    ])

    page = context.new_page()
    page.goto("https://tools.nativeoffice.online")

    input("Confirm NativeOffice is logged in, then press Enter...")

    context.storage_state(path="auth.json")
    browser.close()