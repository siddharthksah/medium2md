# import os
# import requests
# from bs4 import BeautifulSoup
# from readability import Document
# import shutil
# from urllib.parse import urljoin
# from playwright.sync_api import sync_playwright

# def get_media_urls(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         # Limit playwright to capture network requests only during the initial page load
#         page.route("**", lambda route, request: route.continue_())
#         page.goto(url)
#         page.wait_for_load_state()
#         page_content = page.content()
#         browser.close()

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(page_content, 'html.parser')
#     media_urls = [urljoin(url, img['src']) for img in soup.find_all('img')]

#     return page_content, media_urls

# def download_medium_article(url, output_folder):
#     # Get the page content and media URLs using playwright
#     page_content, media_urls = get_media_urls(url)

#     if not media_urls:
#         print("No media found in the article.")
#         return

#     # Send a GET request to the Medium article URL
#     response = requests.get(url)
#     response.raise_for_status()

#     # Parse the HTML content using readability-lxml
#     doc = Document(response.text)
#     article_title = doc.title()
#     article_content = doc.summary()

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Create the media folder inside the output folder
#     media_folder = os.path.join(output_folder, "media")
#     if not os.path.exists(media_folder):
#         os.makedirs(media_folder)

#     # List of valid image extensions
#     valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

#     # Download and save media files in the media folder
#     media_files = {}
#     for idx, media_url in enumerate(media_urls):
#         media_extension = os.path.splitext(media_url.split("/")[-1])[1]
#         media_filename = f"media_{idx+1}{media_extension}"
#         media_file = os.path.join(media_folder, media_filename)
#         if media_extension.lower() in valid_image_extensions:
#             try:
#                 response = requests.get(media_url, stream=True)
#                 response.raise_for_status()
#                 with open(media_file, 'wb') as out_file:
#                     shutil.copyfileobj(response.raw, out_file)
#                 del response
#                 # Add the media file and its URL to the dictionary
#                 media_files[media_filename] = media_url
#             except Exception as e:
#                 print(f"Could not download: {media_url}")
#                 print(f"Error: {e}")

#     # Replace image URLs in the article content with proper image tags
#     for img in BeautifulSoup(article_content, 'html.parser').find_all('img'):
#         img_src = img['src']
#         for media_filename, media_url in media_files.items():
#             if media_url == urljoin(url, img_src):
#                 img['src'] = f"./media/{media_filename}"
#                 break

#     # Save the article markdown locally
#     markdown_file = os.path.join(output_folder, f"{article_title}.md")
#     with open(markdown_file, 'w', encoding='utf-8') as f:
#         # Write the images in the original HTML format
#         f.write(page_content)

#         # Write the remaining text as the article content
#         f.write("\n\n")
#         f.write("# " + article_title + "\n\n")
#         f.write(article_content)

#     print("Medium article downloaded successfully!")
#     print(f"Article saved as: {markdown_file}")
#     print(f"Media files saved in: {media_folder}")

#     return article_title

# if __name__ == "__main__":
#     # article_url = "https://siddharthksah.medium.com/synthetic-data-test-article-727e1f8ac2cb"

#     # article_url = "https://siddharthksah.medium.com/a-sorta-kinda-hitchhikers-guide-to-synthetic-data-ad722798af63"
#     # article_url = "https://siddharthksah.medium.com/real-time-object-tracking-and-segmentation-using-yolov8-with-strongsort-ocsort-and-bytetrack-180eef43354a"
#     # article_url = "https://medium.com/@tenyks_blogger/top-4-computer-vision-problems-solutions-in-agriculture-data-part-2-4eff7010a61e"
    
#     # article_url = "https://siddharthksah.medium.com/synthetic-training-data-object-detection-with-transfer-learning-deep-learning-on-steroids-e20f76bd4269"
    
#     # article_url = "https://medium.com/geekculture/the-5-paid-subscriptions-i-actually-use-in-2023-as-a-software-engineer-9418515a315a"
    
#     output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

#     # Delete the old output folder if it exists
#     if os.path.exists(output_folder):
#         shutil.rmtree(output_folder)

#     article_title = download_medium_article(article_url, output_folder)

import os
import requests
from bs4 import BeautifulSoup
from readability import Document
import shutil
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

def download_medium_article(article_url):
    def get_media_urls(url):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Limit playwright to capture network requests only during the initial page load
            page.route("**", lambda route, request: route.continue_())
            page.goto(url)
            page.wait_for_load_state()
            page_content = page.content()
            browser.close()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')
        media_urls = [urljoin(url, img['src']) for img in soup.find_all('img')]

        return page_content, media_urls

    try:
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

        # Delete the old output folder if it exists
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        # Get the page content and media URLs using playwright
        page_content, media_urls = get_media_urls(article_url)

        if not media_urls:
            print("No media found in the article.")
            return False

        # Send a GET request to the Medium article URL
        response = requests.get(article_url)
        response.raise_for_status()

        # Parse the HTML content using readability-lxml
        doc = Document(response.text)
        article_title = doc.title()
        article_content = doc.summary()

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Create the media folder inside the output folder
        media_folder = os.path.join(output_folder, "media")
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)

        # List of valid image extensions
        valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

        # Download and save media files in the media folder
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
                    # Add the media file and its URL to the dictionary
                    media_files[media_filename] = media_url
                except Exception as e:
                    print(f"Could not download: {media_url}")
                    print(f"Error: {e}")

        # Replace image URLs in the article content with proper image tags
        for img in BeautifulSoup(article_content, 'html.parser').find_all('img'):
            img_src = img['src']
            for media_filename, media_url in media_files.items():
                if media_url == urljoin(article_url, img_src):
                    img['src'] = f"./media/{media_filename}"
                    break

        # Save the article markdown locally
        markdown_file = os.path.join(output_folder, f"{article_title}.md")
        with open(markdown_file, 'w', encoding='utf-8') as f:
            # Write the images in the original HTML format
            f.write(page_content)

            # Write the remaining text as the article content
            f.write("\n\n")
            f.write("# " + article_title + "\n\n")
            f.write(article_content)

        print("Medium article downloaded successfully!")
        print(f"Article saved as: {markdown_file}")
        print(f"Media files saved in: {media_folder}")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# if __name__ == "__main__":
#     # Provide the article URL as an input here
#     article_url = "https://siddharthksah.medium.com/synthetic-data-test-article-727e1f8ac2cb"

#     download_successful = download_medium_article(article_url)
#     if download_successful:
#         print("Download successful!")
#     else:
#         print("Download failed.")
