# OpenFaaS on Kubernetes

faas-netes: https://github.com/openfaas/faas-netes

## Local Development of faas-netes

### Requirements

TODO

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
make build

kind load docker-image --name="${OF_DEV_ENV:-kind}" openfaas/faas-netes:latest

helm upgrade openfaas --install openfaas/openfaas \
    --namespace openfaas  \
    --set basic_auth=true \
    --set openfaasImagePullPolicy=IfNotPresent \
    --set faasnetes.imagePullPolicy=IfNotPresent \
    --set faasnetes.image=openfaas/faas-netes:latest \
    --set functionNamespace=openfaas-fn
```

Note that this technique can also be used to test locally built functions, thus avoiding the need to push the image to a remote registry.

### Port Forwarding

TODO

### Tear Down the Local KinD Cluster

Stop the entire environment and clean up using:

```
make stop-kind
```
