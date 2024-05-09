import os
import uuid

import requests
from game_engine.cdn.file_uploader import FileUploader
from openai import OpenAI


class AssetGenerator:
    def __init__(self, open_ai_key):
        self.open_ai_key = open_ai_key
        self.client = OpenAI()
        self.file_uploader = FileUploader()

    def generate_image(self, img_description) -> str:
        # Generate the image and get temporary URL
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=img_description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        temp_url = response.data[0].url

        rand_img_name = str(uuid.uuid4())
        # Download the image from the temporary URL
        local_file_path = self.download_file(temp_url, rand_img_name)

        # Upload the file to GCP
        file_url = self.file_uploader.upload(
            local_file_path, "image/png"
        )  # Assuming PNG, change accordingly

        # Delete the local file after uploading
        os.remove(local_file_path)

        return file_url

    def download_file(self, url, img_description):
        local_filename = (
            f"{img_description.replace(' ', '_')}.png"  # Generate a safe filename
        )
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_filename, "wb") as f:
                f.write(response.content)
            return local_filename
        else:
            raise Exception("Failed to download image from temporary URL")
