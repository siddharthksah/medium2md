import re
import os

def clean_markdown_file(filepath):
    # Define the regex patterns for the sections to be removed
    section_patterns = [
        re.compile(r"(?s)More from.*", re.MULTILINE),
        re.compile(r"(?s)Recommended.*", re.MULTILINE),
        re.compile(r"(?s)\<header.*header\>", re.MULTILINE),  # Removes the Medium header
        re.compile(r"(?s)\<nav.*nav\>", re.MULTILINE),  # Removes the Medium navigation bar
        re.compile(r"\n.*?Share", re.DOTALL),  # Removes everything from the second line to the word "Share"
    ]

    # Read the content of the markdown file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove unwanted sections from the content
    for pattern in section_patterns:
        content = pattern.sub('', content)

    # Find the last occurrence of "https://miro.medium.com" and remove everything after it
    last_occurrence_index = content.rfind('https://miro.medium.com')
    if last_occurrence_index != -1:  # If found
        line_start_index = content.rfind('\n', 0, last_occurrence_index)
        content = content[:line_start_index]

    # Split content by lines
    lines = content.split('\n')

    # Exclude the last 5 lines
    content = '\n'.join(lines[:-5])

    # Write the cleaned content back to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # Assume the markdown file is located in the output directory
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

    # Get all markdown files in the output directory
    markdown_files = [f for f in os.listdir(output_folder) if f.endswith('.md')]

    for markdown_file in markdown_files:
        # Get the absolute path of the markdown file
        markdown_file_path = os.path.join(output_folder, markdown_file)
        # Clean the markdown file
        clean_markdown_file(markdown_file_path)

    print("Cleaned markdown files successfully!")
