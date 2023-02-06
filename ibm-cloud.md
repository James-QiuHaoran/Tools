# Commercial Cloud Platforms

## IBM Cloud

### IBM Cloud CLI

Install: https://cloud.ibm.com/docs/cli?topic=cli-getting-started

Plug-in for VPC management: https://cloud.ibm.com/docs/vpc?topic=vpc-infrastructure-cli-plugin-vpc-reference

### Examples

- List all VM instances: `ibmcloud is instances`

### Kubernetes Cluster Access

```
# login in to the IBM cloud account
ibmcloud login -a cloud.ibm.com -r us-south -g default
# or by sso
ibmcloud login -a cloud.ibm.com -r us-south -g default -sso

# set the k8s context to the cluster for this terminal session
ibmcloud ks cluster config --cluster bvd6gurd08ea509ckln0

# verify the connection to the k8s cluster
kubectl config current-context
kubectl get nodes
```

## AWS

### AWS CLI

Install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
Configuration: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

### Examples

- List AWS configurations: `aws configure list`
