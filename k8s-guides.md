## Guides of Kubernetes Deployment on Ubuntu 18.04

Go to https://phoenixnap.com/kb/install-kubernetes-on-ubuntu for reference.

### An Example on the Symphony Cluster

#### Install Docker

- Update the package list with the command `sudo apt update`.
- Install Docker with the command: `sudo apt install docker.io`.
- Check the installation and version by entering the following: `docker -v`.
    - 19.03.2: dvorak, dvorak-2-2, dvorak-2-3, dvorak-1-1, dvorak-1-2, dvorak-1-4
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
- Add Software Repositories because Kubernetes is not included in the default repositories: `sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"`.
- Install Kubernetes Admin, which is a tool that helps initialize a cluster, with the command:
    - `sudo apt install kubeadm kubelet kubectl`;
    - `sudo apt-mark hold kubeadm kubelet kubectl`;
    - `kubeadm version` (verify the installation);
    - Refer to: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
- Repeat for all server nodes.

#### Deploy Kubernetes

- [**ALL**] Disable the swap memory on each server: `sudo swapoff -a`.
- [**ALL**] Assign unique hostname for each server node: `sudo hostnamectl set-hostname xxx`.
- [**MASTER**] Initialize Kubernetes on the master node: 
    - `sudo kubeadm init --pod-network-cidr=10.244.0.0/16`: Once this command finishes, it will display a `kubeadm join` message at the end. Make a note of the whole entry because it will be used to join the worker nodes to the cluster.
        - `--pod-network-cidr=10.244.0.0/16` is for flannel virtual network to work.
    - Create a directory for the cluster:
        - `mkdir -p $HOME/.kube`;
        - `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`;
        - `sudo chown $(id -u):$(id -g) $HOME/.kube/config`;
- [**MASTER**] Deploy pod network to the cluster. A pod network is a way to allow communication between different nodes in the cluster.
    - `sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`;
    - `kubectl get pods --all-namespaces` (verify the pod network is working);
- [**WORKER**] Connect each worker node to the cluster.
    - `sudo kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef 1.2.3.4:6443` (replace the alphanumeric codes with those from your master server during initialization);
- [**MASTER**] Check the worker nodes joined to the clusster: `kubectl get nodes`.

By going through all the instructions above, a Kubernetes cluster should be installed, deployed and ready for use.

[Optional] In order to get a kubectl on some other computer (e.g. laptop) to talk to your cluster, you need to copy the administrator `kubeconfig` file from your control-plane node to your workstation like this:

```
scp root@<control-plane-host>:/etc/kubernetes/admin.conf .
kubectl --kubeconfig ./admin.conf get nodes
```

#### Cluster Setup

The example Kubernetes cluster consists of one master node and four worker nodes, all with version `v1.17.2`.

- Master node(s): dvorak
- Worker node(s): dvorak-2-1, dvorak-2-2, dvorak-2-3, dvorak-2-4

Commands to join worker nodes to the Kubernetes cluster (**run as root**):

```
kubeadm join 192.17.100.193:6443 --token 6nyoyd.m9y4647myjz72bvq \
    --discovery-token-ca-cert-hash sha256:15c534de029ce6056404b1c8be0b2a9b63007b0166a48189bd613492d709f961
```

Show all nodes:

```
ubuntu@dvorak:~$ kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
dvorak       Ready    master   22m   v1.17.2
dvorak-2-1   Ready    worker   18m   v1.17.2
dvorak-2-2   Ready    worker   16m   v1.17.2
dvorak-2-3   Ready    worker   16m   v1.17.2
dvorak-2-4   Ready    worker   15m   v1.17.2
```

### Miscellaneous

#### Invalid Signature/Public Key Not Available

If you see error messages like:

```
W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: http://dl.google.com/linux/chrome/deb stable Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 78BD65473CB3BD13
W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: https://dl.yarnpkg.com/debian stable InRelease: The following signatures were invalid: EXPKEYSIG 23E7166788B63E1E Yarn Packaging <yarn@dan.cx>
```

Adding the key using `apt-key` can solve the problem: `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys KEY`.

#### Remove Previously Installed Kubernetes

To remove the outdated Kubernetes installed on the node, execute `sudo apt --purge remove kubeadm kubectl kubelet`.

#### Add/Remove Labels to Nodes in Kubernetes

```
kubectl label node dvorak-2-1 labelname=labelvalue             # add label
kubectl label node dvorak-2-1 labelname-                       # remove label
kubectl label node dvorak-2-1 node-role.kubernetes.io/worker=  # label as worker
```

#### Commands on Displaying Machine/Server Info

- `hostnamectl status`

```
ubuntu@dvorak-2-4:~$ sudo hostnamectl status
   Static hostname: dvorak-2-4
         Icon name: computer-server
           Chassis: server
        Machine ID: 052dfdf6532f42dc8b9098c2e9f2cede
           Boot ID: d9a6da775f214be0b54b9a27c7ce2040
  Operating System: Ubuntu 18.04.3 LTS
            Kernel: Linux 4.15.0-70-generic
      Architecture: x86-64
```
