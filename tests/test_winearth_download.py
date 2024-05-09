import os
import unittest
import json
import tempfile
import requests_mock
from winearth_copy.winearth_download import (
    WinEarthDownload,
)  # Replace with the correct import path


class TestWinEarthDownload(unittest.TestCase):
    def setUp(self):
        self.query_date = "2024-05-08"
        self.api_key = "fake_api_key"
        self.win_earth = WinEarthDownload(self.query_date, self.api_key)
        self.temp_dir = tempfile.TemporaryDirectory()

        # Mocked response data
        self.mocked_json_data = [
            {
                "images.directory": "ISS/16/AS16",
                "images.filename": "AS16-12345.JPG",
                "mission": "Apollo 16",
                "pdate": "2024-05-08",
                "ptime": "08:00:00",
                "lat": "0.0",
                "lon": "0.0",
                "azi": "0.0",
                "elev": "0.0",
                "cldp": "10.0",
            },
            {
                "images.directory": "ISS/16/AS16",
                "images.filename": "AS16-12346.JPG",
                "mission": "Apollo 16",
                "pdate": "2024-05-08",
                "ptime": "08:10:00",
                "lat": "1.0",
                "lon": "1.0",
                "azi": "10.0",
                "elev": "10.0",
                "cldp": "20.0",
            },
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    @requests_mock.Mocker()
    def test_list_images(self, mock):
        # Mock the list_images API endpoint
        mock.get(
            self.win_earth.api_url,
            json=self.mocked_json_data,
            status_code=200,
        )

        response = self.win_earth.list_images()
        self.assertEqual(response, self.mocked_json_data)

    @requests_mock.Mocker()
    def test_list_images_failure(self, mock):
        # Mock the list_images API endpoint with failure status
        mock.get(self.win_earth.api_url, status_code=500)

        response = self.win_earth.list_images()
        self.assertIsNone(response)

    def test_save_metadata(self):
        # Save metadata to the temp directory
        saved_count = self.win_earth.save_metadata(
            self.mocked_json_data, self.temp_dir.name
        )

        # Verify the number of saved metadata files
        self.assertEqual(saved_count, len(self.mocked_json_data))

        # Check if the files exist and have the correct content
        for image_data in self.mocked_json_data:
            directory = os.path.join(self.temp_dir.name, image_data["images.directory"])
            filename = image_data["images.filename"].replace(".JPG", ".json")
            filepath = os.path.join(directory, filename)

            self.assertTrue(os.path.exists(filepath))

            with open(filepath, "r") as file:
                content = json.load(file)
                self.assertEqual(content, image_data)

        # Test the case where the metadata files already exist
        saved_count = self.win_earth.save_metadata(
            self.mocked_json_data, self.temp_dir.name
        )

        # Verify the number of downloaded metadata is 0
        self.assertEqual(saved_count, 0)

    @requests_mock.Mocker()
    def test_download_images(self, mock):
        # Mock the image download URLs
        for image_data in self.mocked_json_data:
            image_url = f"{self.win_earth.base_download_url}{image_data['images.directory']}/{image_data['images.filename']}"
            mock.get(image_url, content=b"This is a test image")

        downloaded_count = self.win_earth.download_images(
            self.mocked_json_data, self.temp_dir.name
        )

        # Verify the number of downloaded images
        self.assertEqual(downloaded_count, len(self.mocked_json_data))

        # Check if the files exist and have the correct content
        for image_data in self.mocked_json_data:
            directory = os.path.join(self.temp_dir.name, image_data["images.directory"])
            filename = image_data["images.filename"]
            filepath = os.path.join(directory, filename)

            self.assertTrue(os.path.exists(filepath))

            with open(filepath, "rb") as file:
                content = file.read()
                self.assertEqual(content, b"This is a test image")

        # Test the case where the downloaded images already exist
        for image_data in self.mocked_json_data:
            image_url = f"{self.win_earth.base_download_url}{image_data['images.directory']}/{image_data['images.filename']}"
            mock.get(image_url, content=b"This is a test image")

        downloaded_count = self.win_earth.download_images(
            self.mocked_json_data, self.temp_dir.name
        )

        # Verify the number of downloaded images is 0
        self.assertEqual(downloaded_count, 0)
