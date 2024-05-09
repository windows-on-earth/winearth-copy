#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="winearth_copy",
    version="1.0.0",
    description="Download Windows on Earth data from NASA and upload to S3.",
    author="Kevin Coakley",
    author_email="kcoakley@sdsc.edu",
    url="https://github.com/windows-on-earth/winearth-copy",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "requests",
    ],
    entry_points={  # Optional
        "console_scripts": [
            "winearth-download=winearth_copy:download",
            "winearth-upload=winearth_copy:upload",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
