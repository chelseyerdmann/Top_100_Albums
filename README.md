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

## Pushing updates to GitHub

From the repo folder:

```powershell
cd c:\Users\chels\Top_100_Albums
git add .
git status
git commit -m "Your commit message"
git push origin main
```
