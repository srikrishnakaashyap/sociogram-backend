import requests
from constants.GC import GC
from bs4 import BeautifulSoup
import re
import os

class MediaStorage:

    def create_link(cid):
        return f"https://{cid}.ipfs.dweb.link"

    def fetch_media(url, cid):
        headers = {
            "Authorization": f"Bearer {GC.WEB3}"
        }
        if re.search(r'\.(jpg|jpeg|png|gif|bmp|svg)$', url, re.IGNORECASE):
            file_name = url
            url = os.path.join(MediaStorage.create_link(cid), url)
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
        else:
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
                    for link in image_links[::-1]:
                        MediaStorage.fetch_media(link, cid)                  
                    else:
                        print(f"Failed to fetch file from Web3.Storage. Status code: {response.status_code}")
                        return None
            except Exception as e:
                print(f"Error: {e}")
                return None