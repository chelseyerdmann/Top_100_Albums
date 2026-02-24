"""
Visual dashboard for your Spotify Liked Songs (all time).
Requires data/liked_songs_all.json — run: py src/fetch_all_liked_songs.py <auth_code> first.

Run: streamlit run src/dashboard_liked_songs.py
"""
import json
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# Path to data
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "liked_songs_all.json"
MANUAL_ALBUMS_PATH = ROOT / "data" / "sample_saved_albums.json"

# Normalize artist name for comparison (case-insensitive; fix known typos)
def _norm(s):
    if not s or s == "?":
        return ""
    s = s.strip().lower()
    if s == "lana del ray":
        s = "lana del rey"
    return s


def load_liked_songs():
    if not DATA_PATH.exists():
        return None, "No data file found. Run: **py src/fetch_all_liked_songs.py &lt;auth_code&gt;** (get the code from the Spotify redirect URL after authorizing)."
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    return items, None


def load_manual_albums():
    """Load manual top albums from sample_saved_albums.json. Returns (artist_set_normalized, list of (album_name, artist_name))."""
    if not MANUAL_ALBUMS_PATH.exists():
        return set(), []
    with open(MANUAL_ALBUMS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    artists_norm = set()
    albums_list = []
    for it in items:
        album = it.get("album") or {}
        arts = album.get("artists") or []
        name = album.get("name", "?")
        artist_name = arts[0].get("name", "?") if arts else "?"
        artists_norm.add(_norm(artist_name))
        albums_list.append((name, artist_name))
    return artists_norm, albums_list


def build_records(items):
    records = []
    for it in items:
        track = it.get("track") or {}
        if not track:
            continue
        name = track.get("name", "?")
        artists = [a.get("name", "?") for a in track.get("artists", [])]
        artist_names = ", ".join(artists) if artists else "?"
        album = (track.get("album") or {})
        album_name = album.get("name", "?")
        release_date = album.get("release_date", "")[:4] if album.get("release_date") else ""
        popularity = track.get("popularity")
        records.append({
            "track_name": name,
            "artists": artist_names,
            "artist_first": artists[0] if artists else "?",
            "album": album_name,
            "release_year": release_date or None,
            "popularity": popularity,
        })
    return records


def main():
    st.set_page_config(page_title="Liked Songs Dashboard", layout="wide")
    st.title("My Spotify Liked Songs — All Time")
    st.caption("Dashboard of your liked tracks. Data from Spotify API (all time).")

    items, err = load_liked_songs()
    if err:
        st.warning(err)
        st.info("To get your auth code: run the first cell of `spotify_artists_from_my_plays.ipynb`, click Agree in the browser, then copy the part of the URL after `?code=` and before `&`.")
        return

    records = build_records(items)
    df = pd.DataFrame(records)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total liked songs", len(df))
    with col2:
        st.metric("Unique artists", df["artist_first"].nunique())
    with col3:
        st.metric("Unique albums", df["album"].nunique())
    with col4:
        years = df["release_year"].dropna()
        st.metric("Release years span", f"{int(years.min())}–{int(years.max())}" if len(years) else "—")

    st.divider()

    # Most plays (proxy: count of liked songs per artist — Spotify doesn't provide personal play counts)
    st.subheader("Most plays (all time)")
    st.caption("Spotify doesn't share personal play counts, so we use **number of liked songs per artist** as a proxy for who you play the most.")
    artist_counts = df["artist_first"].value_counts().head(25)
    plot_df = artist_counts.reset_index()
    plot_df.columns = ["artist", "liked_songs"]
    plot_df = plot_df.sort_values("liked_songs", ascending=True)  # so top artist is at top of horizontal bar
    fig = px.bar(
        plot_df, x="liked_songs", y="artist", orientation="h",
        labels={"liked_songs": "Liked songs in your library", "artist": ""},
        color="liked_songs", color_continuous_scale="Teal",
        text="liked_songs",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, coloraxis_showscale=False, margin=dict(l=20), height=700, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top artists by number of liked songs (simple bar)
    st.subheader("Top artists (by number of liked songs)")
    artist_counts_20 = df["artist_first"].value_counts().head(20)
    st.bar_chart(artist_counts_20)

    st.divider()

    # Top albums
    st.subheader("Top albums (by number of liked songs)")
    album_counts = df["album"].value_counts().head(20)
    st.bar_chart(album_counts)

    st.divider()

    # Release year distribution
    st.subheader("Liked songs by release decade")
    df_year = df[df["release_year"].notna()].copy()
    df_year["release_year"] = df_year["release_year"].astype(int)
    df_year["decade"] = (df_year["release_year"] // 10) * 10
    decade_counts = df_year["decade"].value_counts().sort_index()
    st.bar_chart(decade_counts)

    st.divider()

    # --- Manual vs Spotify alignment (cross-compare with data/sample_saved_albums.json) ---
    manual_artists_norm, manual_albums_list = load_manual_albums()
    if manual_artists_norm and manual_albums_list:
        st.subheader("Manual vs Spotify: do they align?")
        st.caption("Comparing your **manual top albums** (`data/sample_saved_albums.json`) with your **Spotify Liked Songs**.")

        # Spotify artist -> count; artist_first is the primary artist per track
        spotify_artist_counts = df["artist_first"].value_counts()

        # 1) Artists in BOTH: appear in manual and have liked songs
        df["artist_norm"] = df["artist_first"].map(lambda a: _norm(a))
        in_both = spotify_artist_counts[
            spotify_artist_counts.index.map(lambda a: _norm(a) in manual_artists_norm)
        ]
        if len(in_both) > 0:
            plot_both = in_both.reset_index()
            plot_both.columns = ["artist", "liked_songs"]
            plot_both = plot_both.sort_values("liked_songs", ascending=True)
            fig_both = px.bar(
                plot_both, x="liked_songs", y="artist", orientation="h",
                labels={"liked_songs": "Liked songs", "artist": ""},
                color="liked_songs", color_continuous_scale="Blues",
                text="liked_songs",
            )
            fig_both.update_traces(textposition="outside")
            fig_both.update_layout(showlegend=False, coloraxis_showscale=False, margin=dict(l=20), height=400, yaxis=dict(autorange="reversed"))
            st.markdown("**Artists in both:** manual top albums *and* in your Liked Songs (by count of liked tracks)")
            st.plotly_chart(fig_both, use_container_width=True)
        else:
            st.info("No artists from your manual list appear in your Liked Songs (or names don't match).")

        # 2) For each unique manual artist: how many liked songs? (alignment of manual with Spotify)
        unique_manual_artists = list(dict.fromkeys(a for _, a in manual_albums_list))  # preserve order, unique
        manual_liked = []
        for artist_display in unique_manual_artists:
            count = spotify_artist_counts.get(artist_display, 0)
            if count == 0:
                # try match by norm (e.g. alt-J vs Alt-J)
                for spotify_artist, c in spotify_artist_counts.items():
                    if _norm(spotify_artist) == _norm(artist_display):
                        count = c
                        break
            manual_liked.append({"artist": artist_display, "liked_songs": count, "aligns": "Yes" if count > 0 else "No"})
        manual_df = pd.DataFrame(manual_liked).sort_values("liked_songs", ascending=True)
        fig_manual = px.bar(
            manual_df, x="liked_songs", y="artist", orientation="h",
            color="aligns", color_discrete_map={"Yes": "#2ecc71", "No": "#e74c3c"},
            labels={"liked_songs": "Liked songs in your library", "artist": ""},
            text="liked_songs",
        )
        fig_manual.update_traces(textposition="outside")
        fig_manual.update_layout(margin=dict(l=20), height=max(350, len(manual_df) * 22), yaxis=dict(autorange="reversed"), legend_title="In your Liked Songs?")
        st.markdown("**Your manual top-album artists:** how many of their tracks are in your Liked Songs (green = aligns, red = none)")
        st.plotly_chart(fig_manual, use_container_width=True)

        # Summary metrics
        n_manual = len(unique_manual_artists)
        n_align = sum(1 for r in manual_liked if r["liked_songs"] > 0)
        st.metric("Manual artists that appear in Liked Songs", f"{n_align} of {n_manual}", delta=f"{100 * n_align // n_manual}% alignment" if n_manual else None)
    else:
        st.subheader("Manual vs Spotify")
        st.caption("Add manual top albums in `data/sample_saved_albums.json` to see alignment charts here.")

    st.divider()

    # Table: searchable
    st.subheader("All liked songs (searchable)")
    search = st.text_input("Search by track, artist, or album", key="search")
    if search:
        search_lower = search.lower()
        mask = (
            df["track_name"].str.lower().str.contains(search_lower, na=False)
            | df["artists"].str.lower().str.contains(search_lower, na=False)
            | df["album"].str.lower().str.contains(search_lower, na=False)
        )
        df_show = df.loc[mask]
    else:
        df_show = df
    df_show = df_show[["track_name", "artists", "album", "release_year", "popularity"]]
    df_show.columns = ["Track", "Artists", "Album", "Year", "Popularity"]
    st.dataframe(df_show, use_container_width=True, height=400)


if __name__ == "__main__":
    main()
