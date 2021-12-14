# Cgroup

## Monitoring

Cgroup has a hierarchical structure, you can use `systemctl status` command to see the Cgroup tree.
You can use `systemd-cgtop` to monitor the real-time resource usage of each Cgroup.

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

## Disk I/O Rate Limiting

https://andrestc.com/post/cgroups-io/

Disk I/O limits can be set by using `blkio.throttle.write_bps_device` (for write) and `blkio.throttle.read_bps_device` (for read).
This requires us to specify limits by device, so we must find out our device major and minor version:

```
$ cat /proc/partitions
major minor  #blocks  name

   8        0   10485760 sda
   8        1   10484719 sda1
   8       16      10240 sdb
```

Then we can limit the write bytes per second to 1048576 (1MB/s) on the sda device (8:0) for a docker contaier with id `container_id`:

```
$ echo "8:0 1048576" > /sys/fs/cgroup/blkio/docker/container_id/blkio.throttle.write_bps_device
```

## Network Bandwidth Limiting

https://www.kernel.org/doc/Documentation/cgroup-v1/net_cls.txt
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/resource_management_guide/sec-net_cls

The Network classifier cgroup provides an interface to tag network packets with a class identifier (classid).
The Traffic Controller (tc) can be used to assign different priorities to packets from different cgroups.
Also, Netfilter (iptables) can use this tag to perform actions on such packets.

This `net_cls.classid` value is initialized to 0.
You can write hexadecimal values to `net_cls.classid`; the format for these values is `0xAAAABBBB`; `AAAA` is the major handle number and `BBBB` is the minor handle number.
Reading `net_cls.classid` yields a decimal result.

Example:
```
echo 0x100001 >  /sys/fs/cgroup/net_cls/0/net_cls.classid
	- setting a 10:1 handle.
cat /sys/fs/cgroup/net_cls/0/net_cls.classid
1048577
```

Configuring `tc`:
```
tc qdisc add dev eth0 root handle 10: htb

tc class add dev eth0 parent 10: classid 10:1 htb rate 40mbit
 - creating traffic class 10:1
```
