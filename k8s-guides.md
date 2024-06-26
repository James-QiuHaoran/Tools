## Kubernetes Usage Guide

Kubectl controls the Kubernetes Cluster. It is one of the key components of Kubernetes which runs on the workstation on any machine when the setup is done. It has the capability to manage the nodes in the cluster.

`kubectl` commands are used to interact and manage Kubernetes objects and the cluster.

Refer to https://www.tutorialspoint.com/kubernetes/kubernetes_kubectl_commands.htm.

A Guide: https://kubernetes.feisky.xyz/.

Cheat sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

### Standard Operations

- `kubectl get`: similar to `docker ps`, to look up resource lists;
    - `kubectl get apiservices`: show a list of API resources;
- `kubectl describe`: similar to `docker inspect`, to retrieve detailed info for resources;
- `kubectl logs`: similar to `docker logs`, to retrieve docker logs;
- `kubectl exec`: similar to `docker exec`, to execute a command inside a container;
- `kubectl run`: similar to `docker run`, to start a container (in fact a deployment managing a pod);
    - `kubectl run --image=nginx:alpine nginx-app --port=80`;
- `kubectl apply -f <filename>`: configure a resource by file or stdin;
- `kubectl create –f <filename>`: create resource by file (JSON or YAML, should be complete) or stdin;
- `kubectl delete –f ([-f FILENAME] | TYPE [(NAME | -l label | --all)])`: delete resources by file name, stdin, resource or names;
    - `kubectl delete -n social-network --all pod,svc --force --grace-period=0` does not delete the pods and services, instead, the pods are restarting;
    - Delete the deployments is the way to go if you want to delete the pods permenantly;

### Get and Describe Resources

```
# Get commands with basic output
kubectl get services                          # List all services in the namespace
kubectl get pods --all-namespaces             # List all pods in all namespaces
kubectl get pods -o wide                      # List all pods in the current namespace, with more details
kubectl get deployment my-dep                 # List a particular deployment
kubectl get pods                              # List all pods in the namespace
kubectl get pod my-pod -o yaml                # Get a pod's YAML

# Describe commands with verbose output
kubectl describe nodes my-node
kubectl describe pods my-pod
```

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
- `kubectl get deployments deployment_name -o yaml > yaml_file`: export the deployment to an `yaml` file;

### Check Application Configuration & Logs

- `kubectl get pods`: check for existing pods;
- `kubectl describe pods`: view what containers are inside that Pod and what images are used to build those containers;
- `kubectl logs $POD_NAME`: retrieve the logs that the application would normally send to STDOUT;
- Execute commands on the container once the pod is up and running:
  - `kubectl exec $POD_NAME env`
  - `kubectl exec -it $POD_NAME bash` (start a bash session in the container) [deprecated]
  - `kubectl exec -it $POD_NAME -- bash`

### Check Kuberentes Controller Log

```
journalctl -u kubelet -r
```

### Deploy Kubernetes Dashboard Web

Kubernetes dashboard web-service is not deployed by default. To deploy and access it, run

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
kubectl proxy
```

Then you can access the dashboard website using the url:

```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

You could use the bearer token to access. To get the token, run:

```
kubectl describe secrets
```

Note: You may need to create cluster role binding to cluster-admin if RBAC authentication is enabled. Refer to https://github.com/ubuntu/microk8s/issues/637 and https://github.com/fabric8io/fabric8/issues/6840.

### Disable Nodes

Drain the node that you don't want to schedule pods on:

```
kubectl drain <node-name>
```

You will see:

```
ubuntu@dvorak:/gpfs/gpfs0/home/haoranq4/DeathStarBench/socialNetwork/k8s-yaml$ kubectl get nodes
NAME         STATUS                     ROLES    AGE   VERSION
dvorak       Ready                      master   27d   v1.17.2
dvorak-2-1   Ready,SchedulingDisabled   worker   27d   v1.17.2
dvorak-2-2   Ready                      worker   27d   v1.17.2
dvorak-2-3   Ready                      worker   27d   v1.17.2
dvorak-2-4   Ready                      worker   27d   v1.17.2
```

You might have to ignore daemonsets and local-data in the machine.

```
kubectl drain <node-name> --ignore-daemonsets --delete-local-data
```

You can then delete the node or reset the machine if you want.

```
kubectl delete node <node-name>
kubeadm reset (on the worker node you delete)
```

You can rejoin the Kubernetes cluster by using `kubeadm join`.

If you don't want to delete/reset your node, you can then uncordon it and make it schedulable.

`kubectl cordon` can make the node unschedulable for new pods but Kubernetes doesn't migrate pods from it to other nodes.


### Port Forwarding for Pods

Different ways to forward a local port to a port on the Pod:

```
# change redis-master-765d459796-258hz to the name of the Pod
# local-port:pod-port
kubectl port-forward redis-master-765d459796-258hz 7000:6379
kubectl port-forward pods/redis-master-765d459796-258hz 7000:6379

# you can also do this to the service or deployment
kubectl port-forward service/redis-master 7000:6379
kubectl port-forward deployment/redis-master 7000:6379
```

The output is likely to be:

```
I0710 14:43:38.274550    3655 portforward.go:225] Forwarding from 127.0.0.1:7000 -> 6379
I0710 14:43:38.274797    3655 portforward.go:225] Forwarding from [::1]:7000 -> 6379
```

Then you can access the pod's port 6379 from your local port 7000.

### Show Detailed Version of `get pods`

```
ubuntu@dvorak:/gpfs/gpfs0/home/haoranq4/DeathStarBench/socialNetwork/k8s-yaml$ kubectl get pod -n social-network -o wide
NAME                                            READY   STATUS    RESTARTS   AGE     IP             NODE         NOMINATED NODE   READINESS GATES
compose-post-redis-cd45f4f88-sfm8m              1/1     Running   0          8m26s   10.244.3.36    dvorak-2-3   <none>           <none>
compose-post-service-7fbcbdf668-vl8s4           1/1     Running   0          8m26s   10.244.4.112   dvorak-2-4   <none>           <none>
home-timeline-redis-64c59cbcd4-2gc49            1/1     Running   0          8m26s   10.244.2.28    dvorak-2-2   <none>           <none>
home-timeline-service-697bd67c5d-9wsx8          1/1     Running   2          8m26s   10.244.4.113   dvorak-2-4   <none>           <none>
jaeger-d6f5784d5-t5wxf                          1/1     Running   2          8m26s   10.244.2.29    dvorak-2-2   <none>           <none>
media-frontend-c6967569-p6mhv                   1/1     Running   0          8m26s   10.244.4.115   dvorak-2-4   <none>           <none>
...
```

You can see the replicas, status, number of restarts, age, IP, on which node pods are deployed on, etc..

Or you can run this to get the pod-node information:

```
ubuntu@dvorak:~$ kubectl get pod -o=custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName -n social-network
NAME                                            STATUS    NODE
compose-post-redis-cd45f4f88-sfm8m              Running   dvorak-2-3
compose-post-service-7fbcbdf668-vl8s4           Running   dvorak-2-4
home-timeline-redis-64c59cbcd4-2gc49            Running   dvorak-2-2
...

ubuntu@dvorak:~$ kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name -n social-network
NODE         NAME
dvorak-2-3   compose-post-redis-cd45f4f88-sfm8m
dvorak-2-4   compose-post-service-7fbcbdf668-vl8s4
dvorak-2-2   home-timeline-redis-64c59cbcd4-2gc49
dvorak-2-4   home-timeline-service-697bd67c5d-9wsx8
...
```

### Restart a Pod

```
kubectl scale deployment pod-name --replicas=0 -n namespace-name
kubectl scale deployment pod-name --replicas=2 -n namespace-name
```

### Load Balancing

- `ipvs`;
- `iptables`;
- L7 Load-balancing: HAProxy, Envoy, etc.;


### Label Node Roles

Kubernetes does not assign roles for newly added nodes. So you may see something like this:

```
ubuntu@dvorak-2-1:~$ kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
dvorak-2-1   Ready    master   30m   v1.19.0
dvorak-2-2   Ready    <none>   28m   v1.19.0
dvorak-2-3   Ready    <none>   16m   v1.19.0
dvorak-2-4   Ready    <none>   14m   v1.19.0
```

A role is simply a label attached to the node, you can explicitly add the "worker" role/label to any node in the cluster:

```
ubuntu@dvorak-2-1:~$ kubectl label node dvorak-2-2 node-role.kubernetes.io/worker=worker
node/dvorak-2-2 labeled
ubuntu@dvorak-2-1:~$ kubectl label node dvorak-2-3 node-role.kubernetes.io/worker=worker
node/dvorak-2-3 labeled
ubuntu@dvorak-2-1:~$ kubectl label node dvorak-2-4 node-role.kubernetes.io/worker=worker
node/dvorak-2-4 labeled
ubuntu@dvorak-2-1:~$ kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
dvorak-2-1   Ready    master   30m   v1.19.0
dvorak-2-2   Ready    worker   28m   v1.19.0
dvorak-2-3   Ready    worker   16m   v1.19.0
dvorak-2-4   Ready    worker   14m   v1.19.0
```

### Force Delete A Namespace

Sometimes a namespace is deleted using `kubectl delete` but stuck at a "Terminating" stage forever. This is usually due to some unresolved "finalizer".

A solution is to delete the finalizer first and then delete the namespace. For example, if the namespace you want to delete is called "social-network":

```
kubectl get namespace social-network -o json > tmp.json
vim tmp.json # remove the line containing the finalizer
curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json https://10.0.0.108:6443/api/v1/namespaces/social-network/finalize # replace 10.0.0.108:6443 with the cluster ip and port by executing kubectl cluster-info
```

The namespace should be removed completely now.

If the response of the command is like some error message like `"message": "namespaces "social-network" is forbidden: User "system:anonymous" cannot update resource "namespaces/finalize" in API group "" in the namespace "social-network""`, you can try use `kubectl proxy`.

```
kubectl proxy &
curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json https://127.0.0.1:8001/api/v1/namespaces/social-network/finalize
```

The namespace should be removed completely now.

If there's error message like "curl: (35) error:1408F10B:SSL routines:ssl3_get_record:wrong version number", you can then try to use `http` instead of `https`.

```
curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json http://127.0.0.1:8001/api/v1/namespaces/social-network/finalize
```

The namespace should be removed completely now.

## Custom Resource and Custom Resource Definition

Kubernetes exposes a powerful declarative API system, where the record of intent or desired state is specified by cluster operators in a YAML file or via the REST API, and created and persisted in the data store, and then the controllers work in a control loop to converge intent with the observed state.
A Kubernetes resource is a collection of similar objects accessible via the Kubernetes API. Kubernetes comes with several resources by default, such as pods, deployments and ReplicaSets.

### Custom Resource Definition (CRD)

A [custom resource definition (CRD)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/) is a powerful feature introduced in Kubernetes 1.7.

The standard Kubernetes distribution ships with many built-in API objects and resources. CRDs enable IT admins to introduce unique objects or types into the Kubernetes cluster to meet their custom requirements. A Kubernetes CRD acts like any other Kubernetes object: It uses all the features of the Kubernetes ecosystem -- for example, its command-line interface (CLI), security, API services and role-based access control. The custom resource is also stored in the etcd cluster with proper replication and lifecycle management. CRDs eliminate the overhead of self-directed implementation as well.

CRDs are, by themselves, just blobs of data: Their primary purpose is to provide a mechanism to create, store and expose Kubernetes API objects that contain data that suits any requirements not satisfied by default. CRDs do not have any logic attached, nor any special behavior; once they are created, modified or removed, they take no actions on their own.

### Custom Resource (CR)

In a nutshell, custom resources are extensions of the Kubernetes API. But, unlike a normal resource, custom resources are not necessarily available in a default Kubernetes installation. Custom resources are instead registered **dynamically** to a cluster. Once the custom resource is registered, end users can create, update and delete its object using `kubectl`, similar to how users interact with built-in resources, like pods, deployments and services. Kubernetes apiserver manages defined custom resources like standard resources (e.g. ReplicaSet, etc).

Custom resources are used for small, in-house configuration objects without any corresponding controller logic -- and are, therefore, defined declaratively.

Tools to generate the code from CRD yaml: https://github.com/kubernetes/code-generator

### Using CRD and CRs

- Create the CRD and register it to the platform (namely the API server)
- Create a new instance (a CR) of the new CRD

Tutorials:
- https://insujang.github.io/2020-02-11/kubernetes-custom-resource/
- https://insujang.github.io/2020-02-13/programming-kubernetes-crd/

Kubernetes provides a set of options to build a custom controller (to handle CRD events), i.e., using [Operator SDK](https://github.com/operator-framework/operator-sdk), [kubebuilder](https://github.com/kubernetes-sigs/kubebuilder), or [code-generator](https://github.com/kubernetes/code-generator).

Implementing a custom controller with the **code-generator** involves two Kubernetes libraries:
- `client-go`: Go client library that provides all helper functions to access the Kubernetes apiserver.
- `code-generator`: Go library that generates some components that are required to implement a custom controller, based on our CRD specification.

Follow the [instructions](https://insujang.github.io/2020-02-13/programming-kubernetes-crd/):
- Generating Go code with code-generator
- Implementing custom controller based on the generated code and client-go
