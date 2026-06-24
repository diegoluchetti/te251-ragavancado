from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

LAB_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = LAB_ROOT.parent


def load_project_env() -> None:
    load_dotenv(LAB_ROOT / ".env")
    load_dotenv(REPO_ROOT / ".env", override=True)
    if not os.getenv("OPENAI_API_KEY") and os.getenv("OPEN_AI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_API_KEY"]
    if not os.getenv("OPENROUTER_API_KEY") and os.getenv("OPEN_ROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = os.environ["OPEN_ROUTER_API_KEY"]
