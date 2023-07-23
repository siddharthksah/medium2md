import subprocess, os, shutil
from download_with_media import download_medium_article
from html_to_md import convert_html_to_markdown
from clean_md import process_markdown_files
from url_to_local import url2local

article_url = "https://siddharthksah.medium.com/synthetic-training-data-object-detection-with-transfer-learning-deep-learning-on-steroids-e20f76bd4269"
output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")


download_medium_article(article_url)
convert_html_to_markdown(output_folder)
process_markdown_files(output_folder)
url2local()

# remove the media folder inside the output folder
media_folder = os.path.join(output_folder, "media")
if os.path.exists(media_folder):
    shutil.rmtree(media_folder)

print("Done!")



