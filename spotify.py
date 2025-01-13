import base64
import os
import requests
import json

# API Credentials
CLIENT_ID = os.getenv("mm_spotify_id")
CLIENT_SECRET = os.getenv("mm_spotify_secret")

# API endpoints
AUTH_URL = 'https://accounts.spotify.com/api/token'
PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/1ga7Wnub0chLWRkUVP7Yzm'
PLAYLIST_ID = '1ga7Wnub0chLWRkUVP7Yzm'


def get_access_token(client_id, client_secret):
    """Retrieve an access token using the client credentials flow."""
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(AUTH_URL, headers=headers, data=data)
    if response.status_code != 200:
        print("Error retrieving token:", response.status_code, response.json())
        return None

    json_result = response.json()
    return json_result.get("access_token")


def get_track_tempo(track_id, access_token):
    """Retrieve the tempo of a track using its ID."""
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('tempo')
    else:
        print(f"Error fetching tempo for track {track_id}: {response.status_code}, {response.json()}")
        return None


def get_URI(track_id, access_token):
    """Retrieve the Spotify URI for a track."""
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('uri')
    else:
        print(f"Error fetching URI for track {track_id}: {response.status_code}, {response.json()}")
        return None


def get_playlist_tracks(playlist_url, access_token):
    """Retrieve the tracks from a playlist."""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(playlist_url, headers=headers)
    if response.status_code != 200:
        print("Failed to get playlist tracks:", response.json())
        return None
    playlist_data = response.json()
    return playlist_data.get('tracks', {}).get('items', [])


def create_playlist(access_token):
    """Create a new playlist."""
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "TEMPO TESTER",
        "description": "This playlist was made to test the Spotify BPM code",
        "public": True
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json().get('id')
    else:
        print("Failed to create playlist:", response.status_code, response.json())
        return None


def add_tracks(new_playlist_id, track_and_bpm, access_token):
    """Add tracks to a playlist."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    uris = [track[4] for track in track_and_bpm]
    data = {"uris": uris}
    url = f"https://api.spotify.com/v1/playlists/{new_playlist_id}/tracks"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Tracks added successfully!")
    else:
        print("Failed to add tracks:", response.status_code, response.json())


def main():
    """Main program execution."""
    # Get access token
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        return

    # Get playlist tracks
    playlist_tracks = get_playlist_tracks(PLAYLIST_URL, access_token)
    if not playlist_tracks:
        return

    # Output track information
    seperated_list = []
    for track in playlist_tracks:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        track_id = track['track']["id"]
        bpm = get_track_tempo(track_id, access_token)
        uri = get_URI(track_id, access_token)
        if bpm and uri:
            track_and_bpm = [track_name, artist_name, bpm, track_id, uri]
            seperated_list.append(track_and_bpm)

    # Sort tracks by BPM in descending order
    seperated_list = sorted(seperated_list, key=lambda x: x[2], reverse=True)
    print(seperated_list)

    # Create a new playlist and add tracks
    new_playlist_id = create_playlist(access_token)
    if new_playlist_id:
        add_tracks(new_playlist_id, seperated_list, access_token)


if __name__ == "__main__":
    main()
