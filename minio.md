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

Install `mc`:

```
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc
chmod +x $HOME/minio-binaries/mc

export PATH=$PATH:$HOME/minio-binaries/
```

## Usage

- Create a user to get `Access_Key` and `Secret_key`, which will be used by a MinIO client.
- Create a bucket, which is similar to a folder or directory in a file system.
- Use the API by specifying the address/port, access key and secret key.

Python API: https://docs.min.io/docs/python-client-api-reference.html

### Create a User

```
mc alias set myminio http://localhost:7000 minioadmin minioadmin
# mc admin user add ALIAS ACCESSKEY SECRETKEY
mc admin user add myminio admin password
```

### Create a Bucket

```
mc mb myminio/my-bucket
mc mb myminio/compression
mc mb myminio/compression-results
```

### Copy a File to a Bucket (Create a Key)

```
# mc cp local/file/path myminio/compression
mc cp image1.jpeg myminio/compression/4k-image1
```

### Remove All Files in a Bucket

```
mc rm myminio/my-bucket --recursive --force
```
