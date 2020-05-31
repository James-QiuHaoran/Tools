## Docker Installation Guides

Docker support GPU natively (without replying on `nvidia-docker`) starting from version 19.03. However, this version does not support Power Machines.
Therefore, this guide is about how to install Docker 19.03.5 on Power Machines with Ubuntu 18.04.

### Get Docker 19.03.5 Ready

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

```
ubuntu@tuleta:~/test-docker$ tar zxvf docker-19.03.5.tgz 
docker/
docker/docker-proxy
docker/ctr
docker/runc
docker/dockerd
docker/containerd-shim
docker/containerd
docker/docker
docker/docker-init

ubuntu@tuleta:~/test-docker$ sudo mv docker/* /usr/bin/
```

- Start Docker daemon and run an application to check: `sudo dockerd &; sudo docker run hello-world`

This command downloads a test image and runs it in a container. When the container runs, it prints an informational message and exits.

### Nvidia GPU Setup

You don't have to do much here if you already have an NVIDIA GPU and an updated driver. However, you should be sure to have a recent NVIDIA driver installed.

If you are using a new OS install then an easy way to install/update the NVIDIA display driver is to use the "graphics drivers" ppa.

```
sudo add-apt-repository ppa:graphics-drivers/ppa

sudo apt-get update

sudo apt-get install build-essential dkms

sudo apt-get install nvidia-driver-440
```

You can install other available versions of `nvidia-driver` by pressing `[Tab]`.

### Install Nvidia Container Toolkit

Configure the repository first:

```
DIST=$(. /etc/os-release; echo $ID$VERSION_ID)

curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo apt-key add -

curl -s -L https://nvidia.github.io/libnvidia-container/$DIST/libnvidia-container.list | \
  sudo tee /etc/apt/sources.list.d/libnvidia-container.list

sudo apt-get update
```

Install `nvidia-container-toolkit`:

```
sudo apt-get install nvidia-container-toolkit
```

Restart Docker:

```
sudo systemctl restart docker
```

To test `nvidia-container-toolkit`, try the following (still running as root for now),

```
sudo docker run --gpus all --rm nvidia/cuda nvidia-smi
```

After the container downloads you should see the `nvidia-smi` output from the latest cuda release.

### Miscellaneous

#### Uninstall Docker

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Uninstall the Docker Engine - Community package:

```
$ sudo apt-get purge docker-ce
```

Images, containers, volumes, or customized configuration files on your host are not automatically removed. To delete all images, containers, and volumes:

```
$ sudo rm -rf /var/lib/docker
```

You must delete any edited configuration files manually.

#### Cannot Access

Current user cannot access var/run/docker/containerd/docker-containerd.sock

Solution:

```
$ sudo usermod -a -G docker $USER
$ sudo systemctl restart docker
```
