import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")
