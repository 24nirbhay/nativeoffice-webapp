from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://tools.nativeoffice.online")

    input("Log in with Google, then press Enter here...")

    context.storage_state(path="auth.json")

    browser.close()