#!/usr/bin/env python

import json
import os
import requests


class WinEarthDownload:
    def __init__(self, query_date, api_key):
        self.query_date = query_date
        self.api_key = api_key
        self.api_url = "https://eol.jsc.nasa.gov/SearchPhotos/PhotosDatabaseAPI/PhotosDatabaseAPI.pl"
        self.base_download_url = "https://eol.jsc.nasa.gov/DatabaseImages/"

    def list_images(self):
        """
        Retrieves a list of images based on the specified query date.

        Returns:
            dict or None: A dictionary containing the response data in JSON format if the request is successful,
            otherwise None.
        """
        params = {
            "query": f"nadir|pdate|eq|{self.query_date}",
            "return": "nadir|mission|nadir|roll|nadir|frame|nadir|pdate|nadir|ptime|nadir|lat|nadir|lon|nadir|azi|nadir|elev|nadir|cldp|images|directory|images|filename",
            "key": self.api_key,
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def save_metadata(self, json_data, path):
        """
        Save metadata for each image in the provided JSON data.

        Args:
            json_data (list): A list of dictionaries containing image metadata.
            path (str): The base path where the metadata files should be saved.

        Returns:
            int: The number of metadata files successfully written.

        """
        write_count = 0

        for image_data in json_data:
            full_path = "%s/%s/" % (path, image_data["images.directory"])
            filename = image_data["images.filename"].replace(".JPG", ".json")

            if not os.path.exists(os.path.dirname(full_path)):
                os.makedirs(os.path.dirname(full_path))

            if not os.path.exists(full_path + filename):
                with open(full_path + filename, "w") as f:
                    json.dump(image_data, f, indent=4)
                    write_count += 1

        return write_count

    def download_images(self, json_data, path):
        """
        Downloads images from the provided JSON data and saves them to the specified path.

        Args:
            json_data (list): A list of dictionaries containing image data.
            path (str): The path where the images will be saved.

        Returns:
            int: The number of images successfully downloaded and saved.
        """

        write_count = 0

        for image_data in json_data:
            full_path = "%s/%s/" % (path, image_data["images.directory"])
            filename = image_data["images.filename"]

            if not os.path.exists(os.path.dirname(full_path)):
                os.makedirs(os.path.dirname(full_path))

            if not os.path.exists(full_path + filename):
                with open(full_path + filename, "wb") as f:
                    f.write(
                        requests.get(
                            self.base_download_url
                            + image_data["images.directory"]
                            + "/"
                            + image_data["images.filename"]
                        ).content
                    )
                    print(f"Downloaded {image_data['images.filename']}")
                    write_count += 1

        return write_count
