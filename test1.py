import os
import azure.ai.vision
import azure.ai.vision.imageanalysis 

# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
endpoint = os.environ["VISION_ENDPOINT"]
key = os.environ["VISION_KEY"]

def analyze_image(image_url):
    client = azure.ai.vision.imageanalysis.ImageAnalysisClient(endpoint, key)
    analysis_options = VisionAnalysisOptions(features=["Description", "Objects", "Tags", "OCR"])
    result = client.analyze_image_url(image_url, analysis_options)
    
    return result.to_dict()