import os
import unittest
from unittest.mock import patch, MagicMock
from src.url_to_local import download_image, update_image_links_in_markdown

class TestUrlToLocal(unittest.TestCase):

    @patch('requests.get')
    def test_download_image_success(self, mock_requests_get):
        url = "https://example.com/image.jpg"
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.content = b"Mock Image Content"
        mock_requests_get.return_value = response_mock

        image_path = download_image(url, output_folder)
        self.assertIsNotNone(image_path)
        self.assertTrue(os.path.exists(image_path))
        self.assertEqual(os.path.basename(image_path), "image.jpg")

    @patch('requests.get')
    def test_download_image_failure(self, mock_requests_get):
        url = "https://example.com/nonexistent.jpg"
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        response_mock = MagicMock()
        response_mock.status_code = 404
        mock_requests_get.return_value = response_mock

        image_path = download_image(url, output_folder)
        self.assertIsNone(image_path)

    def test_update_image_links_in_markdown(self):
        markdown_content = """This is an image: ![Image1](https://example.com/image1.jpg)
                             Another image: ![Image2](https://example.com/image2.png)"""
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        local_folder = os.path.join(output_folder, "local")
        image1_path = os.path.join(local_folder, "image1.jpg")
        image2_path = os.path.join(local_folder, "image2.png")
        os.makedirs(local_folder)

        with open(image1_path, 'wb') as f:
            f.write(b"Mock Image1 Content")
        with open(image2_path, 'wb') as f:
            f.write(b"Mock Image2 Content")

        updated_content, local_image_paths = update_image_links_in_markdown(markdown_content, output_folder)

        expected_content = f"""This is an image: ![Image1]({os.path.relpath(image1_path, output_folder)})
                             Another image: ![Image2]({os.path.relpath(image2_path, output_folder)})"""
        self.assertEqual(updated_content, expected_content)
        self.assertEqual(local_image_paths, [image1_path, image2_path])

        os.remove(image1_path)
        os.remove(image2_path)
        os.removedirs(local_folder)

if __name__ == "__main__":
    unittest.main()
