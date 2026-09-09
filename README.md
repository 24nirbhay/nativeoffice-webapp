# NativeOffice WebApp — QA Automation

Playwright + Pytest automation for testing the NativeOffice browser-based office suite.

The project focuses on testing real user workflows across documents, spreadsheets, presentations, navigation, sharing, and UI interactions.

## Test Coverage

| Area          | Current Coverage                                                                                                                                       |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Navigation    | Workspace navigation, appearance settings, application entry points                                                                                    |
| Documents     | Text editing, underline, italic, bold, strikethrough, text colour, alignment, line spacing, lists, indentation, paragraph styles, fonts and font sizes |
| Spreadsheets  | Cell input, table creation, borders, number formatting, fill colours, text formatting, alignment, functions and charts                                 |
| Presentations | Presentation creation, title/subtitle editing and presentation editor interaction                                                                      |
| Sharing       | Share dialog visibility and closing                                                                                                                    |
| UI            | Exploratory visual and usability testing                                                                                                               |

## Tech Stack

* Python
* Pytest
* Playwright
* pytest-playwright
* pytest-html
* Chrome

## Project Structure

```text
nativeoffice-webapp/
│
├── tests/
│   ├── test_nav.py
│   ├── test_document.py
│   ├── test_spreadsheet.py
│   └── test_ppt.py
│
├── testdata/
│
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## Test Approach

Tests are built around real user workflows rather than isolated UI clicks.

The current approach includes:

* Functional testing
* Regression testing
* UI interaction testing
* Exploratory visual testing
* Bug identification and reproduction
* Playwright assertions
* Failure screenshots
* Playwright traces for failed tests

Boundary and edge-case scenarios are documented as explicit coverage gaps until they are executed.

## QA Traceability

Human-readable test cases live in `qa/test_cases.py`. Each automated pytest function links to one stable Test Case ID, so the same catalog describes the scenario and the reports record the real execution result.

Example:

```text
TC-SHEET-001
	-> tests/test_sheets.py::test_sheets
	-> pytest execution result
	-> PASS / FAIL / ERROR
	-> failure screenshot and trace when available
```

The catalog includes the objective, preconditions, steps, expected result, severity, priority, automation status, and evidence guidance. `Status` and `Actual Result` are derived from pytest execution for automated cases; they are never manually marked as passing. Catalog scenarios that have not been automated or executed appear as `NOT TESTED / COVERAGE GAP`.

The current catalog deliberately identifies untested negative input, invalid formulas, boundary values, persistence after refresh, duplicate or rapid actions, error handling, and mobile responsive behavior. These entries demonstrate test-design coverage without claiming that the scenarios were executed.

## Running the Tests

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

Run the complete suite:

```bash
pytest
```

Run an individual test:

```bash
pytest tests/test_doc.py
```

```bash
pytest tests/test_sheets.py
```

```bash
pytest tests/test_ppt.py
```

```bash
pytest tests/test_nav.py
```

Pytest-html output can be generated locally with the same report options used in CI:

```bash
REPORT_DIR=artifacts/local-report pytest tests/test_sheets.py --html=artifacts/local-report/report.html --self-contained-html --output=artifacts/local-report/test-results
```

The report contains the QA overview, test-case coverage, real execution status, automated test references, and a generated `qa-test-case-results.json` manifest. The GitHub Actions workflow aggregates these manifests into the public GitHub Pages dashboard.

## Failure Investigation

Failed tests retain Playwright screenshots and traces.

Failure evidence is discovered dynamically from the module's `test-results` directory and linked to the related Test Case ID in the pytest-html report and Pages dashboard. No individual screenshot or trace filename is hard-coded.

A trace can be opened with:

```bash
playwright show-trace path/to/trace.zip
```

This allows investigation of the browser state and actions surrounding the failure.

## Current Status

This project is actively being expanded from basic workflow automation into a broader QA test suite.

Current coverage gaps include:

* Negative, invalid, empty, and error-handling workflows
* Boundary values and duplicate or rapid interactions
* Persistence after refresh or reopen
* Responsive/mobile behavior
* File upload/download workflows
* Additional document, spreadsheet, and presentation scenarios
* More UI/visual regression checks

These are shown as `NOT TESTED / COVERAGE GAP` in the catalog and generated reports until they have an automated or documented execution result.
