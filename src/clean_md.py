# import re
# import os

# output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
# markdown_files = [f for f in os.listdir(output_folder) if f.endswith(".md")]

# def extract_first_heading_and_next_line(file_path):
#     with open(file_path, 'r') as file:
#         md_text = file.read()
        
#     pattern = r"^(#{1,6}) (.*$)\n(.*$)"
#     match = re.search(pattern, md_text, re.MULTILINE)
#     if match:
#         return ' '.join([match.group(2).strip(), match.group(3).strip()])
#     else:
#         return None

# def remove_after_more_from(file_path):
#     with open(file_path, 'r') as file:
#         md_text = file.read()
#     pattern = r"## More from.*"
#     modified_text = re.sub(pattern, "", md_text, flags=re.DOTALL)
#     with open(file_path, 'w') as file:
#         file.write(modified_text)

# def remove_until_share(file_path):
#     with open(file_path, 'r') as file:
#         md_text = file.read()
#     pattern = r".*Share.*?\n"
#     modified_text = re.sub(pattern, "", md_text, flags=re.DOTALL)
#     with open(file_path, 'w') as file:
#         file.write(modified_text)

# def add_heading(file_path, heading):
#     with open(file_path, 'r+') as file:
#         md_text = file.read()
#         file.seek(0)
#         file.write("# " + heading + "\n" + md_text)

# def remove_after_written_by(file_path):
#     with open(file_path, 'r') as file:
#         md_text = file.read()

#     # Remove everything after and including "## Written by"
#     pattern = r"## Written by.*"
#     modified_text = re.sub(pattern, "", md_text, flags=re.DOTALL)

#     with open(file_path, 'w') as file:
#         file.write(modified_text)


# for md_file in markdown_files:
#     file_path = os.path.join(output_folder, md_file)
#     heading = extract_first_heading_and_next_line(file_path)
#     # print(heading)
#     remove_after_more_from(file_path)
#     remove_until_share(file_path)
#     add_heading(file_path, heading)
#     remove_after_written_by(file_path)

# def find_last_pattern_line_number(file_path, pattern):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     # Traverse the lines list in reverse order
#     for num, line in enumerate(reversed(lines), 1):
#         if pattern in line:
#             # Return the line number from the end
#             return len(lines) - num + 1
#     return None

# for md_file in markdown_files:
#     file_path = os.path.join(output_folder, md_file)
#     pattern_line_number = find_last_pattern_line_number(file_path, "\\--")
#     # print(f'Last pattern found at line {pattern_line_number}')

# def delete_lines_from(file_path, start_line):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     # Delete lines from start_line - 3 to the end
#     del lines[start_line - 3:]

#     with open(file_path, 'w') as file:
#         file.writelines(lines)

# for md_file in markdown_files:
#     file_path = os.path.join(output_folder, md_file)
#     pattern_line_number = find_last_pattern_line_number(file_path, "\\--")
#     try:
#         delete_lines_from(file_path, pattern_line_number)
#     except:
#         pass

# def remove_after_pattern(file_path, pattern):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     # Traverse the lines list in reverse order
#     for i, line in enumerate(reversed(lines)):
#         if line.startswith(pattern):
#             # Delete lines from this line number till the end
#             del lines[len(lines) - i - 1:]
#             break

#     with open(file_path, 'w') as file:
#         file.writelines(lines)

# for md_file in markdown_files:
#     file_path = os.path.join(output_folder, md_file)
#     remove_after_pattern(file_path, "## Support independent authors and access the best of Medium.")


import re
import os

def process_markdown_files(output_folder):
    markdown_files = [f for f in os.listdir(output_folder) if f.endswith(".md")]

    def extract_first_heading_and_next_line(file_path):
        with open(file_path, 'r') as file:
            md_text = file.read()
        pattern = r"^(#{1,6}) (.*$)\n(.*$)"
        match = re.search(pattern, md_text, re.MULTILINE)
        if match:
            return ' '.join([match.group(2).strip(), match.group(3).strip()])
        else:
            return None

    def remove_after_more_from(file_path):
        with open(file_path, 'r') as file:
            md_text = file.read()
        pattern = r"## More from.*"
        modified_text = re.sub(pattern, "", md_text, flags=re.DOTALL)
        with open(file_path, 'w') as file:
            file.write(modified_text)

    def remove_until_share(file_path):
        with open(file_path, 'r') as file:
            md_text = file.read()
        pattern = r".*Share.*?\n"
        modified_text = re.sub(pattern, "", md_text, flags=re.DOTALL)
        with open(file_path, 'w') as file:
            file.write(modified_text)

    def add_heading(file_path, heading):
        with open(file_path, 'r+') as file:
            md_text = file.read()
            file.seek(0)
            file.write("# " + heading + "\n" + md_text)

    def remove_after_written_by(file_path):
        with open(file_path, 'r') as file:
            md_text = file.read()

        # Remove everything after and including "## Written by"
        pattern = r"## Written by.*"
        modified_text = re.sub(pattern, "", md_text, flags=re.DOTALL)

        with open(file_path, 'w') as file:
            file.write(modified_text)

    def find_last_pattern_line_number(file_path, pattern):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Traverse the lines list in reverse order
        for num, line in enumerate(reversed(lines), 1):
            if pattern in line:
                # Return the line number from the end
                return len(lines) - num + 1
        return None

    def delete_lines_from(file_path, start_line):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Delete lines from start_line - 3 to the end
        del lines[start_line - 3:]

        with open(file_path, 'w') as file:
            file.writelines(lines)

    def remove_after_pattern(file_path, pattern):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Traverse the lines list in reverse order
        for i, line in enumerate(reversed(lines)):
            if line.startswith(pattern):
                # Delete lines from this line number till the end
                del lines[len(lines) - i - 1:]
                break

        with open(file_path, 'w') as file:
            file.writelines(lines)

    for md_file in markdown_files:
        file_path = os.path.join(output_folder, md_file)
        heading = extract_first_heading_and_next_line(file_path)
        remove_after_more_from(file_path)
        remove_until_share(file_path)
        add_heading(file_path, heading)
        remove_after_written_by(file_path)
        pattern_line_number = find_last_pattern_line_number(file_path, "\\--")
        try:
            delete_lines_from(file_path, pattern_line_number)
        except:
            pass
        remove_after_pattern(file_path, "## Support independent authors and access the best of Medium.")

# if __name__ == "__main__":
#     output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
#     process_markdown_files(output_folder)

