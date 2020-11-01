# Virtual LAN

A virtual LAN (VLAN) is any broadcast domain that is partitioned and isolated in a computer network at the data link layer (OSI layer 2).
LAN is the abbreviation for local area network and in this context virtual refers to a physical object recreated and altered by additional logic.
VLANs work by applying tags to network frames and handling these tags in networking systems – creating the appearance and functionality of network traffic that is physically on a single network but acts as if it is split between separate networks.
In this way, VLANs can keep network applications separate despite being connected to the same physical network, and without requiring multiple sets of cabling and networking devices to be deployed.

Under IEEE 802.1Q, the maximum number of VLANs on a given Ethernet network is 4,094 (4,096 values provided by the 12-bit VID field minus reserved values at each end of the range, 0 and 4,095).
This does not impose the same limit on the number of IP subnets in such a network since a single VLAN can contain multiple IP subnets.
IEEE 802.1ad extends the number of VLANs supported by adding support for multiple, nested VLAN tags.
Shortest Path Bridging (IEEE 802.1aq) expands the VLAN limit to 16 million.

## Packet Priority in VLAN

IEEE 802.1Q, often referred to as Dot1q, is the networking standard that supports virtual LANs (VLANs) on an IEEE 802.3 Ethernet network.
The standard defines a system of VLAN tagging for Ethernet frames and the accompanying procedures to be used by bridges and switches in handling such frames.
The standard also contains provisions for a quality-of-service prioritization scheme commonly known as IEEE 802.1p.

### IEEE 802.1p

IEEE 802.1p is the name of a task group responsible for adding traffic class expediting and dynamic multicast filtering to the IEEE 802.1D standard.
Essentially, the task group provides a mechanism for implementing quality-of-service (QoS) at the media access control (MAC) level.
The QoS technique developed by the working group, also known as class of service (CoS), is a 3-bit field called the Priority Code Point (PCP) within an Ethernet frame header when using VLAN tagged frames as defined by IEEE 802.1Q.
It specifies a priority value of between 0 and 7 inclusive that can be used by QoS disciplines to differentiate traffic.

### IEEE Recommendation

|PCP Value|Priority|Acronym|Traffic Types|
|---------|--------|-------|-------------|
|1	      |0 (lowest) |BK	 |Background   |
|0	      |1 (default)|BE	 |Best Effort  |
|2	      |2	        |EE	 |Excellent Effort|
|3	      |3	        |CA	 |Critical Applications|
|4	      |4	        |VI	 |Video, < 100 ms latency and jitter|
|5	      |5	        |VO	 |Voice, < 10 ms latency and jitter|
|6	      |6	        |IC	 |Internetwork Control|
|7	      |7 (highest)|NC  |Network Control|

## How to Use

### Configure a VLAN Using the `vconfig` Command

Add a VLAN with ID 5 for `eth0` interface:

```
vconfig add eth0 5
```

The `vconfig add` command creates a VLAN-device on `eth0` which results into `eth0.5` interface.
You can use normal `ifconfig` command to see device information:

```
ifconfig eth0.5
```

Use `ifconfig` command to assign IP address to VLAN interface:

```
ifconfig eth0.5 192.168.1.100 netmask 255.255.255.0 broadcast 192.168.1.255 up
```

Get detailed information about VLAN interface:

```
cat /proc/net/vlan/config
cat /proc/net/vlan/eth0.5
```

### Delete a VLAN interface Using the `vconfig` Command

```
ifconfig eth0.5 down
vconfig rem eth0.5
```
