"""Run artist data retrieval (Wolf Alice) - same logic as the notebook."""
import requests
import base64

# Credentials (from .env or notebook)
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# Get token
auth_str = f"{client_id}:{client_secret}"
auth_base64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
response = requests.post(
    'https://accounts.spotify.com/api/token',
    headers={'Authorization': f'Basic {auth_base64}', 'Content-Type': 'application/x-www-form-urlencoded'},
    data={'grant_type': 'client_credentials'}
)
access_token = response.json()['access_token']

def search_artist(query):
    r = requests.get("https://api.spotify.com/v1/search", headers={'Authorization': f'Bearer {access_token}'}, params={'q': query, 'type': 'artist', 'limit': 5})
    return r.json()

def get_artist_top_tracks(artist_id):
    r = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks", headers={'Authorization': f'Bearer {access_token}'}, params={'market': 'US'})
    return r.json()

def get_artist_albums(artist_id):
    r = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/albums", headers={'Authorization': f'Bearer {access_token}'}, params={'market': 'US', 'limit': 5, 'include_groups': 'album,single'})
    return r.json()

def get_album_tracks(album_id):
    r = requests.get(f"https://api.spotify.com/v1/albums/{album_id}/tracks", headers={'Authorization': f'Bearer {access_token}'}, params={'market': 'US'})
    return r.json()

def get_artist_info(artist_id):
    r = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers={'Authorization': f'Bearer {access_token}'})
    return r.json()

# Run for Wolf Alice
search_query = 'Wolf Alice'
search_results = search_artist(search_query)

print(f"Search results for '{search_query}':")
for idx, artist in enumerate(search_results['artists']['items'], start=1):
    print(f"{idx}. {artist['name']} (ID: {artist['id']})")

artist_id = search_results['artists']['items'][0]['id']
artist_info = get_artist_info(artist_id)

genres = artist_info.get('genres', [])
followers = artist_info.get('followers', {}) or {}
print(f"\nInformation about {artist_info['name']}:")
print(f"Genres: {', '.join(genres) if genres else 'N/A'}")
print(f"Popularity: {artist_info.get('popularity', 'N/A')}")
print(f"Followers: {followers.get('total', 'N/A')}")
print("Images:")
for img in artist_info.get('images', []):
    print(f" - {img['url']} ({img['width']}x{img['height']})")

top_tracks = get_artist_top_tracks(artist_id)
tracks_list = top_tracks.get('tracks', [])
print(f"\nTop tracks by {artist_info['name']}:")
for idx, track in enumerate(tracks_list, start=1):
    print(f"{idx}. {track.get('name', '?')} - {track.get('popularity', '?')}")

albums = get_artist_albums(artist_id)
albums_list = albums.get('items', [])
print(f"\nAlbums by {artist_info['name']}:")
for idx, album in enumerate(albums_list, start=1):
    print(f"{idx}. {album.get('name', '?')} (ID: {album.get('id', '?')})")

if albums_list:
    album_id = albums_list[0]['id']
    album_tracks = get_album_tracks(album_id)
    album_tracks_list = album_tracks.get('items', [])
    print(f"\nTracks in the album '{albums_list[0].get('name', '?')}':")
    for idx, track in enumerate(album_tracks_list, start=1):
        print(f"{idx}. {track.get('name', '?')}")
else:
    print("\nNo albums found.")
