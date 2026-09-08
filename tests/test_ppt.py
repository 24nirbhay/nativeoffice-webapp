import re 
from playwright.sync_api import Playwright, Page, sync_playwright, expect


def test_ppt(page: Page) -> None:

    page.goto("https://tools.nativeoffice.online/")
    page.get_by_role("button", name="Create new").click()
    page.get_by_role("button", name="Presentation A widescreen").click()
    page.get_by_text("Click to add title").click()
    page.get_by_text("Click to add title").dblclick()
    page.locator(".sl-editor").fill("hello")
    page.get_by_text("Click to add subtitle").click()
    page.get_by_text("Click to add subtitle").dblclick()
    page.locator(".sl-editor").fill("hello")
    page.get_by_role("button", name="New slide", exact=True).click()
    page.get_by_role("button", name="New slide", exact=True).click()
    page.get_by_role("button", name="New slide", exact=True).click()
    page.get_by_role("button", name="New slide", exact=True).click()
    page.locator("div:nth-child(2) > .film-thumb").click(button="right")
    page.get_by_role("menuitem", name="Delete").click()

#img insert
    page.get_by_role("button", name="Image").click()

    expect(
        page.get_by_role("heading", name="Insert image")
    ).to_be_visible()

    image_url = page.get_by_role(
        "textbox",
        name="Image address",
        exact=True
    )

    image_url.fill("https://pin.it/1E7iVTD3P")

    page.locator(".dialog-actions .btn-primary").click()

    page.locator('a.brand[href="/"]').click()
    expect(page).to_have_url(
        "https://tools.nativeoffice.online/"
    )
