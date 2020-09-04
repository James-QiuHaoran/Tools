## Kubernetes Usage Guide

Kubectl controls the Kubernetes Cluster. It is one of the key components of Kubernetes which runs on the workstation on any machine when the setup is done. It has the capability to manage the nodes in the cluster.

Kubectl commands are used to interact and manage Kubernetes objects and the cluster.

Refer to https://www.tutorialspoint.com/kubernetes/kubernetes_kubectl_commands.htm.

A Guide: https://kubernetes.feisky.xyz/.

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

- `kubectl get pods`: check for existing pods;
- `kubectl describe pods`: view what containers are inside that Pod and what images are used to build those containers;
- `kubectl logs $POD_NAME`: retrieve the logs that the application would normally send to STDOUT;
- Execute commands on the container once the pod is up and running:
  - `kubectl exec $POD_NAME env`
  - `kubectl exec -it $POD_NAME bash` (start a bash session in the container)

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
kubectl port-forward redis-master-765d459796-258hz 7000:6379
kubectl port-forward pods/redis-master-765d459796-258hz 7000:6379
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
