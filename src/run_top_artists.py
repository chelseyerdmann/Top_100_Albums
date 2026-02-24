"""Run second cell: exchange auth code for token and fetch top artists."""
import os
import requests
import base64
from pathlib import Path

# Load from .env (repo root)
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080/callback")
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("auth_code", nargs="?", default=os.getenv("SPOTIFY_AUTH_CODE"), help="Auth code from redirect URL")
args = parser.parse_args()
auth_code = args.auth_code or ""
if not auth_code or not client_id or not client_secret:
    print("Usage: py run_top_artists.py <auth_code>")
    print("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env. Pass auth_code from redirect URL.")
    exit(1)

auth_str = f"{client_id}:{client_secret}"
auth_base64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {auth_base64}", "Content-Type": "application/x-www-form-urlencoded"},
    data={"grant_type": "authorization_code", "code": auth_code, "redirect_uri": redirect_uri},
)
tokens = response.json()
if "error" in tokens:
    print("Token error:", tokens)
    exit(1)
access_token = tokens["access_token"]

top_artists_resp = requests.get(
    "https://api.spotify.com/v1/me/top/artists",
    headers={"Authorization": f"Bearer {access_token}"},
    params={"time_range": "medium_term", "limit": 20},
)
top_artists_data = top_artists_resp.json()
top_artists = top_artists_data.get("items", [])

if not top_artists:
    print("No top artists found. Try long_term time_range or make sure you've been listening.")
else:
    print(f"Your top {len(top_artists)} artists (based on your Spotify plays):\n")

def get_artist_top_tracks(artist_id):
    r = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"market": "US"},
    )
    return r.json().get("tracks", [])

def get_artist_albums(artist_id, limit=3):
    r = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/albums",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"market": "US", "limit": limit, "include_groups": "album,single"},
    )
    return r.json().get("items", [])

for i, artist in enumerate(top_artists, 1):
    name = artist.get("name", "?")
    aid = artist.get("id")
    genres = artist.get("genres", [])
    followers = (artist.get("followers") or {}).get("total", 0)
    print(f"--- {i}. {name} ---")
    print(f"    Genres: {', '.join(genres[:5]) if genres else 'N/A'}")
    print(f"    Followers: {followers:,}")
    top_tracks = get_artist_top_tracks(aid)
    if top_tracks:
        print(f"    Top tracks: {', '.join(t.get('name', '?') for t in top_tracks[:5])}")
    albums = get_artist_albums(aid)
    if albums:
        print(f"    Recent albums: {', '.join(a.get('name', '?') for a in albums)}")
    print()
