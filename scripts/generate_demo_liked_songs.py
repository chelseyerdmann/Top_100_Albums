"""
Generate data/liked_songs_demo.json from data/albums.json for the Streamlit demo.
Run from repo root: python scripts/generate_demo_liked_songs.py
"""
import json
import os
import random

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUMS_PATH = os.path.join(REPO_ROOT, "data", "albums.json")
OUT_PATH = os.path.join(REPO_ROOT, "data", "liked_songs_demo.json")

# How many tracks to sample per album (min, max) for variety
MIN_TRACKS_PER_ALBUM = 3
MAX_TRACKS_PER_ALBUM = 8

def main():
    random.seed(42)
    with open(ALBUMS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for album in data["albums"]:
        title = album["title"]
        artist = album["artist"]
        year = album["year"]
        tracks = album.get("tracks", [])
        if not tracks:
            continue
        n = min(len(tracks), random.randint(MIN_TRACKS_PER_ALBUM, max(MIN_TRACKS_PER_ALBUM, min(MAX_TRACKS_PER_ALBUM, len(tracks)))))
        chosen = random.sample(tracks, n)
        for track_name in chosen:
            items.append({
                "track": {
                    "name": track_name,
                    "artists": [{"name": artist}],
                    "album": {"name": title, "release_date": str(year)},
                    "popularity": random.randint(48, 82),
                }
            })

    # Shuffle so dashboard charts aren't just album-order
    random.shuffle(items)

    out = {"total": len(items), "items": items}
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(items)} liked songs to {OUT_PATH} ({len(data['albums'])} albums)")

if __name__ == "__main__":
    main()
