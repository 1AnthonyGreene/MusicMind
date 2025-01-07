import os
from openai import AzureOpenAI
import quickstart

def main(genre, artist, image_url):
  vision = quickstart
  visionResult = vision.main(image_url)

  tags = vision.add_tags(visionResult)
  captions = vision.add_caption(visionResult)

  tags_string = ", ".join(tags)
  print("Tags: " + tags_string + "\n")
  captions_string = ", ".join(captions)
  print("Captions: " + captions_string + "\n")
  music_preference = genre
  artist_prefered = artist

  client_prompt = f"Based on the provided information, the photo is associated with these tags: {tags_string}, and includes the following captions: {captions_string}. Please recommend a song that complements the mood, theme, or story conveyed by the photo. Consider the following preferences: music style/genre: {music_preference}, and preferred artist: {artist_prefered}. Additionally, identify which specific part of the song (e.g., verse, chorus, bridge) best aligns with the photo's essence and explain why it fits"


  client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01"
  )

  response = client.chat.completions.create(
      model="gpt-35-turbo", # model = "deployment_name".
      messages=[
          {"role": "system", "content": "You are a music assistant helping to suggest music to complement images for an instagram post."},
          {"role": "user", "content": client_prompt}
      ]
  )

  print(response.choices[0].message.content)
  return(response.choices[0].message.content)


if __name__ == "__main__":
    genre = "Pop"
    artist = "SZA"
    main(genre, artist)