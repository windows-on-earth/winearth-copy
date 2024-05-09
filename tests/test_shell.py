import unittest
from mock import patch
import mock
import winearth_copy.shell
from winearth_copy.winearth_download import WinEarthDownload
from winearth_copy.s3_upload import S3Upload


class TestShell(unittest.TestCase):

    @patch.object(WinEarthDownload, "download_images")
    @patch.object(WinEarthDownload, "save_metadata")
    @patch.object(WinEarthDownload, "list_images")
    @patch("winearth_copy.read_configuration.read_configuration")
    @patch("winearth_copy.arguments.parse_arguments")
    def test_download(
        self,
        mock_parse_arguments,
        mock_read_configuration,
        mock_list_images,
        mock_save_metadata,
        mock_download_images,
    ):

        # Test the download function where everything works
        mock_parse_arguments.return_value = mock.Mock(
            query_date="20240101", configuration_file="config.yml"
        )
        mock_read_configuration.configuration_file = {}

        mock_list_images.return_value = []

        result = winearth_copy.shell.download()

        self.assertEqual(result, 0)

        # Test the download function where results is returned but no error
        mock_list_images.return_value = {"result": "mock"}

        mock_save_metadata.return_value = 1
        mock_download_images.return_value = 1

        result = winearth_copy.shell.download()

        self.assertEqual(result, 0)

        # Test the download function when no date is provided
        mock_parse_arguments.return_value = mock.Mock(
            query_date=None, configuration_file="config.yml"
        )

        result = winearth_copy.shell.download()

        self.assertEqual(result, 0)

        # Test the download function when the API failes to retrieve images
        mock_list_images.return_value = None

        result = winearth_copy.shell.download()

        self.assertEqual(result, "Failed to retrieve images from GAPE API.")

        # Test the download function when no images are found
        mock_parse_arguments.return_value = mock.Mock(
            query_date="20240101", configuration_file="config.yml"
        )
        mock_list_images.return_value = {
            "result": "SQL found no records that match the specified criteria"
        }

        result = winearth_copy.shell.download()

        self.assertEqual(result, "No images found for 20240101.")

    @patch.object(S3Upload, "upload_directory")
    @patch("boto3.resource")
    @patch("winearth_copy.read_configuration.read_configuration")
    @patch("winearth_copy.arguments.parse_arguments")
    def test_upload(
        self,
        mock_parse_arguments,
        mock_read_configuration,
        mock_boto,
        mock_upload_directory,
    ):

        # Test the upload function where everything works
        mock_parse_arguments.return_value = mock.Mock(configuration_file="config.yml")
        mock_read_configuration.return_value = {
            "aws_access_key_id": "mock",
            "aws_secret_access_key": "mock",
            "s3_host": "mock",
            "addressing_style": "auto",
            "bucket_name": "mock",
            "path": "mock",
        }

        mock_upload_directory.return_value = 0

        result = winearth_copy.shell.upload()

        self.assertEqual(result, 0)
