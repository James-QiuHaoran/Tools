## Docker Guide

### Docker-compose

- `docker-compose up`: Compose pulls a Redis image, builds an image for your code, and starts the services you defined.
- `docker-compose down`: Stop the application (you can also do this by hitting CTRL+C in the original terminal where you started the app).
- After modifying `docker-compose.yml` file, you need to rebuild the image by running `docker-compose up` again.
- After modifying application, you can see the changes instantly without rebuilding the image.
- If you want to run your services in the background, you can pass the `-d` flag (for "detached" mode) to `docker-compose up`.
- `docker-compose ps`: Show what's currently running.

### Docker

- `docker image ls`: List all local docker images.
- `docker inspect <tag or id>`: Inspect a particular image based on the tag or id.
- An example of `docker run`: `$ docker run -i -t ubuntu /bin/bash`, the following happens (assuming you are using the default registry configuration):
    - If you do not have the ubuntu image locally, Docker pulls it from your configured registry, as though you had run `docker pull ubuntu` manually.
    - Docker creates a new container, as though you had run a `docker container create` command manually.
    - Docker allocates a read-write filesystem to the container, as its final layer. This allows a running container to create or modify files and directories in its local filesystem.
    - Docker creates a network interface to connect the container to the default network, since you did not specify any networking options. This includes assigning an IP address to the container. By default, containers can connect to external networks using the host machine's network connection.
    - Docker starts the container and executes `/bin/bash`. Because the container is running interactively and attached to your terminal (due to the `-i` and `-t` flags), you can provide input using your keyboard while the output is logged to your terminal.
    - When you type `exit` to terminate the `/bin/bash` command, the container stops but is not removed. You can start it again or remove it.
