# Top 100 Albums & Spotify Data Retrieval

A combined project: **manual top albums** with a Streamlit dashboard, plus **Spotify Web API** integration to retrieve your library, liked songs, and top artists—with dashboards and comparison to your manual list.

---

## About this project

This repo demonstrates end-to-end data pipelines and dashboards: **REST APIs** (Spotify Web API with OAuth and client credentials), **data ingestion** (paginated fetches, JSON), **analysis** (Pandas), and **visualization** (Streamlit, Plotly). It also cross-compares API data with manually curated data and deploys a live dashboard (Streamlit Community Cloud) so reviewers can see the output without running anything locally.

**Tech stack:** Python · Spotify Web API (OAuth, client credentials) · Jupyter · Streamlit · Plotly · Pandas · JSON

---

## View the Liked Songs dashboard (no setup)

You can view the **Spotify Liked Songs dashboard** with sample data without cloning or running anything:

**[View dashboard (demo)](https://top100albums-kryrwafdbmdkzcs5xjnwim.streamlit.app/)**

The demo uses `data/liked_songs_demo.json` so visitors see the layout and charts. To use your own Liked Songs, follow the [Quick start](#quick-start-spotify) and run the dashboard locally.

### How to add your own live link

1. Go to [Streamlit Community Cloud](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**; select this repo, branch `main`, and app path: `src/dashboard_liked_songs.py`.
3. Deploy; Streamlit will give you a URL like `https://your-app-name.streamlit.app`.
4. Put that URL in the link above (replace `https://your-app-name.streamlit.app`) so visitors can open the dashboard from the README.

---

## What’s in this repo

| Part | Description |
|------|-------------|
| **Top 100 Albums** | Personal list in `data/albums.json`; dashboard in `scripts/dashboard.py` (pandas + Streamlit). |
| **Spotify** | API scripts and notebooks to fetch saved albums, liked songs, top artists; Streamlit dashboard for liked songs and manual-vs-Spotify alignment. |

---

## Top 100 Albums (manual list)

- **`data/albums.json`** — JSON array of albums: `title`, `artist`, `year`, `tracks` (song titles in order).
- **Dashboard:** `streamlit run scripts/dashboard.py` — metrics, filters (year, artist), table, charts (albums by year, per artist, track count).

### Example album entry

```json
{
  "title": "Bloom",
  "artist": "Beach House",
  "year": 2012,
  "tracks": ["Myth", "Wild", "Lazuli", "Other People", "The Hours", "Troublemaker", "New Year", "Wishes", "On the Sea", "Irene"]
}
```

---

## Spotify Data Retrieval & Dashboard

**Tech:** Python, Spotify Web API (OAuth + client credentials), Jupyter notebooks, Streamlit, Plotly, Pandas.

### Features

- **User library:** Saved albums, liked songs, playlists (`src/spotify_user_data_retrieval.ipynb`).
- **Top artists (from plays):** Your top artists from Spotify in `src/spotify_artists_from_my_plays.ipynb`.
- **Artist search:** Search by name, get top tracks/albums (`src/spotify_artist_data_retrieval.ipynb`).
- **Liked Songs dashboard:** Fetch all liked songs with `src/fetch_all_liked_songs.py`, then run `streamlit run src/dashboard_liked_songs.py` for:
  - KPIs, “most plays” (proxy by liked count), top artists/albums, release decades
  - **Manual vs Spotify** alignment charts (compares `data/sample_saved_albums.json` with your Liked Songs)
  - Searchable table of all tracks
- **Comparison:** [data/COMPARISON.md](data/COMPARISON.md) — manual top artists/albums vs Spotify API.

### Quick start (Spotify)

1. Clone and install:
   ```bash
   git clone https://github.com/chelseyerdmann/Top_100_Albums.git
   cd Top_100_Albums
   pip install -r requirements.txt
   ```
2. Create a [Spotify app](https://developer.spotify.com/dashboard), add Redirect URI: `http://127.0.0.1:8080/callback`.
3. Copy `.env.example` to `.env`; set `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI`.
4. Run the first cell of `src/spotify_artists_from_my_plays.ipynb` to authorize; copy the `code` from the redirect URL and use it in the second cell or with `src/fetch_all_liked_songs.py`.

See [REDIRECT_URI_SETUP.md](REDIRECT_URI_SETUP.md) if you hit redirect URI errors.

### Liked Songs dashboard

```bash
py src/fetch_all_liked_songs.py <your_auth_code>
streamlit run src/dashboard_liked_songs.py
```

Open http://localhost:8501.

---

## Project structure

```
├── README.md
├── requirements.txt
├── .env.example
├── REDIRECT_URI_SETUP.md
├── SETUP_YOUR_ACCOUNT.md
├── data/
│   ├── albums.json              # Top 100 Albums (manual)
│   ├── sample_saved_albums.json # Sample / manual list for Spotify comparison
│   ├── sample_liked_songs.json
│   ├── sample_playlists.json
│   ├── COMPARISON.md
│   └── README.md
├── scripts/
│   └── dashboard.py             # Top 100 Albums Streamlit dashboard
└── src/
    ├── spotify_user_data_retrieval.ipynb
    ├── spotify_artists_from_my_plays.ipynb
    ├── spotify_artist_data_retrieval.ipynb
    ├── spotify_user_data_from_sample.ipynb
    ├── fetch_all_liked_songs.py
    ├── dashboard_liked_songs.py  # Spotify Liked Songs dashboard
    └── run_artist_notebook.py
```

---

## Pushing updates to GitHub

```bash
git add .
git status
git commit -m "Your commit message"
git push origin main
```

---

## License

MIT — see [LICENSE](LICENSE).
