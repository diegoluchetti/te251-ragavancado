"""Capture Streamlit UI screenshots for delivery evidence."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT.parent / "rag-avancado" / "development" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


def main() -> None:
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/streamlit_app.py",
            "--server.headless",
            "true",
            "--server.port",
            "8501",
        ],
        cwd=ROOT,
        env={**dict(**__import__("os").environ), "PYTHONPATH": "app"},
    )
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:8501", wait_until="networkidle", timeout=120_000)
            page.wait_for_timeout(3000)

            chat = page.get_by_placeholder("Ex.: What is an unsafe control action?")
            chat.fill("What is an unsafe control action in STPA?")
            chat.press("Enter")
            page.wait_for_timeout(60_000)
            page.get_by_text("Fontes recuperadas").click()
            page.wait_for_timeout(2000)
            page.screenshot(path=str(EVIDENCE / "in-scope.png"), full_page=True)

            chat = page.get_by_placeholder("Ex.: What is an unsafe control action?")
            chat.fill("What is the capital of France?")
            chat.press("Enter")
            page.wait_for_timeout(45_000)
            page.screenshot(path=str(EVIDENCE / "out-of-scope.png"), full_page=True)
            browser.close()
        print(f"Saved screenshots to {EVIDENCE}")
    finally:
        proc.terminate()
        proc.wait(timeout=10)


if __name__ == "__main__":
    main()
