from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

from dotenv import load_dotenv

REQUIRED_PATHS = [Path("data/raw/STPA_Handbook.pdf"), Path("requirements.txt"), Path(".env")]


def check_import(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def main() -> None:
    load_dotenv()
    print("Python:", sys.version)
    print("Platform:", platform.platform())
    print("Working directory:", Path.cwd())
    print("\nFiles:")
    for path in REQUIRED_PATHS:
        print(f"  {'OK ' if path.exists() else 'MISS'} {path}")
    print("\nPackages:")
    for pkg in ["openai", "chromadb", "streamlit", "dotenv", "pypdf", "tiktoken"]:
        print(f"  {'OK ' if check_import(pkg) else 'MISS'} {pkg}")
    print("\nEnvironment:")
    print("  OPENAI_API_KEY:", "OK" if os.getenv("OPENAI_API_KEY") else "MISSING")
    print("  OPENAI_CHAT_MODEL:", os.getenv("OPENAI_CHAT_MODEL", "not set"))
    print("  OPENAI_EMBED_MODEL:", os.getenv("OPENAI_EMBED_MODEL", "not set"))
    if not Path("data/raw/STPA_Handbook.pdf").exists():
        raise SystemExit("Copy STPA_Handbook.pdf to data/raw before continuing.")


if __name__ == "__main__":
    main()
