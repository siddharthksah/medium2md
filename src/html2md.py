# import os
# import html2text

# # Get the output folder's path
# output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

# # Get all files in the output directory
# all_files = os.listdir(output_folder)

# # Filter all .md files
# markdown_files = [file for file in all_files if file.endswith('.md')]

# # Create an html2text object
# h = html2text.HTML2Text()
# # Ignore converting links from HTML
# h.ignore_links = True

# for md_file in markdown_files:
#     md_file_path = os.path.join(output_folder, md_file)

#     # Open and read the HTML file
#     with open(md_file_path, 'r') as f:
#         html_content = f.read()

#     # Convert the HTML to Markdown
#     markdown_content = h.handle(html_content)

#     # Open and write into the Markdown file
#     with open(md_file_path, 'w') as f:
#         f.write(markdown_content)

# print("Conversion to Markdown is complete.")

import os
import html2text

def convert_html_to_markdown(output_folder):
    # Get all files in the output directory
    all_files = os.listdir(output_folder)

    # Filter all .md files
    markdown_files = [file for file in all_files if file.endswith('.md')]

    # Create an html2text object
    h = html2text.HTML2Text()
    # Ignore converting links from HTML
    h.ignore_links = True

    for md_file in markdown_files:
        md_file_path = os.path.join(output_folder, md_file)

        # Open and read the HTML file
        with open(md_file_path, 'r') as f:
            html_content = f.read()

        # Convert the HTML to Markdown
        markdown_content = h.handle(html_content)

        # Open and write into the Markdown file
        with open(md_file_path, 'w') as f:
            f.write(markdown_content)

    print("Conversion to Markdown is complete.")

# if __name__ == "__main__":
#     # Get the output folder's path
#     output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

#     convert_html_to_markdown(output_folder)

