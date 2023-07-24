import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the root directory to sys.path so that we can import main.py from src folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main.py module from the src folder
from src import main

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=["https://siddharthksah.medium.com/synthetic-data-test-article-727e1f8ac2cb"])
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(url=None))
    def test_prompt_input(self, mock_parse_args, mock_input):
        url = main.prompt_input("Enter the URL of the Medium article:")
        self.assertEqual(url, "https://siddharthksah.medium.com/synthetic-data-test-article-727e1f8ac2cb")
        mock_parse_args.assert_called_once()
        mock_input.assert_called_once_with("Enter the URL of the Medium article:")

    @patch('builtins.input', side_effect=["y"])
    def test_prompt_confirmation(self, mock_input):
        result = main.prompt_confirmation("Would you like to open the markdown file in your default editor?")
        self.assertTrue(result)
        mock_input.assert_called_once_with("Would you like to open the markdown file in your default editor?")

    # Add more test cases for other functions in main.py as needed

if __name__ == "__main__":
    unittest.main()
