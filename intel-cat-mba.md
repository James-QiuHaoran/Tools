# Intel CAT & MBA

Intel Cache Allocation Technology (CAT) and Memory Bandwidth Allocation Technology (MBA) are two techniques provided by some Intel processors for partitioning cache and memory bandwidth.

## Intel CAT

### Code

https://github.com/intel/intel-cmt-cat

### Examples

- `allocation_app_l3cat`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to setting bit mask for L3 CAT classes of service (CLOS) and displaying classes of service (CLOS) and associated bit masks.
- `association_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to association of class of service (CLOS) to cores and displaying class of service (CLOS) and core association.
- `reset_app`: Demonstrates usage of PQoS/Intel(R) RDT library APIs related to resetting all classes of service to system default bit masks (CAT).

### Others

Display supported capabilities of the processor:

```
pqos -d
pqos -D
```
