"""Application entry point for the FastAPI backend."""

import sys
from pathlib import Path


# Ensure the top-level src directory is on the Python path so package imports resolve
PROJECT_SRC = Path(__file__).resolve().parents[1]
if str(PROJECT_SRC) not in sys.path:
    sys.path.append(str(PROJECT_SRC))


from heliosrag.api.helio_api import app  # noqa: E402


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")