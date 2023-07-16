import re
import os
import requests
from bs4 import BeautifulSoup

def extract_media_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    media_urls = []

    # Regular expression to match media URLs (images and videos)
    media_regex = r'(https?://(?:www\.)?[^<>]*?\.(?:jpg|jpeg|gif|png|bmp|svg|webp|mp4|webm))'

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        matches = re.findall(media_regex, href)
        media_urls.extend(matches)

    return media_urls

def download_files(urls, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for url in urls:
        file_name = os.path.join(download_folder, os.path.basename(url))
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {url}")

if __name__ == "__main__":
    file_path = 'html_files/keren.html' # Ganti dengan path file HTML yang memiliki media URLs dan ingin di-download
    download_folder = 'hasil_download' # Ganti dengan nama folder tempat menyimpan file yang didownload
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        media_urls = extract_media_urls(html_content)
        download_files(media_urls, download_folder)
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
