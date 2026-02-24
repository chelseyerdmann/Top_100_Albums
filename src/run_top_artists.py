"""Run second cell: exchange auth code for token and fetch top artists."""
import requests
import base64

client_id = "your_client_id"
client_secret = "your_client_secret"
redirect_uri = "http://127.0.0.1:8080/callback"
auth_code = "AQAXkLC9Uz00wPBND-8CxgrcmnfqPM_fsBdu1H5ikdAagZtu9vmUnowQWy9rda5UNa16-chPOtfdmjyDB3OplgyK9w7JCTDksGtbu-dt-eY6Gkvg_rcTQGX32Xrf2lIMSVWYw0H8ucCS6WiypBgd0Z6o4yAzHPmh-u2pEyhuXkoL9AYdwgUi1ZPmMBceVWK8KA5UeE11dOz40F_WpmKDLvM0OsM"

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
