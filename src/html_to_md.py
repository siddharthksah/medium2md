import os
import html2text


def convert_html_to_markdown(output_folder):
    """
    Convert HTML files in the output folder to markdown format.

    Args:
        output_folder (str): The path to the output folder containing the HTML files.

    Returns:
        None
    """
    # Get a list of all files in the output directory.
    all_files = os.listdir(output_folder)

    # Filter out the list to only have .md files.
    markdown_files = [file for file in all_files if file.endswith('.md')]

    # Initialize html2text converter.
    h = html2text.HTML2Text()
    # Configure html2text to ignore converting links from HTML.
    h.ignore_links = True

    # Loop over each .md file and convert its contents from HTML to markdown.
    for md_file in markdown_files:
        # Construct the full file path by joining the file name with the output directory path.
        md_file_path = os.path.join(output_folder, md_file)

        # Open the markdown file in read mode and read its HTML content.
        with open(md_file_path, 'r') as f:
            html_content = f.read()

        # Convert the HTML content to markdown.
        markdown_content = h.handle(html_content)

        # Open the markdown file in write mode and overwrite it with the markdown content.
        with open(md_file_path, 'w') as f:
            f.write(markdown_content)

    # print("Conversion to Markdown is complete.")


# if __name__ == "__main__":
#     # Construct the output folder's path.
#     output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

#     # Invoke the HTML to markdown conversion function.
#     convert_html_to_markdown(output_folder)
