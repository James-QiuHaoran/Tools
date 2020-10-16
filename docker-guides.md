## Docker Guide

### Docker Compose

- `docker-compose up`: Compose pulls a Redis image, builds an image for your code, and starts the services you defined.
- `docker-compose down`: Stop the application (you can also do this by hitting CTRL+C in the original terminal where you started the app).
- After modifying `docker-compose.yml` file, you need to rebuild the image by running `docker-compose up` again.
- After modifying application, you can see the changes instantly without rebuilding the image.
- If you want to run your services in the background, you can pass the `-d` flag (for "detached" mode) to `docker-compose up`.
- `docker-compose ps`: Show what's currently running.

### Docker

- `docker image ls`: List all local docker images.
- `docker ps`: List all docker containers.
- `docker inspect <tag or id>`: Inspect a particular image based on the tag or id.
- `docker run -d nginx:1.10.0`: Run the docker container in the background and print the container ID.
- `docker stop CONTAINERID`: Stop the running containers with the container ID.
- `docker rm CONTAINERID`: Remove the container and its used files.

Refer to https://docs.docker.com/get-started/ for quick start and https://docs.docker.com/engine/reference/commandline/docker/ for commands.

#### An Example of `docker run`

If you do `$ docker run -i -t ubuntu /bin/bash`, the following happens (assuming you are using the default registry configuration):

- If you do not have the ubuntu image locally, Docker pulls it from your configured registry, as though you had run `docker pull ubuntu` manually.
- Docker creates a new container, as though you had run a `docker container create` command manually.
- Docker allocates a read-write filesystem to the container, as its final layer. This allows a running container to create or modify files and directories in its local filesystem.
- Docker creates a network interface to connect the container to the default network, since you did not specify any networking options. This includes assigning an IP address to the container. By default, containers can connect to external networks using the host machine's network connection.
- Docker starts the container and executes `/bin/bash`. Because the container is running interactively and attached to your terminal (due to the `-i` and `-t` flags), you can provide input using your keyboard while the output is logged to your terminal.
- When you type `exit` to terminate the `/bin/bash` command, the container stops but is not removed. You can start it again or remove it.

#### Build and Deploy a Docker Image

To build a docker image, you need to prepare the source code and a Dockerfile (which specifies the instructions to build the application, the dependencies, as well as the command to run the program).

```
docker build -t haoranq4/image-name .
```

You can check `docker images` to see whether your image is in the local docker repository. It should be there!

Then you can deploy your docker container by `docker run -d -p 7001:7001 haoranq4/image-name`.

- `-d` means to run the container in background and print container ID.
- `-p 7001:7001` means to publish container's port 7001 to the host machine's port 7001.

You can delete the container by `docker stop container-id` and then `docker rm container-id`. The container id can be retrieved from `docker ps`.

You can push the image to the docker hub by `docker image push haoranq4/image-name`.

You can delete the image after all container instances are removed by `docker image rm haoranq4/image-name`.

#### Miscellaneous

Get the full container ID:

```
vagrant@dockertest:~$ docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS              PORTS               NAMES
ad6d5d32576a        nginx:latest        "nginx -g 'daemon of   About a minute ago   Up About a minute   80/tcp, 443/tcp     nostalgic_sammet
9bab1a42d6a9        nginx:latest        "nginx -g 'daemon of   About a minute ago   Up About a minute   80/tcp, 443/tcp     mad_kowalevski
beb70a6a2426        nginx:latest        "nginx -g 'daemon of   3 minutes ago        Up 3 minutes        80/tcp, 443/tcp     admiring_franklin

vagrant@dockertest:~$ docker ps -q --no-trunc | grep ad6d5d32576a
ad6d5d32576ad3cb1fcaa59b564b8f6f22b079631080ab1a3bbac9199953eb7d
```

Get the cgroup name with only the `pid`:

```
ps -o cgroup <pid>
```

### Docker Swarm

The following commands work for the Sward Orchestrator:

- `docker service ls`: List all docker services.
