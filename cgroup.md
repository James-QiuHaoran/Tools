# Cgroup

## CPU Sub-system

Get the full ID of the container:

```
docker ps -q --no-trunc | grep cd5469264e5f
```

Cgroup directory location:

```
/sys/fs/cgroup/cpu/docker/cd5469264e5ffd983e532aabcaa8378e2a37f3c8d76d7fe4312c8783dca10bc7
```

### Pin Container to Cores

Location:

```
/sys/fs/cgroup/cpuset/docker/cd5469264e5ffd983e532aabcaa8378e2a37f3c8d76d7fe4312c8783dca10bc7/cpuset.cpus
```
