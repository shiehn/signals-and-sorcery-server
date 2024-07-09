import os
import uuid
import requests
import logging
from game_engine.cdn.file_uploader import FileUploader
from openai import OpenAI
import asyncio

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class AssetGenerator:
    def __init__(self, open_ai_key):
        self.client = OpenAI(api_key=open_ai_key)
        self.file_uploader = FileUploader()

    async def generate_riddle(self, password: str, setting_and_lore: str) -> str:
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-3.5-turbo-0125",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a content creator for a fantasy RPG. You generate straightforward clues, hints, and riddles for players to solve for a password.",
                    },
                    {
                        "role": "user",
                        "content": f"The password is {password}, please generate a simple clue, hint, or riddle that could be found in this fantasy settings: {setting_and_lore}.",
                    },
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating description asset: {e}")
            return "Error generating asset description "

    async def generate_description(self, type: str, aesthetic: str) -> str:
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-3.5-turbo-0125",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a content creator for a chat-based fantasy RPG. Your role is generate short descriptions based on the specified item detials and aesthetic guidelines.",
                    },
                    {
                        "role": "user",
                        "content": f"Creat a brief description of a {type} based on the following aesthetic guidelines and details: {aesthetic}",
                    },
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating description asset: {e}")
            return "Error generating asset description "

    async def generate_image(self, type: str, aesthetic: str) -> str:
        try:
            # Generate the image and get temporary URL
            response = await asyncio.to_thread(
                self.client.images.generate,
                model="dall-e-3",
                prompt=f"Generate an image for a {type} based on the following aesthetic guidelines and details: {aesthetic}",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            temp_url = response.data[0].url

            rand_img_name = str(uuid.uuid4())
            # Download the image from the temporary URL
            local_file_path = await self.download_file(temp_url, rand_img_name)

            # Upload the file to GCP
            file_url = await asyncio.to_thread(
                self.file_uploader.upload, local_file_path, "image/png"
            )  # Assuming PNG, change accordingly

            # Delete the local file after uploading
            os.remove(local_file_path)

            return file_url
        except Exception as e:
            logger.error(f"Error generating image asset: {e}")
            return (
                "https://storage.googleapis.com/byoc-file-transfer/img_placeholder.png"
            )

    async def download_file(self, url, img_description):
        local_filename = (
            f"{img_description.replace(' ', '_')}.png"  # Generate a safe filename
        )
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            with open(local_filename, "wb") as f:
                f.write(response.content)
            return local_filename
        else:
            raise Exception("Failed to download image from temporary URL")
