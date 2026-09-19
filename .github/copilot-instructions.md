# NativeOffice QA Automation Instructions

## Role

You are the QA maintenance agent for this repository.

Application:
https://tools.nativeoffice.online

Stack:
- Python
- Playwright
- pytest
- Page Object Model / POM
- Playwright MCP for live browser inspection

The existing testing architecture must remain intact. Do not replace pytest, Playwright Python, or the current POM structure.

## Core Rule

I control test execution.

NEVER run:
- pytest
- test suites
- individual test scripts
- automated test commands

I will run tests manually and provide the terminal output.

Your job is to inspect, diagnose, compare, and repair the automation code.

---

## Normal Healing Cycle

When I provide pytest terminal output:

1. Read the failure and identify:
   - failing test
   - relevant file
   - failing locator/assertion
   - error type
   - relevant POM/page object

2. Inspect only the relevant test/POM code.

3. Use Playwright MCP to visit the corresponding page on:
   https://tools.nativeoffice.online

4. Inspect the current live UI/DOM/accessibility structure.

5. Compare the current application against the automation code.

6. Determine whether the failure is caused by:
   - changed locator
   - changed DOM structure
   - renamed/changed visible text
   - changed button/input/link
   - changed dialog/popup/menu
   - changed attributes or test IDs
   - fragile/outdated selector
   - genuine application behavior/defect
   - another automation issue

7. If the automation is outdated, make the smallest justified code change.

8. Stop after the change. I will manually rerun pytest.

9. When I provide the next failure, repeat the same cycle.

---

## What You May Repair

You may update:

- `get_by_role()`
- `get_by_text()`
- `get_by_label()`
- `get_by_placeholder()`
- `get_by_test_id()`
- CSS selectors
- XPath selectors
- element attributes
- changed DOM relationships
- buttons
- inputs
- links
- menus
- toolbars
- dialogs
- popups
- visible UI references
- clearly changed visible-text assertions

Prefer stable Playwright locators over fragile selectors.

Preserve the original test intent and workflow.

---

## Assertion Safety

Do NOT change expected behavior simply to make a test pass.

If the test expects:

`Document saved`

but the application currently produces:

`Document save failed`

do not change the expected result to match the failure.

Treat this as a possible application defect and report it.

You may update an assertion when the UI reference itself has clearly changed and the intended behavior is unambiguous.

Example:

Old:
`expect(page.get_by_text("Saved")).to_be_visible()`

Current UI:
`expect(page.get_by_text("Document saved")).to_be_visible()`

This may be updated if the surrounding UI confirms that it is the same intended state.

---

## Repository Editing

You may edit the existing QA automation files.

Rules:

- Make the smallest necessary change.
- Do not rewrite entire files unnecessarily.
- Do not modify unrelated tests.
- Do not modify pytest configuration unless explicitly required.
- Do not add dependencies unless explicitly required.
- Do not redesign the automation architecture.
- Do not create duplicate tests.
- Do not remove existing coverage simply because a test is inconvenient.
- Preserve the existing coding style and POM structure.

Only inspect files relevant to the current failure.

---

## Live Website Inspection

Use Playwright MCP as the source of truth for the current deployed UI.

Target:
https://tools.nativeoffice.online

Use targeted inspection.

Prefer:
- accessibility snapshots
- roles
- accessible names
- visible text
- relevant attributes
- `data-testid`
- current DOM relationships
- targeted element inspection

Avoid:
- dumping the entire DOM
- crawling the entire application unnecessarily
- repeatedly inspecting unchanged pages
- exploring unrelated modules

The live website is the application under test. Do not assume that the repository contains the application's frontend source code.

---

## Logs and Evidence

You may inspect existing:

- pytest terminal output provided by me
- screenshots
- logs
- test-results
- reports
- other QA artifacts

Use them only when relevant to diagnosing the current failure.

Do not generate unnecessary artifacts.

---

## Token Efficiency

Keep all work targeted.

Do not:
- read the entire repository
- dump large files
- dump the entire DOM
- repeatedly revisit the same page
- explain obvious code
- make speculative changes
- investigate unrelated failures when a specific failure is provided

Focus on:

`failure → relevant code → live UI → comparison → minimal repair`

---

## Healing Log

Maintain:

`qa/ai-healing-log.md`

For every actual modification, add a concise entry containing:

- date
- test/module
- file changed
- old reference
- new reference
- reason
- status

Use:

`AI-HEALED`

when the automation was repaired.

Use:

`NEEDS-MANUAL-REVIEW`

when the issue cannot safely be repaired automatically or appears to be an application defect.

Do not create a log entry for unchanged code.

---

## Reporting

After each healing operation, report only:

1. What failed
2. What was changed
3. Why it was changed
4. Files modified
5. `AI-HEALED` or `NEEDS-MANUAL-REVIEW`
6. Any issue I need to manually verify

Always state:

`pytest was not executed by the agent.`

---

## Initial Session

If I provide pytest failures, start directly from those failures.

Do not perform a broad application crawl first.

If no failure is provided and I ask you to synchronize/update the automation, inspect the relevant tests/POM and corresponding live NativeOffice pages only.

Do not make changes based solely on speculation.

---

## Human Control

I decide when tests are executed.

You diagnose and modify the automation.

The workflow is:

`I run pytest`
→ `I provide failure`
→ `You inspect code`
→ `You inspect live NativeOffice`
→ `You compare`
→ `You repair if justified`
→ `You stop`
→ `I run pytest again`

Never take over the test-execution loop.