# OpenFaaS on Kubernetes

faas-netes: https://github.com/openfaas/faas-netes

## Local Development of faas-netes

### Requirements

1. Install KinD: https://github.com/kubernetes-sigs/kind
    - Use the latest `go` to do this, ideally `go` 1.13 or greater

```
$ GO111MODULE="on" go get sigs.k8s.io/kind@v0.11.1
```

2. Install `helm3`

```
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```

3. Install Tiller to your running Kubernetes cluster:

```
$ helm init
```

It will also set up any necessary local configuration.

4. Install `faas-cli`:

```
$ curl -sSL https://cli.openfaas.com | sudo sh
```

### Deployment

https://github.com/openfaas/faas-netes/blob/master/CONTRIBUTING.md#local-development-of-faas-netes

A Makefile and a series of scripts automates the creation of a local Kubernetes cluster with OpenFaaS preinstalled.
Kubernetes in Docker (KinD) is used to create a single-node cluster and install the latest version of OpenFaaS via the Helm chart.

```
make start-kind
```

You can use OF_DEV_ENV to set a custom name for the cluster. The default value is kind.

### Rebuild

As you are developing on faas-netes, you will want to build and test your own local images by loading a custom image into the KinD cluster.
This can easily be done using the following commands:

```
make build-docker # which will generated the docker image ghcr.io/openfaas/faas-netes:latest

kind load docker-image --name="${OF_DEV_ENV:-kind}" ghcr.io/openfaas/faas-netes:latest

helm upgrade openfaas --install chart/openfaas \
    --namespace openfaas  \
    --set basic_auth=true \
    --set openfaasImagePullPolicy=IfNotPresent \
    --set faasnetes.imagePullPolicy=IfNotPresent \
    --set faasnetes.image=ghcr.io/openfaas/faas-netes:latest \
    --set functionNamespace=openfaas-fn
```

Note that this technique can also be used to test locally built functions, thus avoiding the need to push the image to a remote registry.

To verify that OpenFaaS has been started and running, run:

```
kubectl -n openfaas get deployments -l "release=openfaas, app=openfaas"
```

### Port Forwarding

TODO

### Tear Down the Local KinD Cluster

Stop the entire environment and clean up using:

```
make stop-kind
```
