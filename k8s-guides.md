## Guides of Kubernetes Deployment on Ubuntu 18.04

Go to https://phoenixnap.com/kb/install-kubernetes-on-ubuntu for reference.

### An Example on Symphony Cluster

#### Install Docker

- Update the package list with the command `sudo apt update`.
- Install Docker with the command: `sudo apt install docker.io`.
- Check the installation and version by entering the following: `docker -v`.
    - 19.03.2: dvorak-2-2, dvorak-2-3, dvorak-1-1, dvorak-1-2, dvorak-1-4
    - 19.03.4: dvorak-1-3
    - 19.03.5: dvorak-2-1, dvorak-2-4
- Repeat the process on each server that will act as a node in the Kubernetes cluster.

#### Start and Enable Docker

- Set Docker to launch at boot by entering the following command: `sudo systemctl enable docker`.
- Verify Docker is running: `sudo systemctl status docker`.
- Start Docker if it's not running: `sudo systemctl start docker`.
- Repeat the process on each server that will act as a node in the Kubernetes cluster.

#### Install Kubernetes

- Add Kubernetes signing key: `curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add`.
- Repeat for all server nodes.
