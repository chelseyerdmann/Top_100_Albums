"""
Top 100 Albums – simple dashboard using pandas and Streamlit.
Run from repo root: streamlit run scripts/dashboard.py
"""
import json
import os
import sys

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load data
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data", "albums.json")

with open(DATA_PATH, encoding="utf-8") as f:
    raw = json.load(f)

albums = raw["albums"]

# Build DataFrame: one row per album, with track count
rows = []
for a in albums:
    rows.append({
        "title": a["title"],
        "artist": a["artist"],
        "year": a["year"],
        "track_count": len(a.get("tracks", [])),
    })
df = pd.DataFrame(rows)

st.set_page_config(page_title="Top 100 Albums", layout="wide")
st.title("Top 100 Albums – Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))
artist_options = ["All"] + sorted(df["artist"].unique().tolist())
selected_artist = st.sidebar.selectbox("Artist", artist_options)

# Apply filters
mask = (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])
if selected_artist != "All":
    mask = mask & (df["artist"] == selected_artist)
df_filtered = df[mask]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Albums", len(df_filtered))
col2.metric("Artists", df_filtered["artist"].nunique())
col3.metric("Total tracks", df_filtered["track_count"].sum())

# Table
st.subheader("Albums")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

# Charts
st.subheader("Albums by year")
year_counts = df_filtered.groupby("year").size().reset_index(name="count")
fig_year = px.bar(year_counts, x="year", y="count", labels={"year": "Year", "count": "Albums"})
st.plotly_chart(fig_year, use_container_width=True)

st.subheader("Albums per artist")
artist_counts = df_filtered["artist"].value_counts().reset_index()
artist_counts.columns = ["artist", "count"]
fig_artist = px.bar(artist_counts.head(15), x="artist", y="count", labels={"artist": "Artist", "count": "Albums"})
fig_artist.update_xaxis(tickangle=-45)
st.plotly_chart(fig_artist, use_container_width=True)

st.subheader("Track count per album")
fig_tracks = px.histogram(df_filtered, x="track_count", nbins=15, labels={"track_count": "Number of tracks"})
st.plotly_chart(fig_tracks, use_container_width=True)
