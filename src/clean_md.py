import re
import os
from typing import List

def list_markdown_files(folder_path: str) -> List[str]:
    """
    List all markdown files in a directory.

    :param folder_path: Path to the directory
    :return: List of markdown files
    """
    return [file for file in os.listdir(folder_path) if file.endswith('.md')]

def process_markdown_files(folder_path: str):
    """
    Process all markdown files in a directory.

    :param folder_path: Path to the directory
    """
    # Get all markdown files in the directory
    markdown_files = list_markdown_files(folder_path)

    # Process each markdown file
    for md_file in markdown_files:
        file_path = os.path.join(folder_path, md_file)
        process_single_file(file_path)

def process_single_file(file_path: str):
    """
    Apply transformations to a single markdown file.

    :param file_path: Path to the markdown file
    """
    # Extract the first heading and the line that follows
    heading = extract_first_heading_and_next_line(file_path)

    # Remove sections from the markdown
    remove_section_after(file_path, "## More from")
    remove_until(file_path, "Share")

    # Add the extracted heading at the beginning of the file
    add_heading(file_path, heading)

    # Remove another section
    remove_section_after(file_path, "## Written by")

    # Delete lines after a certain pattern
    last_pattern_line_number = find_last_line_containing(file_path, "\\--")
    if last_pattern_line_number is not None:
        delete_lines_from(file_path, last_pattern_line_number)

    # Remove final section
    remove_section_after(file_path, "## Support independent authors and access the best of Medium.")

def extract_first_heading_and_next_line(file_path: str) -> str:
    """
    Extract the first heading and the line that follows from a markdown file.

    :param file_path: Path to the markdown file
    :return: Extracted heading and the line that follows it
    """
    with open(file_path, 'r') as file:
        file_text = file.read()

    pattern = r"^(#{1,6}) (.*$)\n(.*$)"
    match = re.search(pattern, file_text, re.MULTILINE)
    return ' '.join([match.group(2).strip(), match.group(3).strip()]) if match else None

def remove_section_after(file_path: str, heading: str):
    """
    Remove all content after a certain heading in a file.

    :param file_path: Path to the file
    :param heading: Heading after which content should be removed
    """
    with open(file_path, 'r') as file:
        file_text = file.read()

    pattern = f"{heading}.*"
    modified_text = re.sub(pattern, "", file_text, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(modified_text)

def remove_until(file_path: str, keyword: str):
    """
    Remove all content until a certain keyword in a file.

    :param file_path: Path to the file
    :param keyword: Keyword until which content should be removed
    """
    with open(file_path, 'r') as file:
        file_text = file.read()

    pattern = f".*{keyword}.*?\n"
    modified_text = re.sub(pattern, "", file_text, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(modified_text)

def add_heading(file_path: str, heading: str):
    """
    Add a heading at the beginning of a file.

    :param file_path: Path to the file
    :param heading: Heading to be added
    """
    with open(file_path, 'r+') as file:
        file_text = file.read()
        file.seek(0)
        file.write("# " + heading + "\n" + file_text)

def find_last_line_containing(file_path: str, pattern: str) -> int:
    """
    Find the last line in a file that contains a certain pattern.

    :param file_path: Path to the file
    :param pattern: Pattern to look for
    :return: Line number of the last occurrence of the pattern
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for num, line in enumerate(reversed(lines), 1):
        if pattern in line:
            return len(lines) - num + 1

    return None

def delete_lines_from(file_path: str, start_line: int):
    """
    Delete all lines starting from a certain line number in a file.

    :param file_path: Path to the file
    :param start_line: Line number from which to start deleting
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    del lines[start_line - 3:]

    with open(file_path, 'w') as file:
        file.writelines(lines)

# if __name__ == "__main__":
#     output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
#     process_markdown_files(output_folder)
