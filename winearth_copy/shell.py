#!/usr/bin/env python

import sys
from datetime import datetime
import winearth_copy.arguments
import winearth_copy.read_configuration
from winearth_copy.winearth_download import WinEarthDownload
from winearth_copy.s3_upload import S3Upload


def download():
    """
    :return: 0 if successful otherwise return an error message as a string
    """
    args = winearth_copy.arguments.parse_arguments(sys.argv[1:])

    if args.query_date is None:
        query_date = datetime.today().strftime("%Y%m%d")
    else:
        query_date = args.query_date

    configuration = winearth_copy.read_configuration.read_configuration(
        args.configuration_file
    )

    start_time = datetime.now()

    gape = WinEarthDownload(query_date, configuration["gape_api_key"])
    results = gape.list_images()

    if results is None:
        return "Failed to retrieve images from GAPE API."
    if "result" in results:
        if (
            results["result"]
            == "SQL found no records that match the specified criteria"
        ):
            return "No images found for %s." % args.query_date

    print(f"Found {len(results)} images for {query_date}")

    meta_data_count = gape.save_metadata(results, configuration["path"])
    download_count = gape.download_images(results, configuration["path"])

    end_time = datetime.now()

    print(f"Saved {meta_data_count} metadata files to {configuration['path']}")
    print(f"Downloaded {download_count} images to {configuration['path']}")
    print(f"Time elapsed: {end_time - start_time}")

    return 0


def upload():
    args = winearth_copy.arguments.parse_arguments(sys.argv[1:])

    configuration = winearth_copy.read_configuration.read_configuration(
        args.configuration_file
    )

    aws_access_key_id = configuration["aws_access_key_id"]
    aws_secret_access_key = configuration["aws_secret_access_key"]
    s3_host = configuration["s3_host"]
    addressing_style = configuration["addressing_style"]
    bucket_name = configuration["bucket_name"]
    path = configuration["path"]

    s3 = S3Upload(aws_access_key_id, aws_secret_access_key, s3_host, addressing_style)

    result = s3.upload_directory(bucket_name, path)

    return result
