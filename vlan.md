# Virtual LAN

A virtual LAN (VLAN) is any broadcast domain that is partitioned and isolated in a computer network at the data link layer (OSI layer 2).
LAN is the abbreviation for local area network and in this context virtual refers to a physical object recreated and altered by additional logic.
VLANs work by applying tags to network frames and handling these tags in networking systems – creating the appearance and functionality of network traffic that is physically on a single network but acts as if it is split between separate networks.
In this way, VLANs can keep network applications separate despite being connected to the same physical network, and without requiring multiple sets of cabling and networking devices to be deployed.

Under IEEE 802.1Q, the maximum number of VLANs on a given Ethernet network is 4,094 (4,096 values provided by the 12-bit VID field minus reserved values at each end of the range, 0 and 4,095).
This does not impose the same limit on the number of IP subnets in such a network since a single VLAN can contain multiple IP subnets.
IEEE 802.1ad extends the number of VLANs supported by adding support for multiple, nested VLAN tags.
Shortest Path Bridging (IEEE 802.1aq) expands the VLAN limit to 16 million.

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
