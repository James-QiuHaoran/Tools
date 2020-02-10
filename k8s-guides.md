## Kubernetes Usage Guide

Kubectl controls the Kubernetes Cluster. It is one of the key components of Kubernetes which runs on the workstation on any machine when the setup is done. It has the capability to manage the nodes in the cluster.

Kubectl commands are used to interact and manage Kubernetes objects and the cluster.

Refer to https://www.tutorialspoint.com/kubernetes/kubernetes_kubectl_commands.htm.

### Standard Operations

- `kubectl apply -f <filename>`: configure a resource by file or stdin;
- `kubectl create –f <filename>`: create resource by file (JSON or YAML, should be complete) or stdin;
- `kubectl delete –f ([-f FILENAME] | TYPE [(NAME | -l label | --all)])`: delete resources by file name, stdin, resource or names;
    - `kubectl delete -n social-network --all pod,svc`;

### DNS Service Debugging

Check if the DNS pod is running by using the `kubectl get pods` command.

```
ubuntu@dvorak:/gpfs/gpfs0/home/haoranq4/DeathStarBench$ kubectl get pods --namespace=kube-system -l k8s-app=kube-dns
NAME                       READY   STATUS    RESTARTS   AGE
coredns-6955765f44-ctsl7   1/1     Running   0          3h33m
coredns-6955765f44-mgxq2   1/1     Running   0          3h33m
```

Verify that the DNS service is up by using the `kubectl get service` command.

```
ubuntu@dvorak:/gpfs/gpfs0/home/haoranq4/DeathStarBench$ kubectl get svc --namespace=kube-system
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   3h25m
```

Verify that DNS endpoints are exposed by using the `kubectl get endpoints` command.

```
ubuntu@dvorak:/gpfs/gpfs0/home/haoranq4/DeathStarBench$ kubectl get ep kube-dns --namespace=kube-system
NAME       ENDPOINTS                                               AGE
kube-dns   10.244.0.2:53,10.244.0.3:53,10.244.0.2:53 + 3 more...   3h31m
```

### Cluster Status Checking

- `kubectl version`
- `kubectl get nodes`
- `kubectl cluster-info`
- `kubectl get services`: list the current services from the cluster
- `kubectl get pod -n social-network`: list all the pods under the social-network namespace
- `kubectl get namespaces`: list all the created namespaces

### Deployments

Deployments are upgraded and higher version of replication controller. They manage the deployment of replica sets which is also an upgraded version of the replication controller. They have the capability to update the replica set and are also capable of rolling back to the previous version.

- `kubectl create deployment deployment_name image`: provide the deployment name and the app image location;
- `kubectl get deployments`;

### Check Application Configuration & Logs

- `kubectl get pods`
- `kubectl describe pods`
- `kubectl logs $POD_NAME`
- Execute commands on the container once the pod is up and running:
  - `kubectl exec $POD_NAME env`
  - `kubectl exec -it $POD_NAME bash` (start a bash session in the container)
