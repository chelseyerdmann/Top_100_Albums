"""
Fetch ALL liked songs from Spotify (paginated) and save to data/liked_songs_all.json.
Run once with your auth code; then open the dashboard with: streamlit run dashboard_liked_songs.py

Usage:
  py fetch_all_liked_songs.py <auth_code>
  or set SPOTIFY_AUTH_CODE in .env (optional)
"""
import argparse
import json
import os
import requests
import base64
from pathlib import Path

# Load .env from project root
def load_env():
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"'))

load_env()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080/callback")


def get_access_token(auth_code: str) -> str:
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth_b64}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "authorization_code", "code": auth_code, "redirect_uri": REDIRECT_URI},
    )
    data = r.json()
    if "error" in data:
        raise SystemExit(f"Token error: {data}")
    return data["access_token"]


def fetch_all_liked_songs(access_token: str) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    all_items = []
    offset = 0
    limit = 50
    while True:
        r = requests.get(
            "https://api.spotify.com/v1/me/tracks",
            headers=headers,
            params={"limit": limit, "offset": offset},
        )
        if r.status_code != 200:
            raise SystemExit(f"API error {r.status_code}: {r.text[:200]}")
        data = r.json()
        items = data.get("items", [])
        if not items:
            break
        all_items.extend(items)
        total = data.get("total", 0)
        if offset + len(items) >= total:
            break
        offset += limit
        print(f"  Fetched {len(all_items)} / {total} liked songs...")
    return all_items


def main():
    parser = argparse.ArgumentParser(description="Fetch all Spotify liked songs and save to JSON")
    parser.add_argument("auth_code", nargs="?", default=os.getenv("SPOTIFY_AUTH_CODE"), help="Auth code from redirect URL")
    args = parser.parse_args()
    if not args.auth_code:
        print("Usage: py fetch_all_liked_songs.py <auth_code>")
        print("Get auth_code by running the first cell of spotify_artists_from_my_plays.ipynb and copying the code from the redirect URL.")
        raise SystemExit(1)
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SystemExit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env (copy from .env.example). Do not commit .env.")

    print("Exchanging code for token...")
    token = get_access_token(args.auth_code)
    print("Fetching all liked songs (all time)...")
    items = fetch_all_liked_songs(token)
    print(f"Total: {len(items)} liked songs.")

    root = Path(__file__).resolve().parent.parent
    out_path = root / "data" / "liked_songs_all.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(items), "items": items}, f, indent=2, ensure_ascii=False)
    print(f"Saved to {out_path}")
    print("Run the dashboard: streamlit run src/dashboard_liked_songs.py")


if __name__ == "__main__":
    main()
