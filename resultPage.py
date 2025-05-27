
def get_recommendation_data(track, artist, sp):
    query = f"track:{track}"
    if artist:
        query += f" artist:{artist}"

    results = sp.search(q=query, type="track", limit=1)

    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_name = track["name"]
        track_url = track["external_urls"]["spotify"]
        artist_name = track["artists"][0]["name"]
        try:
            image_url = track['album']['images'][0]['url']
            height = track['album']['images'][0]['height']
            width = track['album']['images'][0]['width']
        except: 
            image_url = None
            height = None
            width = None
    return (track, track_name, track_url, artist_name, image_url, height, width)
