import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from readability import Document
import re
from urllib.parse import urljoin

def download_medium_article(url, output_folder):
    # Send a GET request to the Medium article URL
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content using readability-lxml
    doc = Document(response.text)
    article_title = doc.title()
    article_content = doc.summary()

    # Find all the media URLs in the article
    soup = BeautifulSoup(article_content, 'html.parser')
    media_urls = [urljoin(url, img['src']) for img in soup.find_all('img')]

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the media folder inside the output folder
    media_folder = os.path.join(output_folder, "media")
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    # Download and save media files in the media folder
    for idx, media_url in enumerate(media_urls):
        response = requests.get(media_url)
        response.raise_for_status()
        media_extension = os.path.splitext(media_url.split("/")[-1])[1]
        media_filename = f"media_{idx+1}{media_extension}"
        media_file = os.path.join(media_folder, media_filename)
        with open(media_file, 'wb') as media_f:
            media_f.write(response.content)

    # Replace image URLs in the article content with relative paths to the media folder
    for idx, img in enumerate(soup.find_all('img')):
        img['src'] = f"./media/media_{idx+1}{os.path.splitext(img['src'])[1]}"

    # Convert the article content to Markdown format
    markdown_content = markdownify(str(soup))

    # Save the article markdown locally
    markdown_file = os.path.join(output_folder, f"{article_title}.md")
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print("Medium article downloaded successfully!")
    print(f"Article saved as: {markdown_file}")
    print(f"Media files saved in: {media_folder}")

if __name__ == "__main__":
    article_url = "https://siddharthksah.medium.com/a-sorta-kinda-hitchhikers-guide-to-synthetic-data-ad722798af63"
    output_folder = "output"
    download_medium_article(article_url, output_folder)
