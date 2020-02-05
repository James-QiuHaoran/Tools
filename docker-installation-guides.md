## Docker Installation Guides

Docker support GPU natively (without replying on `nvidia-docker`) starting from version 19.03. However, this version does not support Power Machines.
Therefore, this guide is about how to install Docker 19.03.5 on Power Machines with Ubuntu 18.04.

## Get Docker Repository Ready

- Download the repository: `git clone https://github.com/docker/docker-ce.git`;
- Switch to the specific tag:

```
git tag
git checkout v19.03.5
git branch
```

- Have a running `docker` daemon to proceed (`dockerd` is built using docker);
- Build: `make static DOCKER_BUILD_PKGS=static-linux DOCKER_BUILDKIT=0`;
- Check that results from the build: `tree ./components/packaging/static/build/linux`;

```
ubuntu@tuleta:~/docker-ce$ tree ./components/packaging/static/build/linux
./components/packaging/static/build/linux
├── docker
│   ├── containerd
│   ├── containerd-shim
│   ├── ctr
│   ├── docker
│   ├── dockerd
│   ├── docker-init
│   ├── docker-proxy
│   └── runc
├── docker-19.03.5.tgz
├── docker-rootless-extras
│   ├── dockerd-rootless.sh
│   ├── rootlesskit
│   └── rootlesskit-docker-proxy
└── docker-rootless-extras-19.03.5.tgz
```

- Send the `.tgz` to the machines you want, unpack it to the desired destination (`/usr/bin` if you don’t want to change the systemd scripts) and you’re done.


## Miscellaneous

### Uninstall Docker Engine - Community

Uninstall the Docker Engine - Community package:

```
$ sudo apt-get purge docker-ce
```

Images, containers, volumes, or customized configuration files on your host are not automatically removed. To delete all images, containers, and volumes:

```
$ sudo rm -rf /var/lib/docker
```

You must delete any edited configuration files manually.
