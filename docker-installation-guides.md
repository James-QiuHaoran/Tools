## Docker Installation Guides

Docker support GPU natively (without replying on `nvidia-docker`) starting from version 19.03. However, this version does not support Power Machines.
Therefore, this guide is about how to install Docker 19.03.5 on Power Machines with Ubuntu 18.04.

## Get Docker Repository Ready

- Download the repository: `git clone https://github.com/docker/docker-ce.git`
- Switch to the specific tag:

```
git tag
git checkout v19.03.5
git branch
```
