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

Boundary and edge-case testing will be added as the test suite expands.

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
pytest tests/test_document.py
```

```bash
pytest tests/test_spreadsheet.py
```

```bash
pytest tests/test_ppt.py
```

```bash
pytest tests/test_nav.py
```

## Failure Investigation

Failed tests retain Playwright screenshots and traces.

A trace can be opened with:

```bash
playwright show-trace path/to/trace.zip
```

This allows investigation of the browser state and actions surrounding the failure.

## Current Status

This project is actively being expanded from basic workflow automation into a broader QA test suite.

Planned additions include:

* Boundary and edge-case testing
* Additional document workflows
* Additional spreadsheet workflows
* Additional presentation workflows
* File upload/download testing
* More UI/visual regression checks
* Structured bug reporting
* HTML test reporting
