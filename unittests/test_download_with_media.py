import os
import unittest
from unittest.mock import patch, Mock
from download_with_media import download_medium_article


class TestDownloadWithMedia(unittest.TestCase):

    def setUp(self):
        self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(self.output_folder, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.output_folder)

    @patch('download_with_media.sync_playwright')
    @patch('download_with_media.requests.get')
    @patch('download_with_media.open')
    def test_download_medium_article_success(self, mock_open, mock_requests_get, mock_sync_playwright):
        # Prepare mock data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Article Content</p></body></html>"
        mock_requests_get.return_value = mock_response

        mock_page = Mock()
        mock_page.content.return_value = "<html><body><p>Page Content</p></body></html>"
        mock_sync_playwright.return_value.__enter__.return_value.chromium.launch.return_value.new_page.return_value = mock_page

        # Invoke the download_medium_article function
        article_url = "https://test-article-url.com"
        download_successful = download_medium_article(article_url, self.output_folder)

        # Assert that the download was successful
        self.assertTrue(download_successful)

        # Verify that the expected requests.get and sync_playwright calls were made
        mock_requests_get.assert_called_once_with(article_url)
        mock_sync_playwright.assert_called_once()

        # Verify that the mock page was used to get the page content
        mock_page.goto.assert_called_once_with(article_url)
        mock_page.wait_for_load_state.assert_called_once()
        mock_page.content.assert_called_once()

        # Verify that the correct content was written to the markdown file
        mock_open.assert_called_once_with(os.path.join(self.output_folder, "Article Title.md"), 'w', encoding='utf-8')
        file_write_calls = mock_open.return_value.__enter__.return_value.write.mock_calls
        self.assertIn("Page Content", str(file_write_calls))
        self.assertIn("# Article Title", str(file_write_calls))
        self.assertIn("Article Content", str(file_write_calls))

    @patch('download_with_media.sync_playwright')
    @patch('download_with_media.requests.get')
    def test_download_medium_article_failure(self, mock_requests_get, mock_sync_playwright):
        # Prepare mock data for failed download
        mock_response = Mock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Invoke the download_medium_article function
        article_url = "https://test-article-url.com"
        download_successful = download_medium_article(article_url, self.output_folder)

        # Assert that the download was unsuccessful
        self.assertFalse(download_successful)

        # Verify that the expected requests.get call was made
        mock_requests_get.assert_called_once_with(article_url)
        mock_sync_playwright.assert_not_called()


if __name__ == "__main__":
    unittest.main()
