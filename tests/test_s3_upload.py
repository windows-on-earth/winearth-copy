import os
import hashlib
import tempfile
import unittest
from mock import patch
from botocore.stub import Stubber
from winearth_copy.s3_upload import S3Upload  # Replace with the correct import path


class TestS3Upload(unittest.TestCase):
    def setUp(self):
        # Initialize the S3Upload object with dummy credentials and endpoint
        aws_access_key_id = "fake_access_key"
        aws_secret_access_key = "fake_secret_key"
        s3_host = "http://localhost:4566"  # Replace with your test S3 endpoint
        addressing_style = "path"

        self.s3_upload = S3Upload(
            aws_access_key_id, aws_secret_access_key, s3_host, addressing_style
        )
        self.s3 = self.s3_upload.s3

        # Create a stubber for S3
        self.stubber = Stubber(self.s3.meta.client)
        self.stubber.activate()

        # Temporary S3 bucket name and file paths
        self.bucket_name = "test-bucket"
        self.object_name = "test-object.txt"

    def tearDown(self):
        self.stubber.deactivate()

    def test_md5(self):
        # Create a temporary file with some data
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"This is a test file.")
            tmp_file_path = tmp_file.name

        # Calculate expected MD5 hash
        expected_md5 = hashlib.md5(b"This is a test file.").hexdigest()

        # Check the result of md5 function
        result = self.s3_upload.md5(tmp_file_path)

        # Clean up the temporary file
        os.remove(tmp_file_path)

        self.assertEqual(result, expected_md5)

    def test_md5_file_not_found(self):
        # Test with a non-existent file path
        non_existent_path = "non_existent_file.txt"
        result = self.s3_upload.md5(non_existent_path)
        self.assertIsNone(result)

    def test_remove_file(self):
        # Create a temporary file to remove
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"Temporary file to remove.")
            tmp_file_path = tmp_file.name

        # Ensure the file exists before removal
        self.assertTrue(os.path.exists(tmp_file_path))

        # Remove the file using the remove_file function
        self.s3_upload.remove_file(tmp_file_path)

        # Assert that the file no longer exists
        self.assertFalse(os.path.exists(tmp_file_path))

    def test_remove_non_existent_file(self):
        # Test with a non-existent file path
        non_existent_path = "non_existent_file.txt"
        self.s3_upload.remove_file(non_existent_path)

    def test_get_object_etag(self):
        # Stub the head_object response
        expected_etag = '"1234567890abcdef"'
        self.stubber.add_response(
            "head_object",
            {"ETag": expected_etag},
            {"Bucket": self.bucket_name, "Key": self.object_name},
        )

        # Run the test
        result = self.s3_upload.get_object_etag(self.bucket_name, self.object_name)
        self.assertEqual(result, expected_etag.replace('"', ""))

    def test_get_object_etag_non_existent_object(self):
        # Stub a ClientError response for a non-existent object
        self.stubber.add_client_error(
            "head_object",
            service_error_code="404",
            service_message="Not Found",
            expected_params={
                "Bucket": self.bucket_name,
                "Key": "non_existent_object.txt",
            },
        )

        # Run the test
        result = self.s3_upload.get_object_etag(
            self.bucket_name, "non_existent_object.txt"
        )
        self.assertIsNone(result)

    def test_upload_object(self):
        # Create a temporary file to upload
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"This is a test upload file.")
            tmp_file_path = tmp_file.name

        # Stub the put response
        self.stubber.add_response(
            "put_object",
            {},
        )

        # Run the upload_object function
        result = self.s3_upload.upload_object(self.bucket_name, tmp_file_path)

        # Clean up the temporary file
        os.remove(tmp_file_path)

        # Assert that the upload was successful
        self.assertIsNotNone(result)

    def test_upload_object_client_error(self):
        # Create a temporary file to upload
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"This is a test upload file.")
            tmp_file_path = tmp_file.name

        # Stub a ClientError response for the put_object call
        self.stubber.add_client_error(
            "put_object",
            service_error_code="500",
            service_message="Internal Server Error",
        )

        # Run the upload_object function
        result = self.s3_upload.upload_object(self.bucket_name, tmp_file_path)

        # Clean up the temporary file
        os.remove(tmp_file_path)

        # Assert that the upload failed
        self.assertIsNone(result)

    def test_upload_object_non_existent_file(self):
        # Run the upload_object function with a non-existent file
        result = self.s3_upload.upload_object(self.bucket_name, "non_existent_file.txt")
        self.assertIsNone(result)

    @patch.object(S3Upload, "get_object_etag")
    @patch.object(S3Upload, "upload_object")
    @patch.object(S3Upload, "md5")
    def test_upload_directory(self, mock_md5, mock_upload_object, mock_get_object_etag):
        mock_md5.return_value = "fake_md5"
        mock_get_object_etag.return_value = "fake_md5"

        # Create a temporary directory with multiple files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_paths = []
            for i in range(3):
                file_path = os.path.join(temp_dir, f"file_{i}.txt")
                with open(file_path, "w") as file:
                    file.write(f"File {i} content.")
                file_paths.append(file_path)

            # Stub the put response for each file
            for file_path in file_paths:
                self.stubber

            result = self.s3_upload.upload_directory(self.bucket_name, temp_dir)

        self.assertEqual(result, 0)

    @patch.object(S3Upload, "get_object_etag")
    @patch.object(S3Upload, "upload_object")
    @patch.object(S3Upload, "md5")
    def test_upload_directory_bad_md5(
        self, mock_md5, mock_upload_object, mock_get_object_etag
    ):
        mock_md5.return_value = "fake_md5"
        mock_get_object_etag.return_value = "fake_etag"

        # Create a temporary directory with multiple files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_paths = []
            for i in range(3):
                file_path = os.path.join(temp_dir, f"file_{i}.txt")
                with open(file_path, "w") as file:
                    file.write(f"File {i} content.")
                file_paths.append(file_path)

            # Stub the put response for each file
            for file_path in file_paths:
                self.stubber

            result = self.s3_upload.upload_directory(self.bucket_name, temp_dir)

        self.assertIsNone(result)
