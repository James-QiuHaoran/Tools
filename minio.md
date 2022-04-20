# MinIO

## Intro

MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service. Use MinIO to build high performance infrastructure for machine learning, analytics and application data workloads.

## Get Started

References:
- https://hub.docker.com/r/minio/minio/
- https://docs.min.io/docs/minio-quickstart-guide.html

### GNU/Linux

Install and start MinIO server:

```
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server /data
```

The default port to use is `:9000` so change to other port that you want by using `--address localhost:7000`.

Console endpoint is listening on a dynamic port every time the server is started, please use `--console-address ":PORT"` to choose a static port.

## Usage

- Create a user to get `Access_Key` and `Secret_key`, which will be used by a MinIO client.
- Create a bucket, which is similar to a folder or directory in a file system.
- Use the API by specifying the address/port, access key and secret key.

Python API: https://docs.min.io/docs/python-client-api-reference.html
