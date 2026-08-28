from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://tools.nativeoffice.online/")

    # ==================== OPEN DOCUMENT ====================

    page.get_by_role("button", name="Document Write, edit, and").click()

    editor = page.locator("#editor").get_by_role("textbox")

    expect(editor).to_be_visible()
    expect(editor).to_be_editable()

    # ==================== TEXT EDITING ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for text formatting."
    )

    expect(editor).to_contain_text("hello")

    # ==================== UNDERLINE ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for underline."
    )

    page.get_by_role("button", name="U", exact=True).click()

    # ==================== ITALIC ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for italic."
    )

    page.get_by_role(
        "button",
        name="I",
        description="Italic (Ctrl+I)"
    ).click()

    # ==================== BOLD ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for bold."
    )

    page.get_by_role(
        "button",
        name="B",
        description="Bold (Ctrl+B)"
    ).click()

    # ==================== STRIKETHROUGH ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for strikethrough."
    )

    page.get_by_role(
        "button",
        name="S",
        description="Strikethrough"
    ).click()

    # ==================== TEXT COLOUR ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for text colour."
    )

    page.get_by_role(
        "textbox",
        name="A",
        exact=True
    ).fill("#1e1627")

    # ==================== ALIGNMENT ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for alignment."
    )

    page.get_by_role("button", name="Centre").click()

    # ==================== LINE SPACING ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for line spacing."
    )

    page.get_by_label("Line spacing").select_option("2")

    # ==================== LISTS ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for lists."
    )

    page.get_by_role("button", name="Checklist").click()

    editor.fill(
        "hello\n\n"
        "hello this is a test for bullet list."
    )

    page.get_by_role("button", name="Bulleted list").click()

    editor.fill(
        "hello\n\n"
        "hello this is a test for numbered list."
    )

    page.get_by_role("button", name="Numbered list").click()

    # ==================== INDENT ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for indentation."
    )

    page.get_by_role(
        "button",
        name="Increase indent (Tab)"
    ).click()

    # ==================== PARAGRAPH STYLE ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for paragraph styles."
    )

    page.get_by_label("Paragraph style").select_option("h1")

    # ==================== FONT ====================

    editor.fill(
        "hello\n\n"
        "hello this is a test for font selection."
    )

    page.get_by_label(
        "Font",
        exact=True
    ).select_option("Inter")

    # ==================== FONT SIZE ====================

    editor.fill(
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

    # ==================== RETURN HOME ========================

    page.get_by_role(
        "link",
        name="NativeOffice"
    ).click()