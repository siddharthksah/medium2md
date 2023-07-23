import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from readability import Document

def download_medium_article(url, output_folder):
    # Send a GET request to the Medium article URL
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content using readability-lxml
    doc = Document(response.text)
    article_title = doc.title()
    article_content = doc.summary()

    # Convert the article content to Markdown format
    markdown_content = markdownify(article_content)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the article markdown locally
    markdown_file = os.path.join(output_folder, f"{article_title}.md")
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    # Download and save media files (images) inside the asset folder
    media_elements = BeautifulSoup(article_content, 'html.parser').find_all('img')
    asset_folder = os.path.join(output_folder, "assets")
    if media_elements:
        if not os.path.exists(asset_folder):
            os.makedirs(asset_folder)
        for idx, element in enumerate(media_elements):
            media_url = element['src']
            response = requests.get(media_url)
            response.raise_for_status()
            media_extension = os.path.splitext(media_url.split("/")[-1])[1]
            media_filename = f"media_{idx+1}{media_extension}"
            media_file = os.path.join(asset_folder, media_filename)
            with open(media_file, 'wb') as f:
                f.write(response.content)

    print("Medium article downloaded successfully!")
    print(f"Article saved as: {markdown_file}")
    if media_elements:
        print(f"Media files saved in: {asset_folder}")

if __name__ == "__main__":
    article_url = "https://siddharthksah.medium.com/synthetic-data-test-article-727e1f8ac2cb"
    output_folder = "output"
    download_medium_article(article_url, output_folder)
