import os
import re
import requests
import glob

def download_image(url, output_folder):
    response = requests.get(url)
    if response.status_code == 200:
        image_name = os.path.basename(url)
        image_path = os.path.join(output_folder, "local", image_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    else:
        return None

def update_image_links_in_markdown(markdown_content, output_folder):
    pattern = r"!\[\]\((https?://.+?\.(?:jpg|jpeg|png|gif))\)"
    image_urls = re.findall(pattern, markdown_content)

    local_image_paths = []
    for url in image_urls:
        local_image_path = download_image(url, output_folder)
        if local_image_path:
            local_image_paths.append(local_image_path)
            markdown_content = markdown_content.replace(url, os.path.relpath(local_image_path, output_folder))

    return markdown_content, local_image_paths

if __name__ == "__main__":
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = glob.glob(os.path.join(output_folder, "*.md"))

    if not input_files:
        print("No markdown files found in the output folder.")
    elif len(input_files) > 1:
        print("More than one markdown file found in the output folder. Please ensure there's only one.")
    else:
        input_file_path = input_files[0]

        local_folder = os.path.join(output_folder, "local")
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        with open(input_file_path, 'r') as f:
            markdown_content = f.read()

        updated_content, local_image_paths = update_image_links_in_markdown(markdown_content, output_folder)

        with open(input_file_path, 'w') as f:
            f.write(updated_content)

        print("Images downloaded and markdown file updated successfully.")
