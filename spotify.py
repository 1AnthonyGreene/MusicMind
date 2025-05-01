import os
import datetime
import pymssql
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def connect_spotify():
    """Authenticate and return a Spotipy client."""
    client_id = os.getenv("Spotify_id")
    client_secret = os.getenv("Spotify_secret")
    redirect_url = "https://mindmind-hge3gkf6achycjd7.eastus2-01.azurewebsites.net/callback"  # Ensure HTTPS + callback

    if not client_id or not client_secret:
        raise ValueError("Spotify client ID or secret not set in environment variables.")

    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_url,
        scope=scope
    ))
    return sp


def connect_sql():
    """Connect to Azure SQL Database and return the connection and cursor."""
    server = "servermind.database.windows.net"
    database = "sqlmindy"
    username = os.getenv("Azure_Sql_Username")
    password = os.getenv("Azure_Sql_Password")

    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        port="1433",
        charset="UTF-8",
        autocommit=True
    )
    cursor = conn.cursor()
    return conn, cursor


def insert_user(cursor, user_info):
    """Insert user into the database if not already exists."""
    try:
        cursor.execute(
            "INSERT INTO Users (UserId, Name, Email, JoinDate) VALUES (%s, %s, %s, %s)",
            (user_info['id'], user_info['display_name'], user_info['email'], datetime.datetime.now())
        )
    except Exception as e:
        print(f"User might already exist or error inserting user: {e}")
        cursor.execute("SELECT * FROM Users WHERE UserId = %s", (user_info['id'],))
        return cursor.fetchone()
    return None


def insert_tracks(cursor, sp, user_id):
    """Insert user's top tracks into the database."""
    ranges = ['short_term', 'medium_term', 'long_term']
    user_tracks = []

    for sp_range in ranges:
        print(f"Fetching top tracks for range: {sp_range}")
        try:
            top_tracks = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            items = top_tracks.get('items', [])
            if not items:
                print(f"No top tracks found for {sp_range}.")
                continue

            for item in items:
                try:
                    track_id = item.get('id')
                    track_name = item.get('name', 'Unknown Track')
                    artist_name = item['artists'][0]['name'] if item.get('artists') else 'Unknown Artist'

                    # Optional: Check if track already inserted to prevent duplication (requires slight DB design)

                    cursor.execute(
                        "INSERT INTO Tracks (TrackId, UserId, TrackName, Artist) VALUES (%s, %s, %s, %s)",
                        (track_id, user_id, track_name, artist_name)
                    )
                    cursor.execute(
                        "INSERT INTO UserTrack (UserId, TrackId, TrackName, Artist) VALUES (%s, %s, %s, %s)",
                        (user_id, track_id, track_name, artist_name)
                    )

                    user_tracks.append(f"{track_name} by {artist_name}")
                except Exception as e:
                    print(f"Failed to insert track '{track_name}': {e}")
                    continue
        except Exception as e:
            print(f"Error fetching top tracks for {sp_range}: {e}")
            continue

    return user_tracks


def main():
    sp = connect_spotify()
    conn, cursor = connect_sql()

    try:
        user_info = sp.current_user()
        print(f"Connected as {user_info['display_name']} ({user_info['email']})")

        insert_user(cursor, user_info)
        user_tracks = insert_tracks(cursor, sp, user_info['id'])

        print("\nUser's Top Tracks:")
        for track in user_tracks:
            print(track)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
