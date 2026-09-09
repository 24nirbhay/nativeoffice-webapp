from playwright.sync_api import Page, expect
import playwright 


def test_doc(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # ==================== OPEN DOCUMENT ====================

    page.get_by_role("button", name="doc").click()

    editor = page.locator("#editor",has_text="Start writing,or share this with someone.")

    # ==================== TEXT EDITING ====================

    editor.click()
    page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for text formatting."
    )

    expect(editor).to_contain_text("hello")

    # ==================== UNDERLINE ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for underline."
    )

    page.get_by_role("button", name="U", exact=True).click()

    # ==================== ITALIC ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for italic."
    )

    page.get_by_role(
        "button",
        name="I",
        description="Italic (Ctrl+I)"
    ).click()

    # ==================== BOLD ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for bold."
    )

    page.get_by_role(
        "button",
        name="B",
        description="Bold (Ctrl+B)"
    ).click()

    # ==================== STRIKETHROUGH ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for strikethrough."
    )

    page.get_by_role(
        "button",
        name="S",
        description="Strikethrough"
    ).click()

    # ==================== TEXT COLOUR ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for text colour."
    )
    
    page.keyboard.press("Control+A")
    page.keyboard.insert_text("#1e1627")
    page.keyboard.press("Enter")

    # ==================== ALIGNMENT ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for alignment."
    )

    page.get_by_role("button", name="Centre").click()

    # ==================== LINE SPACING ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for line spacing."
    )

    page.get_by_label("Line spacing").select_option("2")

    # ==================== LISTS ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for lists."
    )

    page.get_by_role("button", name="Checklist").click()

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for bullet list."
    )

    page.get_by_role("button", name="Bulleted list").click()

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for numbered list."
    )

    page.get_by_role("button", name="Numbered list").click()

    # ==================== INDENT ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for indentation."
    )

    page.get_by_role(
        "button",
        name="Increase indent (Tab)"
    ).click()

    # ==================== PARAGRAPH STYLE ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for paragraph styles."
    )

    page.get_by_label("Paragraph style").select_option("h1")

    # ==================== FONT ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for font selection."
    )

    page.get_by_label(
        "Font",
        exact=True
    ).select_option("Inter")

    # ==================== FONT SIZE ====================

    editor.page.keyboard.insert_text(
        "hello\n\n"
        "hello this is a test for font size."
    )

    page.get_by_label("Font size").select_option("24pt")

    # ==================== SHARE ====================

    page.get_by_role("button", name="Share").click()

    expect(page.locator("#share-scrim")).to_be_visible()

    expect(
        page.get_by_role(
            "heading",
            name="Share this document"
        )
    ).to_be_visible()

    page.get_by_role("button", name="Done").click()

    expect(
        page.locator("#share-scrim")
    ).not_to_be_visible()

    # ==================== MENUS ====================

    page.get_by_role("button", name="Edit").click()
    page.get_by_role("button", name="View").click()
    page.get_by_role(
        "button",
        name="Insert",
        exact=True
    ).click()
    page.get_by_role(
        "button",
        name="Format",
        exact=True
    ).click()
    page.get_by_role("button", name="Tools").click()
    page.get_by_role(
        "button",
        name="Help",
        exact=True
    ).click()

