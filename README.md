# Spotify Data Retrieval & Dashboard

**Python project** that uses the Spotify Web API to retrieve your library data, top artists, and liked songs—with a **Streamlit dashboard** for visualization and comparison against manually curated data.

---

## Overview

This repo lets you:

- **Pull your Spotify data** (saved albums, liked songs, playlists, top artists)
- **Run a visual dashboard** of your liked songs (all time): top artists, top albums, release decades, and a searchable table
- **Compare** your Spotify data with manual “top albums” data (e.g. from `data/sample_saved_albums.json`) via alignment charts in the dashboard
- **Search artists** and inspect their top tracks and albums (client-credentials flow)

Useful for portfolio projects, data exploration, or keeping a local view of your music library.

---

## Tech stack

- **Python 3** (notebooks + scripts)
- **Spotify Web API** (OAuth authorization code + client credentials)
- **Jupyter** notebooks for exploration and one-off runs
- **Streamlit** + **Plotly** + **Pandas** for the Liked Songs dashboard
- **`.env`** for credentials (see Setup)

---

## Features

| Feature | Description |
|--------|-------------|
| **User library** | Saved albums, liked songs, playlists via `spotify_user_data_retrieval.ipynb` |
| **Top artists (from plays)** | Your top artists from Spotify (medium/short/long term) in `spotify_artists_from_my_plays.ipynb` |
| **Artist search** | Search by name, get top tracks and albums in `spotify_artist_data_retrieval.ipynb` |
| **Liked Songs dashboard** | Streamlit app: fetch all liked songs, then view “most plays” (proxy), top artists/albums, decades, manual-vs-Spotify alignment, searchable table |
| **Manual vs Spotify** | Cross-compare `data/sample_saved_albums.json` with Liked Songs in the dashboard and in [data/COMPARISON.md](data/COMPARISON.md) |
| **Sample data** | Use `data/` JSON and `spotify_user_data_from_sample.ipynb` without API keys |

---

## Quick start

```bash
git clone https://github.com/nurulashraf/spotify-data-retrieval.git
cd spotify-data-retrieval
pip install -r requirements.txt
```

1. Create a [Spotify app](https://developer.spotify.com/dashboard), add Redirect URI: `http://127.0.0.1:8080/callback`
2. Copy `.env.example` to `.env` and set `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI`
3. Run the first cell of `src/spotify_artists_from_my_plays.ipynb` to authorize; copy the `code` from the redirect URL
4. Paste the code into the second cell and run to fetch top artists, or use it with `src/fetch_all_liked_songs.py` for the dashboard (see below)

See [REDIRECT_URI_SETUP.md](REDIRECT_URI_SETUP.md) if you hit redirect URI errors.

---

## Liked Songs dashboard (all time)

1. Get an auth code (run first cell of `spotify_artists_from_my_plays.ipynb`, Agree, copy `?code=...` from the URL).
2. Fetch all liked songs (paginated):
   ```bash
   py src/fetch_all_liked_songs.py <your_auth_code>
   ```
   Saves to `data/liked_songs_all.json` (gitignored).
3. Run the dashboard:
   ```bash
   streamlit run src/dashboard_liked_songs.py
   ```
   Open http://localhost:8501.

**Dashboard includes:**

- **KPIs:** Total liked songs, unique artists/albums, release year span
- **Most plays (all time):** Horizontal bar chart (proxy: count of liked songs per artist)
- **Top artists / top albums** by count of liked songs
- **Liked songs by release decade**
- **Manual vs Spotify alignment:** Two charts comparing `data/sample_saved_albums.json` with your Liked Songs (artists in both; manual artists with/without liked tracks)
- **Searchable table** of all liked tracks

---

## Manual data vs Spotify API

- **Written comparison:** [data/COMPARISON.md](data/COMPARISON.md) — manual top artists/albums vs API top artists.
- **In the dashboard:** “Manual vs Spotify: do they align?” section with alignment charts (requires `data/sample_saved_albums.json`).

---

## Project structure

```
spotify-data-retrieval/
├── README.md
├── requirements.txt
├── .env.example
├── REDIRECT_URI_SETUP.md
├── SETUP_YOUR_ACCOUNT.md
├── data/
│   ├── sample_saved_albums.json   # Manual top albums (edit for comparison)
│   ├── sample_liked_songs.json
│   ├── sample_playlists.json
│   ├── COMPARISON.md              # Manual vs API write-up
│   └── README.md
└── src/
    ├── spotify_user_data_retrieval.ipynb
    ├── spotify_artists_from_my_plays.ipynb
    ├── spotify_artist_data_retrieval.ipynb
    ├── spotify_user_data_from_sample.ipynb
    ├── fetch_all_liked_songs.py   # Paginated fetch → liked_songs_all.json
    ├── dashboard_liked_songs.py   # Streamlit dashboard
    └── run_artist_notebook.py     # CLI run for artist search (e.g. Wolf Alice)
```

---

## API scopes used

- `user-library-read` — saved albums and tracks
- `user-top-read` — top artists and tracks
- `user-read-playback-state` — playback state (user notebook)

---

## Limitations

- Access token expires (~1 hour); re-authorize and paste a new code when needed.
- Redirect URI must match exactly (use `http://127.0.0.1:8080/callback`; see [Redirect URIs](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri)).

---

## Contributing

Contributions, issues, and feature requests are welcome.

---

## License

MIT — see [LICENSE](LICENSE).
