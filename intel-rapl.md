## Intel RAPL

RAPL stand for Running Average Power Limit, it is a feature of recent Intel processors that provide the energy consumption of the processor.

The RAPL formula is designed to mesure power consumption of domains (CPU or RAM) in real time.

Check if Intel RAPL is supported on your machine: `cat /sys/class/powercap/intel-rapl/enabled`

Support References: https://web.eece.maine.edu/~vweaver/projects/rapl/rapl_support.html

## Linux Power Capping Framework

The power-capping framework provides a consistent interface between the kernel and the user space, allowing power-capping drivers to expose the settings to the user space uniformly.

Reference: [https://www.kernel.org/doc/html/latest/power/powercap/powercap.html](https://www.kernel.org/doc/html/latest/power/powercap/powercap.html)

The framework exposes **power-capping devices** to user space via `sysfs` as a tree of objects. The objects at the root level of the tree represent “control types,” which correspond to different methods of power capping. For example, the `intel-rapl` control type represents the **Intel Running Average Power Limit (RAPL)** technology, whereas the `idle-injection` control type corresponds to idle injection for controlling power.

### Install Packages

Utilities for accessing the power-capping Linux kernel feature:

```
sudo apt install powercap-utils
```

This package contains utilities for accessing the `powercap` Linux kernel feature through `sysfs`. Specifically, it provides `powercap-info` and `powercap-set` for generic access to `powercap` control types, and `rapl-info` and `rapl-set` for managing Intel RAPL implementations.

### Measurement

TODO

References:
- https://web.eece.maine.edu/~vweaver/projects/rapl/
- https://powerapi-ng.github.io/rapl.html

### Power Capping

TODO

References:
- https://www.kernel.org/doc/html/latest/power/powercap/powercap.html
