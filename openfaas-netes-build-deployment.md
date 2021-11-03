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

This command will port-forward the OpenFaaS Gateway to your local port 31112:

```
kubectl port-forward deploy/gateway -n openfaas 31112:8080 &>/dev/null & echo -n "$!" > "of_${OF_DEV_ENV:-kind}_portforward.pid"
```

You can stop the forwarding with:

```
kill $(<"of_${OF_DEV_ENV:-kind}_portforward.pid")
```

For simplicity, a restart script is provided in `contrib/`:

```
./contrib/restart_port_forward.sh
```

### Login

You need to provide credentials and login to OpenFaaS gateway (password can be find in `password.txt` created when deploying OpenFaaS):

```
faas-cli login --password 08e0b3694c5f5182c0fdb21882545abd3ade6ca0
```

### Tear Down the Local KinD Cluster

Stop the entire environment and clean up using:

```
make stop-kind
```

## Example Usage

1. Get ready the source code of the function. (Templates available at https://docs.openfaas.com/cli/templates/)

```
faas-cli new hello-python --lang python3
```

It will generates source codes:

```
+ hello-python
  - handler.py
  - requirements.txt
- hello-python.yml
```

Edit the source code in `handler.py`:

```
def handle(req):
    print("Hello! " + req)
```

2. Build the function.

```
faas-cli build -f ./hello-python.yml
```

3. Push the function to register.

```
faas-cli push -f ./hello-python.yml
```

4. Deploy the function.

```
faas-cli deploy -f ./hello-python.yml
```

5. Invoke the function with the given URL after registering the fucntion.

```
curl URL -d PARAM
```

Reference: https://chaoscodes.github.io/2019/06/11/My-first-try-in-OpenFass/

### Get Function Info

```
$ faas-cli describe hello-python
Name:                hello-python
Status:              Ready
Replicas:            1
Available replicas:  1
Invocations:         7
Image:               haoranq4/hello-python:latest
Function process:    python3 index.py
URL:                 http://127.0.0.1:31112/function/hello-python
Async URL:           http://127.0.0.1:31112/async-function/hello-python
Labels:              faas_function : hello-python
                     uid : 626324001
Annotations:         prometheus.io.scrape : false
```
