import os
import shutil
import requests
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright


def download_medium_article(article_url, output_folder):
    """Download a Medium article and its associated media files.

    Args:
        article_url (str): URL of the Medium article.

    Returns:
        bool: True if the article and media files were downloaded successfully, False otherwise.
    """
    def get_page_content_and_media_urls(url):
        """Fetches the page content and media urls from a given url.

        Args:
            url (str): url of the webpage.

        Returns:
            tuple: page content and list of media urls.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.route("**", lambda route, request: route.continue_())
            page.goto(url)
            page.wait_for_load_state()
            page_content = page.content()
            browser.close()

        soup = BeautifulSoup(page_content, 'html.parser')
        media_urls = [urljoin(url, img['src']) for img in soup.find_all('img')]

        return page_content, media_urls

    try:
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        page_content, media_urls = get_page_content_and_media_urls(article_url)

        response = requests.get(article_url)
        response.raise_for_status()

        doc = Document(response.text)
        article_title = doc.title()
        article_content = doc.summary()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        media_folder = os.path.join(output_folder, "media")
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)

        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

        media_files = {}
        for idx, media_url in enumerate(media_urls):
            media_extension = os.path.splitext(media_url.split("/")[-1])[1]
            media_filename = f"media_{idx+1}{media_extension}"
            media_file = os.path.join(media_folder, media_filename)
            if media_extension.lower() in valid_image_extensions:
                try:
                    response = requests.get(media_url, stream=True)
                    response.raise_for_status()
                    with open(media_file, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response
                    media_files[media_filename] = media_url
                except Exception as e:
                    print(f"Could not download: {media_url}")
                    print(f"Error: {e}")

        for img in BeautifulSoup(article_content, 'html.parser').find_all('img'):
            img_src = img['src']
            for media_filename, media_url in media_files.items():
                if media_url == urljoin(article_url, img_src):
                    img['src'] = f"./media/{media_filename}"
                    break

        markdown_file = os.path.join(output_folder, f"{article_title}.md")
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
            f.write("\n\n")
            f.write("# " + article_title + "\n\n")
            f.write(article_content)

        # print("Medium article downloaded successfully!")
        # print(f"Article saved as: {markdown_file}")
        # print(f"Media files saved in: {media_folder}")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    


# if __name__ == "__main__":
#     article_url = "https://siddharthksah.medium.com/synthetic-data-test-article-727e1f8ac2cb"
#     download_successful = download_medium_article(article_url)
#     if download_successful:
#         print("Download successful!")
#     else:
#         print("Download failed.")