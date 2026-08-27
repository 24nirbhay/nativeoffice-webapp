from playwright.sync_api import Page

def test_app_loads(page):
    response = page.goto("/")

    assert response is not None
    assert response.ok

    print(f"Title: {page.title()}")