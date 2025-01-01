import os
import azureStorage
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

class ImageAnalyzer:
    def __init__(self, endpoint: str, key: str):
        """Initialize the ImageAnalyzer with the given Azure endpoint and key."""
        self.endpoint = endpoint
        self.key = key
        self.client = ImageAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    def analyze_image(self, image_url: str):
        """Analyze the image using the provided URL and return the result."""
        result = self.client.analyze_from_url(
            image_url=image_url,
            visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.READ],
            gender_neutral_caption=True  # Optional (default is False)
        )
        return result

    def print_caption(self, result):
        """Print the caption from the result."""
        print(" Caption:")
        if result.caption is not None:
            print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")
        else:
            print("No caption detected")

    def print_tags(self, result):
        """Print the tags and their confidence levels from the result."""
        print(" Tags:")
        if 'tagsResult' in result and 'values' in result['tagsResult']:
            for tag in result['tagsResult']['values']:
                # Check if the tag has the expected attributes
                if 'name' in tag and 'confidence' in tag:
                    print(f"   Tag: {tag['name']}, Confidence: {tag['confidence']:.2f}")
                else:
                    print(f"   Tag detected but missing expected attributes: {tag}")
        else:
            print("No tags detected")

    def print_read(self, result):
        """Print the text (OCR) analysis from the result."""
        print(" Read:")
        if result.read is not None:
            try:
                for block in result.read.blocks:
                    for line in block.lines:
                        print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
                        for word in line.words:
                            print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")
            except AttributeError:
                print("Nothing to read")
        else:
            print("No text detected")


# Main code execution
def main():
    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()
    image_urls = []
    storage = azureStorage()

    print(storage.get_upload_images("static\files"))
    
    """folder_path = "static/files"
    for root, dirs, files in os.walk(folder_path): 
        for file in files:
            file_path = os.path.join(root, file)
            image_urls.append(file_path)
    """
    results = []

    image_analyzer = ImageAnalyzer(endpoint, key)

    # Analyze image
    #image_url = "https://musicmindstorage.blob.core.windows.net/instacontainer/IMG_2930.jpeg"
    #result = image_analyzer.analyze_image(image_url)

    
    for image_url in image_urls:
        result = image_analyzer.analyze_image(image_url)
        results.append(result)
       #image_analyzer.print_tags(result)
    
    """
    # Print the results
    print("Raw response:")
    print(result)

    image_analyzer.print_caption(result)
    image_analyzer.print_tags(result)
    image_analyzer.print_read(result)
    """
    #print(results)
    return results

  
def add_caption():
    mainResults = main()
    captions = []
    try:
        if mainResults.caption is not None:
                    captions.append(mainResults.caption.text)
        else:
                    print("No caption detected")
    except:
        pass
    return captions

def add_tags():
    mainResults = main()
    tags = []
    try:
        for result in mainResults:
            if 'tagsResult' in result and 'values' in result['tagsResult']:
                for tag in result['tagsResult']['values']:
                    # Check if the tag has the expected attributes
                    if (tag['name'] not in tags):
                       tags.append(tag['name'])
                    else:
                        pass
            else:
                print("No tags detected")
    except:
        pass
    return tags
    




if __name__ == "__main__":
    main()