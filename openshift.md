# OpenShift

## OpenShift Container Platform

OpenShift is a family of containerization software products developed by Red Hat. Its flagship product is the OpenShift Container Platform — a hybrid cloud platform as a service built around Linux containers orchestrated and managed by Kubernetes on a foundation of Red Hat Enterprise Linux.

## OpenShift CLI

You can use the Red Hat® OpenShift® on IBM Cloud® command line interface (CLI) plug-in (`ibmcloud oc`) to create and manage your Red Hat OpenShift cluster infrastructure, such as creating clusters and worker nodes. Then, you can use the Red Hat OpenShift CLI (`oc`) to manage the resources within your Red Hat OpenShift cluster, such as projects, pods, and deployments.

### Installing the IBM Cloud CLI and Plug-ins

```
$ ibmcloud login
$ ibmcloud plugin install container-service
$ ibmcloud plugin install container-registry
$ ibmcloud plugin install observe-service
$ ibmcloud plugin list
```

### Installing OpenShift CLI

Go to https://cloud.ibm.com/kubernetes/clusters?platformType=openshift

### Access the Cluster

```
$ ibmcloud oc cluster get -c <cluster_name_or_ID>

# get the passcode from https://iam.cloud.ibm.com/identity/passcode

$ oc login -u passcode -p <iam_passcode> --server=<master_URL>
```

### Start Using the `oc` Command

OpenShift's command line is called `oc`. It is identical to `kubectl` in most ways, but provides extra features that simplify tasks, such as container image deployment and logging into clusters.
