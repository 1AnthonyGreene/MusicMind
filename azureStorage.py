from azure.storage.blob import BlobServiceClient
import os

# Environment variables for Azure connection string and container name
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

def upload_images(folder_path):
    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Walk through the folder and upload each file
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)  # Full local file path
            blob_name = os.path.relpath(file_path, folder_path)  # Blob name relative to the folder

            try:
                # Create a BlobClient for the specific file
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

                # Open the file in binary mode and upload its contents
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)  # Overwrite=True ensures idempotent uploads

                print(f"Uploaded: {blob_name}")
            except Exception as e:
                print(f"Failed to upload {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    folder_path = "static/files"  # Path to the folder containing files to upload
    upload_images(folder_path)
