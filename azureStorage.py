from azure.storage.blob import BlobServiceClient, ContentSettings
import os

# Environment variables for Azure connection string and container name

def get_type(file):
    if ".jpeg" or ".jpg" in file:
        return "image/jpeg"
    elif ".png" in file:
        return "image/png"
    elif ".gif" in file: 
        return "image/gif"
    elif ".bmp" in file: 
        return "image/bmp"
    else:
        return "application/octet-stream"
    

def get_upload_images(file_path, file_name):
    CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    uploaded_urls = []

    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_service_client.get_container_client
    # Walk through the folder and upload each file

    
    try:
                # Create a BlobClient for the specific file
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        content_type = get_type(file_path)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(
                data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
                # Open the file in binary mode and upload its contents

        uploaded_urls.append(blob_client.url)

    except Exception as e:
        print(f"Failed to upload {file_name}: {e}")
    return uploaded_urls

# Example usage
if __name__ == "__main__":
    folder_path = "static/files"  # Path to the folder containing files to upload
    get_upload_images(folder_path)
