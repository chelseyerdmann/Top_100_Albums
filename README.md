# Top_100_Albums

A personal list of top albums with full track listings. Data is in `data/albums.json` for use in code, testing, or other projects.

## Data

- **`data/albums.json`** ? JSON array of albums. Each album has:
  - **`title`** ? Album name
  - **`artist`** ? Artist or band name
  - **`year`** ? Release year
  - **`tracks`** ? Array of song titles (in order)

### Example

```json
{
  "title": "Bloom",
  "artist": "Beach House",
  "year": 2012,
  "tracks": ["Myth", "Wild", "Lazuli", "Other People", "The Hours", "Troublemaker", "New Year", "Wishes", "On the Sea", "Irene"]
}
```

Load in scripts or tests (e.g. Node, Python) by parsing the JSON and iterating over `albums`.

## Dashboard (pandas + Streamlit)

A simple web dashboard visualizes the album data with [pandas](https://github.com/pandas-dev/pandas) (data analysis library) and Plotly.

### Install

From the repo folder (Python 3.8+):

```powershell
cd c:\Users\chels\Top_100_Albums
pip install -r requirements.txt
```

### Run

```powershell
cd c:\Users\chels\Top_100_Albums
streamlit run scripts/dashboard.py
```

A browser window opens with:

- **Metrics:** album count, artist count, total tracks
- **Filters:** year range and artist (sidebar)
- **Table:** albums (title, artist, year, track count)
- **Charts:** albums by year, albums per artist, track count distribution

## Pushing updates to GitHub

From the repo folder:

```powershell
cd c:\Users\chels\Top_100_Albums
git add .
git status
git commit -m "Your commit message"
git push origin main
```
