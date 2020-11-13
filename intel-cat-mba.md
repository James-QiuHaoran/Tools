# Intel CAT & MBA

Intel Cache Allocation Technology (CAT) and Memory Bandwidth Allocation Technology (MBA) are two techniques provided by some Intel processors for partitioning cache and memory bandwidth.

## Intel CAT

### Code

https://github.com/intel/intel-cmt-cat

### Build and Install (on Linux)

CMT, MBM and CAT are configured using Model Specific Registers (MSRs) to measure occupancy, set up the class of service masks and manage the association of the cores/logical threads to a class of service.
The `pqos` software executes in user space, and access to the MSRs is obtained through a standard Linux interface.
The virtual file system structure `/dev/cpu/CPUNUM/msr` provides an interface to read and write the MSRs.
The `msr` file interface is protected and requires root privileges. The `msr` driver might not be auto-loaded and on some modular kernels the driver may need to be loaded manually:

```
$ modprobe msr
```

In the repo directory:

```
$ make
$ make install
```

### Examples

Examples are given in three different programming languages: C, Python, and Perl.
Most of the examples are similar: allocate LLC partition, associate cores to a partition, and reset the partition configurations.
In addition, there's examples that is to **monitor cache and memory bandwidth per core or per process**. But this is hardware-dependent, which means only supported events will be shown.

For examples in C, build binary files by `make`.

- `allocation_app_l3cat`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to setting bit mask for L3 CAT classes of service (CLOS) and displaying classes of service (CLOS) and associated bit masks.
- `association_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to association of class of service (CLOS) to cores and displaying class of service (CLOS) and core association.
- `reset_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to resetting all classes of service to system default bit masks (CAT).
- `monitor_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to monitoring events like cache occupancy, local memory bandwidth usage, and remote memory bandwidth usage. It operates in user space and uses PQoS/Intel(R) RDT and C libraries only.

Note that all apps operate in user space and use PQoS/Intel(R) RDT and C libraries only.

#### Configure CLOSs

One can use `./allocation_app_l3cat <CLOS#> <bit-mask>` to configure cache allocation for each CLOS.
The bit-masks are represented as hex-numbers. For example, a mask enabling a CLOS to use the first 2 cache ways (bits) of the LLC is then `0xc0000`.
And let's say if you want to allocate this to `CLOS0`, then you can execute `sudo ./allocation_app_l3cat 0 0xc0000`.
The default bit-mask for a CLOS is `0xfffff`, which means it can use all cache ways without any constraints.

#### Associate Cores to a CLOS

By default, all cores are associated to `CLOS0`.
One can use `./association_app <CLOS#> <core1> <core2>...` to configure the mapping between cores to CLOSs.
For example, if you want to pin core number 0, 7, 13, 24 to `CLOS1`, then you can execute `sudo ./association_app 1 0 7 13 24`.

### Others

Display supported capabilities of the processor:

```
pqos -d
pqos -D
```

## Intel MBA

Intel MBA is sharing the CLOSs with CAT, though they may have different number of available CLOSs (the overlapped CLOSs have the same association to cores).
For example, if you associate core 0-4 to CLOS0, then core 0-4 is using the same configuration of CAT and MBA for CLOS0.

### Examples

Since Intel MBA is sharing the same CLOSs with CAT, the following is the same as CAT:

- `association_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to association of class of service (CLOS) to cores and displaying class of service (CLOS) and core association.
- `reset_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to resetting all classes of service to system default bit masks (CAT).
- `monitor_app` - Demonstrates usage of PQoS/Intel(R) RDT library APIs related to monitoring events like cache occupancy, local memory bandwidth usage, and remote memory bandwidth usage. It operates in user space and uses PQoS/Intel(R) RDT and C libraries only.

The difference is the allocation:

- `allocation_app_mba`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to setting MBA delay values for classes of service (CLOS) and displaying classes of service (CLOS) and associated delay values.

Note that all apps operate in user space and use PQoS/Intel(R) RDT and C libraries only.
