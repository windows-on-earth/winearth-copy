import unittest
from unittest.mock import patch
import winearth_copy.read_configuration


class TestReadConfiguration(unittest.TestCase):
    def test_read_configuration_existing_file(self):
        # Mock the open function to return a file with valid JSON content
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                '{"gape_api_key": "12345"}'
            )
            configuration = winearth_copy.read_configuration.read_configuration(
                "/path/to/config.json"
            )

        expected_configuration = {
            "gape_api_key": "12345",
            "s3_host": "https://localhost:443",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "addressing_style": "auto",
            "bucket_name": "",
            "path": "/tmp",
        }

        self.assertEqual(configuration, expected_configuration)

    def test_read_configuration_missing_file(self):
        # Mock the open function to raise FileNotFoundError
        with patch("builtins.open", side_effect=FileNotFoundError):
            configuration = winearth_copy.read_configuration.read_configuration(
                "/path/to/nonexistent.json"
            )

        self.assertIsNone(configuration)

    def test_read_configuration_invalid_json(self):
        # Mock the open function to return a file with invalid JSON content
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                "invalid json"
            )
            configuration = winearth_copy.read_configuration.read_configuration(
                "/path/to/invalid.json"
            )

        self.assertIsNone(configuration)
