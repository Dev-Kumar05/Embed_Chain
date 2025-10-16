"""Centralized path definitions for the heliosrag package."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
RESOURCES_DIR = PACKAGE_ROOT / "resources"
DATA_DIR = RESOURCES_DIR / "data"
STATIC_DIR = RESOURCES_DIR / "static"
RAW_DOCS_DIR = DATA_DIR / "raw"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
USER_VECTORSTORES_DIR = DATA_DIR / "user_vectorstores"
UPLOADS_DIR = DATA_DIR / "uploads"
DEFAULT_ENV_FILE = PACKAGE_ROOT / ".env"

__all__ = [
    "PACKAGE_ROOT",
    "RESOURCES_DIR",
    "DATA_DIR",
    "STATIC_DIR",
    "RAW_DOCS_DIR",
    "VECTORSTORE_DIR",
    "USER_VECTORSTORES_DIR",
    "UPLOADS_DIR",
    "DEFAULT_ENV_FILE",
]
