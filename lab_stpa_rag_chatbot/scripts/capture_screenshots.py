"""Capture Streamlit UI screenshots for delivery evidence."""
from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.env_config import load_project_env

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT.parent / "rag-avancado" / "development" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
STREAMLIT_URL = "http://localhost:8501"


def wait_for_streamlit(timeout_s: int = 90) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            urllib.request.urlopen(STREAMLIT_URL, timeout=2)
            return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(1)
    raise TimeoutError(f"Streamlit did not start within {timeout_s}s at {STREAMLIT_URL}")


def main() -> None:
    load_project_env()
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
        env={**os.environ, "PYTHONPATH": "app"},
    )
    try:
        wait_for_streamlit()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto(STREAMLIT_URL, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3000)

            chat = page.get_by_placeholder("Ex.: What is an unsafe control action?")
            chat.fill("What is an unsafe control action in STPA?")
            chat.press("Enter")
            page.get_by_text("Referências", exact=False).first.wait_for(timeout=120_000)
            page.get_by_text("Fontes recuperadas").click()
            page.wait_for_timeout(2000)
            page.screenshot(path=str(EVIDENCE / "in-scope.png"), full_page=True)

            chat = page.get_by_placeholder("Ex.: What is an unsafe control action?")
            chat.fill("What is the capital of France?")
            chat.press("Enter")
            page.get_by_text("Informação não encontrada", exact=False).wait_for(timeout=90_000)
            page.wait_for_timeout(2000)
            page.screenshot(path=str(EVIDENCE / "out-of-scope.png"), full_page=True)
            browser.close()
        print(f"Saved screenshots to {EVIDENCE}")
    finally:
        proc.terminate()
        proc.wait(timeout=10)


if __name__ == "__main__":
    main()
