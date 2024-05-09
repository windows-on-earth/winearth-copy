#!/usr/bin/env python

import json


def read_configuration(path):
    """
    Reads the configuration file at the given path and returns a dictionary
    containing the merged default configuration and the file configuration.

    Args:
        _path (str): The path to the configuration file.

    Returns:
        dict: A dictionary containing the merged configuration.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.decoder.JSONDecodeError: If the configuration file is not a valid JSON.

    """
    default_configuration = {
        "gape_api_key": "",
        "s3_host": "https://localhost:443",
        "aws_access_key_id": "",
        "aws_secret_access_key": "",
        "addressing_style": "auto",
        "bucket_name": "",
        "path": "/tmp",
    }

    # Read the configuration file
    try:
        with open(path, "r") as f:
            file_configuration = json.load(f)
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return None

    # Merge the default config with the file config
    configuration = {**default_configuration, **file_configuration}
    return configuration
