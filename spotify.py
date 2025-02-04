# Shows the top tracks for a user
import pymssql
import datetime
import os
import spotipy


from spotipy.oauth2 import SpotifyOAuth
def main():
    # Load environment variables for Spotify credentials
    client_id = os.getenv("Spotify_id")
    client_secret = os.getenv("Spotify_secret")
    sql_username = os.getenv("Azure_Sql_Username")
    sql_password =  os.getenv("Azure_Sql_Password")
    server = "servermind.database.windows.net"
    database = "sqlmindy"
   
    redirect_url = "https://musicmindwebapp-ctdncyfca8fzhsaf.eastus2-01.azurewebsites.net/"
    driver = "ODBC Driver 18 for SQL Server"
    user_tracks = []

    scope = 'user-top-read'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
                                                    client_secret=client_secret, 
                                                    redirect_uri=redirect_url, 
                                                    scope=scope))
                                                    



    #Connect to Azure SQL5
    conn = pymssql.connect(
    server=server,
    user=sql_username,
    password=sql_password,
    database=database,
    port="1433",
    charset="UTF-8",
    autocommit=True
    )

    cursor = conn.cursor()
    # Ensure client_id and client_secret are available
    if not client_id or not client_secret:
        raise ValueError("Spotify client ID or secret not set in environment variables.")

    # Define the scope and authenticate

    # Define the time ranges for top tracks
    ranges = ['short_term', 'medium_term', 'long_term']
    UserID = sp.current_user().get("id")




    #if not row: 
    SPUserId = sp.current_user().get("id")
    SpUName = sp.current_user().get("name")
    Email = sp.current_user().get("email")
    JoinDate = datetime.datetime.now()
    try:
        cursor.execute("Insert Into Users(UserId, Name, Email, JoinDate) Values (%s, %s, %s, %s)", (SPUserId, SpUName, Email, JoinDate))
    except Exception as e:
        cursor.execute("SELECT * FROM Users WHERE UserId = %s", UserID)
        row = cursor.fetchone()
    # Fetch and display top tracks for each range
    for sp_range in ranges:
        print(f"Time Range: {sp_range.capitalize()}")
        try:
            topTrack = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            #topArtist = sp.current_user_top_artists(time_range=sp_range, limit=50)
            items = topTrack.get('items', [])
            if not items:
                print("No top tracks found for this range.\n")
                continue
            for item in items:
                    try: 
                        trackId = item.get('id')
                        trackName = item.get('name', 'Unknown Track')
                        artistName = item['artists'][0]['name'] if item.get('artists') else 'Unknown Artist'
                        cursor.execute("Insert Into Tracks(TrackId, UserId, TrackName, Artist) Values (%s, %s, %s, %s)", (trackId, SPUserId, trackName, artistName))
                        cursor.execute("Insert Into UserTrack(UserId, TrackId, TrackName, Artist) Values (%s, %s, %s, %s)", (SPUserId, trackId, trackName, artistName))

                        #print(f"{i + 1}. {track_name} // {artist_name}")
                    except Exception as e:
                        continue
        except Exception as e:
                print(f"An error occurred while fetching top tracks for {sp_range}: {e}")
        print()
    
    cursor.execute("SELECT * FROM UserTrack WHERE UserId = %s", UserID)
    results = cursor.fetchall()
    for result in results:
         trackName = result[2]
         artist = result [3]
         user_tracks.append(trackName + " by " + artist )
    conn.commit()
    cursor.close()
    conn.close()
    print (user_tracks)
    return user_tracks

