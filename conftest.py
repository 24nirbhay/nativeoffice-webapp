import base64
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest
from importlib import import_module


pytest_html = import_module("pytest_html")
metadata_key = import_module("pytest_metadata.plugin").metadata_key


def _report_dir() -> Path:
    """
    Directory supplied by the CI workflow for the current test module.
    Falls back to local artifacts/report when running manually.
    """
    path = os.getenv(
        "REPORT_DIR",
        f"artifacts/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _classification(item):
    """
    Classification is controlled by pytest markers.

    Supported:
        @pytest.mark.ui
        @pytest.mark.visual
        @pytest.mark.functional
        @pytest.mark.logic

    Default:
        Functional / Logic
    """
    if item.get_closest_marker("ui") or item.get_closest_marker("visual"):
        return "UI / Visual"

    if item.get_closest_marker("functional") or item.get_closest_marker("logic"):
        return "Functional / Logic"

    return "Functional / Logic"


def _impact(item):
    """
    Impact is controlled by pytest markers.

    Supported:
        @pytest.mark.p1
        @pytest.mark.p3

    Default:
        P3
    """
    if item.get_closest_marker("p1"):
        return "Critical / P1"

    return "Medium / P3"


def pytest_configure(config):
    if hasattr(config, "stash"):
        config.stash[metadata_key]["Tester"] = "Peru"
        config.stash[metadata_key]["Application"] = "NativeOffice"
        config.stash[metadata_key]["Environment"] = "CI"
        config.stash[metadata_key]["Report Generated"] = (
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        )


def pytest_html_report_title(report):
    report.title = "NativeOffice QA Test Report"


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Area</th>")
    cells.insert(3, "<th>Impact</th>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    report.area = _classification(item)
    report.impact = _impact(item)

    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        report_dir = _report_dir()
        screenshot_dir = report_dir / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        safe_name = (
            item.nodeid
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("[", "_")
            .replace("]", "_")
        )

        screenshot_path = screenshot_dir / f"{safe_name}.png"

        page = item.funcargs.get("page")

        if page:
            try:
                screenshot_bytes = page.screenshot(full_page=True)

                screenshot_path.write_bytes(screenshot_bytes)

                encoded = base64.b64encode(screenshot_bytes).decode("utf-8")

                extras.append(
                    pytest_html.extras.image(
                        encoded,
                        mime_type="image/png",
                        extension="png",
                        name="Failure Screenshot",
                    )
                )

                extras.append(
                    pytest_html.extras.text(
                        f"Screenshot: {screenshot_path.as_posix()}",
                        name="Evidence Path",
                    )
                )

            except Exception as exc:
                extras.append(
                    pytest_html.extras.text(
                        f"Screenshot capture failed: {exc}",
                        name="Screenshot Error",
                    )
                )

    report.extras = extras


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{report.area}</td>")
    cells.insert(3, f"<td>{report.impact}</td>")


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend(
        [
            """
            <div style="
                margin: 12px 0;
                padding: 12px 16px;
                border-left: 4px solid #315fe8;
                background: #f6f8fa;
                border-radius: 6px;
            ">
                <strong>NativeOffice QA</strong><br>
                Failure screenshots are embedded directly in this report.
                Playwright traces are retained in the module's
                <code>test-results</code> directory.
            </div>
            """
        ]
    )