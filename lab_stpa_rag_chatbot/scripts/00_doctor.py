from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.env_config import LAB_ROOT, REPO_ROOT, load_project_env

REQUIRED_PATHS = [Path("data/raw/STPA_Handbook.pdf"), Path("requirements.txt")]


def check_import(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def main() -> None:
    load_project_env()
    print("Python:", sys.version)
    print("Platform:", platform.platform())
    print("Working directory:", Path.cwd())
    print("\nFiles:")
    for path in REQUIRED_PATHS:
        print(f"  {'OK ' if path.exists() else 'MISS'} {path}")
    print("\nPackages:")
    for pkg in ["openai", "chromadb", "streamlit", "dotenv", "pypdf", "tiktoken"]:
        print(f"  {'OK ' if check_import(pkg) else 'MISS'} {pkg}")
    print(f"  repo .env: {'OK' if (REPO_ROOT / '.env').exists() else 'MISS'} {REPO_ROOT / '.env'}")
    print(f"  lab .env:  {'OK' if (LAB_ROOT / '.env').exists() else 'MISS'} {LAB_ROOT / '.env'}")
    print("\nEnvironment:")
    print("  OPENAI_API_KEY:", "OK" if os.getenv("OPENAI_API_KEY") else "MISSING")
    print("  OPENROUTER_API_KEY:", "OK" if os.getenv("OPENROUTER_API_KEY") else "MISSING")
    print("  OPENAI_CHAT_MODEL:", os.getenv("OPENAI_CHAT_MODEL", "not set"))
    print("  OPENAI_EMBED_MODEL:", os.getenv("OPENAI_EMBED_MODEL", "not set"))
    if not Path("data/raw/STPA_Handbook.pdf").exists():
        raise SystemExit("Copy STPA_Handbook.pdf to data/raw before continuing.")


if __name__ == "__main__":
    main()
