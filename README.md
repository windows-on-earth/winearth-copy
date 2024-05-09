# winearth-copy

[![codecov](https://codecov.io/gh/windows-on-earth/winearth-copy/graph/badge.svg?token=DSBN6JON9I)](https://codecov.io/gh/windows-on-earth/winearth-copy)

[![Python package](https://github.com/windows-on-earth/winearth-copy/actions/workflows/pythonpackage.yml/badge.svg)](https://github.com/windows-on-earth/winearth-copy/actions/workflows/pythonpackage.yml)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Run with Docker

### Build the Docker Image

```bash

    docker build . --file Dockerfile --tag winearth-copy

```

### Download New NASA Images

```bash
   
    docker run  -it --rm --name=winearth-copy -v $PWD:/winearth winearth-copy:latest winearth-download --config config.json --query-date 20240101

``` 

### Upload Images to S3

```bash

    docker run  -it --rm --name=winearth-copy -v $PWD:/winearth winearth-copy:latest winearth-upload --config config.json 

```