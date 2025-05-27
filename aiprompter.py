import os
import re
from openai import AzureOpenAI
import quickstart
import pymssql

def main(genre, artist, image_urls, personalization, user_tracks):
  print("Personalization: " + personalization)
  vision = quickstart
  visionResult = vision.main(image_urls)

  tags = quickstart.add_tags(visionResult)
  captions = quickstart.add_caption(visionResult)

  tags_string = ", ".join(tags)
  print("Tags: " + tags_string + "\n")
  captions_string = ", ".join(captions)
  print("Captions: " + captions_string + "\n")
  music_preference = genre
  artist_prefered = artist

  if personalization == "spotify":
    print("based off spotify suggestions: ")
    client_prompt = f"""
    Based on the provided information, the photo is associated with these tags: {tags_string}, and includes the following captions: {captions_string}.
    The user's taste in music is reflected in their top tracks: {user_tracks}.

    Please provide your response in the following structured format:

    1. Song Recommendation: "Track Name" by Artist Name  
    2. Key Part of the Song: [e.g., chorus, verse, bridge]  
    3. Why It Fits: [1–2 sentence explanation of how the part connects with the photo]  
    4. Suggested Caption: [A creative and engaging Instagram caption]

    Keep the formatting consistent so it can be parsed programmatically.
    """
  else:
    print("based off artist and genre preference")
    client_prompt = f"""
    Based on the provided information, the photo is associated with these tags: {tags_string}, and includes the following captions: {captions_string}.

    Please recommend a **unique** song that complements the mood, theme, or story conveyed by the photo.

    Consider the user's preferences:
    - Preferred music style/genre: {music_preference}
    - Preferred artist: {artist_prefered}

    Please respond using the following structured format:

    1. Song Recommendation: "Track Name" by Artist Name  
    2. Key Part of the Song: [e.g., verse, chorus, bridge]  
    3. Why It Fits: [1–2 sentences explaining how that part aligns with the photo]  
    4. Suggested Caption: [A creative and engaging Instagram caption]

    Keep the formatting consistent so the response can be parsed programmatically.
    """


  client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01"
  )
  
  response = client.chat.completions.create(
      model="gpt-35-turbo", # model = "deployment_name".
      messages=[
          {"role": "system", "content": "You are a music assistant helping to suggest unique music to complement images for an instagram post and suggest a caption to compliment it."},
          {"role": "user", "content": client_prompt}
      ]
  )
  if response and response.choices and response.choices[0].message and response.choices[0].message.content:
      result = response.choices[0].message.content
      print("Response content:", result)
  else:
      print("Error: Empty or malformed response from OpenAI.")
 
  recommendation_track, recommendation_artist = get_recommendation(result)

  return(result, recommendation_track, recommendation_artist)

def get_recommendation(result):
    match = re.search(r'Song Recommendation: "(.*?)" by (.*?)\n', result)

    if match:
      track = match.group(1)
      track = str(track)
      artist = match.group(2)
      artist = str(artist)
      print(f"Track: {track}")
      print(f"Artist: {artist}")
      return track, artist
    else:
      print("No match found.")
      return None, None
