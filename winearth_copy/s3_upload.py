#!/usr/bin/env python

import boto3
import botocore
import hashlib
import os


class S3Upload:
    """
    A class for uploading files to Amazon S3.

    Args:
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
        s3_host (str): The S3 host URL.
        addressing_style (str, optional): The S3 addressing style. Defaults to "auto".

    Attributes:
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
        s3_host (str): The S3 host URL.
        addressing_style (str): The S3 addressing style.
        s3 (boto3.resources.factory.s3.ServiceResource): The S3 resource.

    """

    def __init__(
        self, aws_access_key_id, aws_secret_access_key, s3_host, addressing_style
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.s3_host = s3_host
        self.addressing_style = addressing_style

        self.s3 = self.s3_auth(
            aws_access_key_id, aws_secret_access_key, s3_host, addressing_style
        )

    def md5(self, path):
        """
        Calculate the MD5 hash of a file.

        Args:
            path (str): The path to the file.

        Returns:
            str: The MD5 hash of the file.

        """
        hash_md5 = hashlib.md5()
        try:
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except Exception as e:
            print("MD5 error: %s" % e)
            return None

        return hash_md5.hexdigest()

    def remove_file(self, path):
        """
        Remove a file.

        Args:
            path (str): The path to the file.

        Returns:
            None

        """
        try:
            os.remove(path)
        except Exception as e:
            print("Remove file error: %s" % e)

        return None

    def get_object_etag(self, bucket_name, object_name):
        """
        Get the ETag of an object in a bucket.

        Args:
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.

        Returns:
            str: The ETag of the object.

        """
        try:
            etag = self.s3.meta.client.head_object(Bucket=bucket_name, Key=object_name)[
                "ETag"
            ].replace('"', "")
        except botocore.exceptions.ClientError as e:
            print("S3 ClientError: %s" % e)
            return None

        return etag

    def upload_object(self, bucket_name, object):
        """
        Upload an object to a bucket.

        Args:
            bucket_name (str): The name of the bucket.
            object (str): The path to the object.

        Returns:
            boto3.resources.factory.s3.Object: The uploaded object.

        """
        try:
            self.s3.Object(bucket_name, object).put(Body=open(object, "rb"))
            uploaded_object = self.s3.Object(bucket_name, object)
        except botocore.exceptions.ClientError as e:
            print("S3 ClientError: %s" % e)
            return None
        except FileNotFoundError as e:
            print("FileNotFoundError: %s" % e)
            return None

        return uploaded_object

    def s3_auth(
        self, aws_access_key_id, aws_secret_access_key, s3_host, addressing_style="auto"
    ):
        """
        Authenticate with Amazon S3.

        Args:
            aws_access_key_id (str): The AWS access key ID.
            aws_secret_access_key (str): The AWS secret access key.
            s3_host (str): The S3 host URL.
            addressing_style (str, optional): The S3 addressing style. Defaults to "auto".

        Returns:
            boto3.resources.factory.s3.ServiceResource: The S3 resource.

        """
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=s3_host,
            config=botocore.client.Config(
                signature_version="s3", s3={"addressing_style": addressing_style}
            ),
        )

        return s3

    def upload_directory(self, bucket_name, path):
        """
        Upload a directory to a bucket.

        Args:
            bucket_name (str): The name of the bucket.
            path (str): The path to the directory.

        Returns:
            int: 0 if successful.

        """
        for dir_path, dir_names, file_names in os.walk(path):
            for file_name in file_names:

                # Get the full path of the object
                object = os.path.join(dir_path, file_name)

                # Get md5 hash of the file
                local_md5sum = self.md5(object)

                # Upload the file
                self.upload_object(bucket_name, object)

                # Get the etag of the uploaded file
                etag = self.get_object_etag(bucket_name, object)

                # Verify the original and s3 md5 hashes match
                if local_md5sum == etag:
                    print("upload_object: Ok")
                else:
                    print("Upload Object Failed: %s %s" % (local_md5sum, etag))
                    return None

                # Remove random file
                self.remove_file(object)

        return 0
