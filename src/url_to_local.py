import os
import re
import requests
import glob
import shutil


def download_image(url, output_folder):
    """
    Download an image from a URL.

    Args:
        url (str): The URL of the image to be downloaded.
        output_folder (str): The directory where the image will be saved.

    Returns:
        str: The local path to the image if the download was successful, otherwise None.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # If the request was successful, save the image
    if response.status_code == 200:
        image_name = os.path.basename(url)
        image_path = os.path.join(output_folder, "local", image_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path

    return None


def update_image_links_in_markdown(markdown_content, output_folder):
    """
    Update the image links in the markdown content to point to their local versions.

    Args:
        markdown_content (str): The markdown content to be updated.
        output_folder (str): The directory where the images are saved.

    Returns:
        str: The updated markdown content.
        list: A list of the local paths to the images.
    """
    # Regex pattern to find all image links in the markdown content
    pattern = r"!\[\]\((https?://.+?\.(?:jpg|jpeg|png|gif))\)"

    # Find all image URLs in the markdown content
    image_urls = re.findall(pattern, markdown_content)

    # For each image URL, download the image and update the link
    local_image_paths = []
    for url in image_urls:
        local_image_path = download_image(url, output_folder)
        if local_image_path:
            local_image_paths.append(local_image_path)
            markdown_content = markdown_content.replace(url, os.path.relpath(local_image_path, output_folder))

    return markdown_content, local_image_paths


def url_to_local():
    """
    Download all images linked in a markdown file and replace the links with local paths.

    Returns:
        None
    """
    # Define the output directory
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all markdown files in the output directory
    input_files = glob.glob(os.path.join(output_folder, "*.md"))

    # If there are no markdown files or more than one, print an error message
    if not input_files:
        print("No markdown files found in the output folder.")
    elif len(input_files) > 1:
        print("More than one markdown file found in the output folder. Please ensure there's only one.")
    else:
        input_file_path = input_files[0]

        # Create a directory for the local images
        local_folder = os.path.join(output_folder, "local")
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        # Open the markdown file, download all images and update the links
        with open(input_file_path, 'r') as f:
            markdown_content = f.read()

        updated_content, local_image_paths = update_image_links_in_markdown(markdown_content, output_folder)

        # Save the updated markdown content
        with open(input_file_path, 'w') as f:
            f.write(updated_content)

        # print("Images downloaded and markdown file updated successfully.")


# if __name__ == "__main__":
#     url2local()
