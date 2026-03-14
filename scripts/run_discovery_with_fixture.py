"""
Run the Discovery API using the sample HTML fixture (no live fetch).
Use this when the server is running: python -m uvicorn backend.main:app --reload

From project root:
  python scripts/run_discovery_with_fixture.py
"""
import httpx
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_PATH = PROJECT_ROOT / "backend" / "fixtures" / "sample-page.html"
API_URL = "http://127.0.0.1:8000/api/discovery"


def main():
    if not FIXTURE_PATH.exists():
        print(f"Fixture not found: {FIXTURE_PATH}")
        return 1
    html = FIXTURE_PATH.read_text(encoding="utf-8")
    body = {"url": "https://example.com", "html": html}
    print("Posting to", API_URL, "...")
    try:
        r = httpx.post(API_URL, json=body, timeout=120.0)
        print("Status:", r.status_code)
        print(r.json())
        return 0 if r.is_success else 1
    except httpx.ConnectError as e:
        print("Connection failed. Is the server running?")
        print("  python -m uvicorn backend.main:app --reload")
        print("Error:", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
