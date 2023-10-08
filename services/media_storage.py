import io
import requests
from constants.GC import GC
from bs4 import BeautifulSoup
import re
import os
import boto3
import botocore
import base64
from models.file import File
import time
from beanie import operators
from PIL import Image

class MediaStorage:

    aws_access_key_id = GC.S3_ACCESS_KEY
    aws_secret_access_key = GC.S3_SECRET_KEY
    bucket_name = GC.S3_BUCKET_NAME
    web3_token = GC.WEB3
    folder_name = GC.S3_UPLOAD_FOLDER_NAME

    s3 = boto3.client('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

    @classmethod
    def fetch_data_from_web3(cls, cid):
        files_to_upload = []
        url = f"https://{cid}.ipfs.dweb.link"
        url = f"https://api.web3.storage/car/{cid}"
        headers = {
            "Authorization": f"Bearer {cls.web3_token}"
        }
        try:
            # Send a GET request to fetch the file
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # The content of the file is in the response's content attribute
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all anchor elements on the webpage (e.g., <a href="image.jpg">)
                anchor_tags = soup.find_all('a', href=True)

                # Extract the 'href' attributes that point to images
                image_links = [os.path.basename(tag['href']) for tag in anchor_tags if ('ipfs-hash' not in tag.get("class", []) and re.search(r'\.(jpg|jpeg|png|gif|bmp|svg)$', tag['href'], re.IGNORECASE))]
                # print(image_links)
                # Print the image links
                for link in image_links:
                    url = os.path.join(f"https://{cid}.ipfs.dweb.link", url)
                    files_to_upload.append(url)
                return files_to_upload
            else:
                print(f"Failed to fetch file from Web3.Storage. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    @classmethod
    def fetch_media_from_web3(cls, url, cid)->list:
        headers = {
            "Authorization": f"Bearer {cls.web3_token}"
        }
        file_name = url
        url = os.path.join(f"https://{cid}.ipfs.dweb.link", url)
        print(url)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                image_content = response.content
                with open(file_name, 'wb') as file:
                    file.write(image_content)
        except Exception as e:
            print(f"Error: {e}")
            return None
    @classmethod
    async def fileio_to_s3(cls, file_object_ids):
        print("file objs from db")
        file_objects = await cls.file_objs_from_db(file_object_ids)
        print("fetch media from fileio")
        image_objects = cls.fetch_media_from_fileio(file_objects)
        processed_image_objects = dict()
        for file_object in file_objects:
            processed_image_objects[file_object.id] = [file_object, cls.process_media(image_objects[file_object.id][1])]
        print("upload files")
        file_objects = cls.upload_files(processed_image_objects)
        print("update file objects")
        cls.update_file_objects(file_objects)

    @classmethod
    async def file_objs_from_db(cls, file_object_ids):
        # filters = [File.get(id) for id in file_object_ids]
        # file_objects = File.get_all(*filters).to_list()
        file_objects = await File.find(operators.In(File.id, file_object_ids)).to_list()
        return file_objects
        
    @classmethod
    def fetch_media_from_fileio(cls, file_objects):
        image_objects = dict()
        for file_object in file_objects:
            url = file_object.temp_link
            response = requests.request("GET", url)
            if response.status_code == 200:
                image_objects[file_object.id] = [file_object, response.content]
        return image_objects
  
    @classmethod
    def process_media(cls, content):
        return content
        webp_image_bytes = io.BytesIO()
        image = Image.frombuffer(content)
        image.save(webp_image_bytes, format='WEBP')

        # Get the WebP image bytes as a string
        webp_image_string = webp_image_bytes.getvalue()

        # Close the WebP image bytes
        webp_image_bytes.close()

        # Return the WebP image string
        return webp_image_string
    
    @classmethod
    def upload_files(cls, file_objects):
        for file_id in file_objects.keys():
            try:
                s3_object_key = f'{cls.folder_name}/{time.time()}_{file_objects[file_id][0].name}.webp'

                # Upload the image content to the specified S3 bucket and object key
                cls.s3.upload_fileobj(
                    Fileobj=io.BytesIO(file_objects[file_id][1]),
                    Bucket=cls.bucket_name,
                    Key=s3_object_key
                )

                print(f"Image '{s3_object_key}' uploaded to S3 bucket '{cls.bucket_name}' successfully.")
                file_objects[file_id][1] = s3_object_key
            except botocore.exceptions.NoCredentialsError:
                print("AWS credentials are not properly configured.")
            except Exception as e:
                print(f"An error occurred: {e}") #### Throw error in console
        return file_objects
    
    @classmethod
    def update_file_objects(file_objects):
        pass
