# winearth-copy

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