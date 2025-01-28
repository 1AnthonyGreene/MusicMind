import os
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
    client_prompt = f"Based on the provided information, the photo is associated with these tags: {tags_string}, and includes the following captions: {captions_string}. Consider the users taste in music based off their top tracks: {user_tracks} Please recommend a song that complements the mood, theme, or story conveyed by the photo. Additionally, identify which specific part of the song (e.g., verse, chorus, bridge) best aligns with the photo's essence and explain why it fits. Also suggest a creative caption to go with it."
  else:
    print("based off artist and genre preference")
    client_prompt = f"Based on the provided information, the photo is associated with these tags: {tags_string}, and includes the following captions: {captions_string}. Please recommend a unique song that complements the mood, theme, or story conveyed by the photo. For context, these photos are taken in Tennesse during winter break. Consider the following preferences: music style/genre: {music_preference}, and preferred artist: {artist_prefered}. Additionally, identify which specific part of the song (e.g., verse, chorus, bridge) best aligns with the photo's essence and explain why it fits. Also suggest a creative caption to go with it."


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

  print(response.choices[0].message.content)
  return(response.choices[0].message.content)

def get_user_tracks():
  pass

