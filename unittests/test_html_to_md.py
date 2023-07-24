import os
import unittest
from unittest.mock import patch
from src.html_to_md import convert_html_to_markdown

class TestHtmlToMd(unittest.TestCase):

    def setUp(self):
        self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(self.output_folder, exist_ok=True)

    def tearDown(self):
        for file in os.listdir(self.output_folder):
            file_path = os.path.join(self.output_folder, file)
            if file.endswith('.md'):
                os.remove(file_path)
        os.removedirs(self.output_folder)

    @patch('html2text.HTML2Text.handle')
    def test_convert_html_to_markdown_single_file(self, mock_html2text_handle):
        # Prepare a mock markdown content
        mock_markdown_content = "Mock Markdown Content"
        mock_html2text_handle.return_value = mock_markdown_content

        # Create a test .md file in the output folder
        test_md_file_path = os.path.join(self.output_folder, "test.md")
        with open(test_md_file_path, 'w') as f:
            f.write("<p>Test HTML Content</p>")

        # Invoke the conversion function
        convert_html_to_markdown(self.output_folder)

        # Read the updated content from the test .md file
        with open(test_md_file_path, 'r') as f:
            updated_content = f.read()

        # Assert that the content is updated with the mock markdown content
        self.assertEqual(updated_content, mock_markdown_content)

    @patch('html2text.HTML2Text.handle')
    def test_convert_html_to_markdown_multiple_files(self, mock_html2text_handle):
        # Prepare a mock markdown content
        mock_markdown_content = "Mock Markdown Content"
        mock_html2text_handle.return_value = mock_markdown_content

        # Create two test .md files in the output folder
        test_md_file1_path = os.path.join(self.output_folder, "test1.md")
        with open(test_md_file1_path, 'w') as f:
            f.write("<p>Test HTML Content 1</p>")

        test_md_file2_path = os.path.join(self.output_folder, "test2.md")
        with open(test_md_file2_path, 'w') as f:
            f.write("<p>Test HTML Content 2</p>")

        # Invoke the conversion function
        convert_html_to_markdown(self.output_folder)

        # Read the updated content from the test .md files
        with open(test_md_file1_path, 'r') as f:
            updated_content1 = f.read()

        with open(test_md_file2_path, 'r') as f:
            updated_content2 = f.read()

        # Assert that both .md files' content are updated with the mock markdown content
        self.assertEqual(updated_content1, mock_markdown_content)
        self.assertEqual(updated_content2, mock_markdown_content)

if __name__ == "__main__":
    unittest.main()
