# Cross-Comparison: Manual Data vs Spotify API

This document compares the **manually entered data** in `data/sample_saved_albums.json` with **Spotify API data** (your top 20 artists from `spotify_artists_from_my_plays.ipynb` / medium-term listening).

---

## Top Artists Comparison

### Artists in BOTH manual saved albums AND API top 20

| Artist (manual) | In API top 20 | Notes |
|-----------------|---------------|--------|
| Alt-J           | ✓ #5 (alt-J)  | Same artist, different casing |
| Wolf Alice      | ✓ #8          | |
| Sturgill Simpson| ✓ #3          | |
| The Avett Brothers | ✓ #7       | |
| Manchester Orchestra | ✓ #11    | |
| Yeah Yeah Yeahs | ✓ #13          | |
| Big Thief       | ✓ #14          | |
| Pink Floyd      | ✓ #17          | |
| Blind Pilot     | ✓ #19          | |
| Lana Del Rey    | ✓ #20          | Manual has "Lana Del Ray" (typo) |

**10 artists** from your manual saved albums also appear in your Spotify top 20 artists.

### Artists in manual saved albums but NOT in API top 20

- Elton John  
- Fleetwood Mac  
- Trampled by Turtles  
- The Beatles  
- BORNS  
- Julia Jacklin  
- The Decemberists  
- Beach House  

These are in your saved albums list but did not appear in the medium-term top 20 artists from the API.

### Artists in API top 20 but NOT in manual saved albums

- White Noise Radiance  
- Enya  
- Sierra Ferrell  
- Mark Knopfler  
- Bahamas  
- The Paper Kites  
- Khruangbin  
- Future Islands  
- Mitski  
- Green Day  

These are in your listening (top artists) but do not have saved albums in the manual sample file.

---

## Top Albums Comparison

Manual data lists **27 saved albums**. Selected albums from manual data and whether that artist appears in API top artists:

| Album (manual) | Artist | Artist in API top 20? |
|----------------|--------|------------------------|
| Blue Weekend   | Wolf Alice | ✓ |
| The Dream / RELAXER / This Is All Yours | Alt-J | ✓ |
| Cuttin' Grass Vol. 1, The Ballad of Dood & Juanita | Sturgill Simpson | ✓ |
| Emotionalism, Mignonette, The Gleam II | The Avett Brothers | ✓ |
| Mean Everything to Nothing | Manchester Orchestra | ✓ |
| The Wall, Meddle | Pink Floyd | ✓ |
| Mosquito (Deluxe), It's Blitz! | Yeah Yeah Yeahs | ✓ |
| Dragon New Warm Mountain I Believe In You | Big Thief | ✓ |
| 3 Rounds and a Sound | Blind Pilot | ✓ |
| Norman Fucking Rockwell | Lana Del Rey | ✓ |
| The King is Dead, The Crane Wife | The Decemberists | No |
| Bloom | Beach House | No |
| Captain Fantastic... | Elton John | No |
| Tusk | Fleetwood Mac | No |
| Sgt. Peppers..., The Beatles | The Beatles | No |

**Summary:** Your manual saved albums align well with your API top artists: 10 of the artists in your manual list are in your Spotify top 20. The rest of the manual list (e.g. Fleetwood Mac, The Beatles, Beach House) are saved albums you care about but may listen to less frequently in the medium-term window.

---

## How to regenerate this comparison

1. Run `spotify_artists_from_my_plays.ipynb` (paste auth code, run second cell) to get fresh top artists.
2. Optionally run `spotify_user_data_retrieval.ipynb` to get live saved albums from the API.
3. Compare the artist names and album lists from the API output with `data/sample_saved_albums.json`.
