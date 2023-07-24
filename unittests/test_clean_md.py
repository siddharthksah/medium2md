import os
import unittest
from clean_md import list_markdown_files, process_single_file, extract_first_heading_and_next_line, \
    remove_section_after, remove_until, add_heading, find_last_line_containing, delete_lines_from


class TestCleanMd(unittest.TestCase):

    def setUp(self):
        self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(self.output_folder, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.output_folder)

    def test_list_markdown_files(self):
        # Create dummy markdown files
        for i in range(5):
            with open(os.path.join(self.output_folder, f"test{i}.md"), 'w') as f:
                f.write(f"This is test {i}")

        # Get the list of markdown files
        markdown_files = list_markdown_files(self.output_folder)

        # Assert that all 5 files are found
        self.assertEqual(len(markdown_files), 5)

    def test_extract_first_heading_and_next_line(self):
        # Create a sample markdown file
        md_file_path = os.path.join(self.output_folder, "sample.md")
        with open(md_file_path, 'w') as f:
            f.write("# Heading 1\n\nThis is the first line.\n\n## Heading 2\n\nThis is the second line.")

        # Extract the first heading and the line that follows
        extracted_heading = extract_first_heading_and_next_line(md_file_path)

        # Assert that the extracted heading is correct
        self.assertEqual(extracted_heading, "Heading 1 This is the first line.")

    def test_remove_section_after(self):
        # Create a sample markdown file
        md_file_path = os.path.join(self.output_folder, "sample.md")
        with open(md_file_path, 'w') as f:
            f.write("# Heading 1\n\nThis is the first line.\n\n## Heading 2\n\nThis is the second line.")

        # Remove the section after Heading 1
        remove_section_after(md_file_path, "# Heading 1")

        # Read the modified content
        with open(md_file_path, 'r') as f:
            modified_content = f.read()

        # Assert that the section is removed
        self.assertNotIn("## Heading 2\n\nThis is the second line.", modified_content)

    def test_remove_until(self):
        # Create a sample markdown file
        md_file_path = os.path.join(self.output_folder, "sample.md")
        with open(md_file_path, 'w') as f:
            f.write("This is the first line.\n\nShare this article\n\nThis is the second line.")

        # Remove content until the keyword "Share"
        remove_until(md_file_path, "Share")

        # Read the modified content
        with open(md_file_path, 'r') as f:
            modified_content = f.read()

        # Assert that the content until the keyword is removed
        self.assertNotIn("This is the first line.", modified_content)

    def test_add_heading(self):
        # Create a sample markdown file
        md_file_path = os.path.join(self.output_folder, "sample.md")
        with open(md_file_path, 'w') as f:
            f.write("This is the first line.\n\nThis is the second line.")

        # Add a new heading
        add_heading(md_file_path, "New Heading")

        # Read the modified content
        with open(md_file_path, 'r') as f:
            modified_content = f.read()

        # Assert that the new heading is added
        self.assertEqual(modified_content.strip(), "# New Heading\n\nThis is the first line.\n\nThis is the second line.")

    def test_find_last_line_containing(self):
        # Create a sample markdown file
        md_file_path = os.path.join(self.output_folder, "sample.md")
        with open(md_file_path, 'w') as f:
            f.write("This is the first line.\n\n--\n\nThis is the second line.\n\n--")

        # Find the line number of the last occurrence of the pattern
        line_number = find_last_line_containing(md_file_path, "\\--")

        # Assert that the correct line number is found
        self.assertEqual(line_number, 5)

    def test_delete_lines_from(self):
        # Create a sample markdown file
        md_file_path = os.path.join(self.output_folder, "sample.md")
        with open(md_file_path, 'w') as f:
            f.write("This is the first line.\n\nThis is the second line.\n\n--\n\nThis is the third line.\n\nThis is the fourth line.")

        # Delete lines from a certain line number
        delete_lines_from(md_file_path, 3)

        # Read the modified content
        with open(md_file_path, 'r') as f:
            modified_content = f.read()

        # Assert that the lines are deleted
        self.assertEqual(modified_content.strip(), "This is the first line.\n\nThis is the second line.")


if __name__ == "__main__":
    unittest.main()
