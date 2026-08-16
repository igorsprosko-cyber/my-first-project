#!/usr/bin/env python3
"""Static audit for the InSales theme repository.

This intentionally checks source/configuration only. It does not claim runtime
or browser coverage.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
SETUP = ROOT / "config" / "setup.json"


def main() -> int:
    if not TEMPLATES.is_dir():
        raise SystemExit("templates directory is missing")
    if not SETUP.is_file():
        raise SystemExit("config/setup.json is missing")

    liquid_files = sorted(TEMPLATES.rglob("*.liquid"))
    if not liquid_files:
        raise SystemExit("no Liquid templates found")

    total_styles = 0
    total_scripts = 0
    issues: list[str] = []

    for path in liquid_files:
        text = path.read_text(encoding="utf-8")
        styles = len(re.findall(r"<style\b", text, flags=re.I))
        style_ends = len(re.findall(r"</style\s*>", text, flags=re.I))
        scripts = len(re.findall(r"<script\b", text, flags=re.I))
        script_ends = len(re.findall(r"</script\s*>", text, flags=re.I))
        total_styles += styles
        total_scripts += scripts
        if styles != style_ends:
            issues.append(f"{path}: inline <style> blocks are not balanced ({styles} open/{style_ends} close)")
        if scripts != script_ends:
            issues.append(f"{path}: inline <script> blocks are not balanced ({scripts} open/{script_ends} close)")
        if styles or scripts:
            print(f"{path}: inline_css={styles} inline_js={scripts}")

    with SETUP.open(encoding="utf-8") as fh:
        setup = json.load(fh)

    widget_lists = setup.get("theme_widgets", {}).get("widget_lists")
    if not isinstance(widget_lists, list):
        issues.append("config/setup.json: theme_widgets.widget_lists is missing or not a list")
        widget_lists = []

    handles = [item.get("handle") for item in widget_lists if isinstance(item, dict)]
    if any(not handle for handle in handles):
        issues.append("config/setup.json: every widget list must have a handle")
    if len(handles) != len(set(handles)):
        issues.append("config/setup.json: duplicate widget-list handles found")

    widget_count = 0
    empty_list_count = 0
    for item in widget_lists:
        if not isinstance(item, dict):
            issues.append("config/setup.json: widget list entry is not an object")
            continue
        widgets = item.get("widgets", [])
        if not isinstance(widgets, list):
            issues.append(f"config/setup.json: widgets for {item.get('handle')} are not a list")
            continue
        if not widgets:
            empty_list_count += 1
        for widget in widgets:
            widget_count += 1
            if not isinstance(widget, dict) or not widget.get("widget_type"):
                issues.append(f"config/setup.json: widget list {item.get('handle')} contains an entry without widget_type")

    print(f"Liquid templates scanned: {len(liquid_files)}")
    print(f"Inline CSS blocks: {total_styles}")
    print(f"Inline JS blocks: {total_scripts}")
    print(f"Widget lists: {len(widget_lists)}")
    print(f"Widgets: {widget_count}")
    print(f"Empty widget lists: {empty_list_count}")

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1

    print("Static audit passed: Liquid inline CSS/JS and setup.json widget inventory are structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
