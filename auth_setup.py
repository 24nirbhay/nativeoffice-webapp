import os
from pathlib import Path

from playwright.sync_api import sync_playwright

user_data_path = Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "User Data" / "Default"
auth_path = Path(__file__).resolve().parent / "auth.json"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=str(user_data_path),
        channel="chrome",
        headless=False,
    )

    pages = context.pages
    page = next(
        (candidate for candidate in pages if candidate.url != "about:blank"),
        pages[0] if pages else context.new_page(),
    )

    for candidate in pages:
        if candidate != page and not candidate.is_closed():
            candidate.close()

    page.goto("https://tools.nativeoffice.online/", wait_until="domcontentloaded")
    page.get_by_role("link", name="Sign in", exact=True).click()

    print("Complete Google login in the browser. Waiting for the NativeOffice callback...")
    page.wait_for_url(
        "https://tools.nativeoffice.online/**",
        timeout=300000,
    )
    page.wait_for_load_state("networkidle")

    # Wait for the account button — proves the session cookie is live
    page.locator("button.account-btn").wait_for(state="visible", timeout=10000)

    # Debug: confirm the session cookie exists
    cookies = context.cookies("https://tools.nativeoffice.online")
    nativeoffice_cookies = [
        cookie["name"]
        for cookie in cookies
        if "nativeoffice.online" in cookie["domain"]
    ]
    print(f"NativeOffice cookies: {nativeoffice_cookies}")

    if not nativeoffice_cookies or nativeoffice_cookies == ["no_session"]:
        raise RuntimeError(
            "Google login returned, but no authenticated NativeOffice session cookie was created."
        )

    context.storage_state(path=str(auth_path))
    print(f"auth.json saved successfully: {auth_path}")
    input("Session saved. Press Enter to close the browser...")
    context.close()   