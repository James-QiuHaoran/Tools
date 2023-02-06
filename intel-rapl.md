## Intel RAPL

RAPL stand for Running Average Power Limit, it is a feature of recent Intel processors that provide the energy consumption of the processor.

RAPL provides a set of counters providing **energy and power consumption** information. RAPL is not an analog power meter but rather uses a software power model. This software power model estimates energy usage using hardware performance counters and I/O models. Based on our measurements, they match actual power measurements.

RAPL provides a way to **set power limits on processor packages and DRAM**. This will allow a monitoring and control program to dynamically limit max average power to match its expected **power and cooling budget**. In addition, power limits in a rack enable power budgeting across the rack distribution. By dynamically monitoring the feedback on power consumption, power limits can be reassigned based on use and workloads. Because multiple bursts of heavy workloads will eventually cause the ambient temperature to rise, reducing the heat transfer rate, one uniform power limit can’t be enforced. **RAPL provides a way to set short-term and longer-term averaging windows for power limits. These window sizes and power limits can be adjusted dynamically.**

Check if Intel RAPL is supported on your machine: `cat /sys/class/powercap/intel-rapl/enabled`

Support References: https://web.eece.maine.edu/~vweaver/projects/rapl/rapl_support.html

Paper: Power-Management Architecture of the Intel Microarchitecture Code-Name Sandy Bridge (IEEE Micro, March/April 2012)

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

Note that you cannot get readings for individual processes; the results are for the **entire CPU socket**.

There were at one point 4 ways to read RAPL results on Linux:

- Reading the files under `/sys/class/powercap/intel-rapl/intel-rapl:0` using the `powercap` interface. This required no special permissions, and was introduced in Linux 3.13.
- Using the `perf_event` interface with Linux 3.14 or newer. This requires root or a paranoid less than 1 (as do all system-wide measurements with `-a`): `sudo perf stat -a -e "power/energy-cores/" /bin/ls`
    - Available events can be found via `perf list` or under the directory `/sys/bus/event_source/devices/power/events/`
- Using raw access to the underlying MSRs under `/dev/msr`. This requires **root access**. Some HPC tools will attempt to use this interface to bypass the kernel, but the kernel developers want to make raw MSR access go away, as there are many questionable things you can do to a system with raw MSR access. There have been attempts to make alternate drivers that whitelist the MSRs that can be used, but they are probably going away in the future too.
    - The `msr` driver is not auto-loaded. On modular kernels you might need to run `modprobe msr` (and then check `lsmod | grep msr`)
    - https://github.com/intel/msr-tools
    - [Userspace Access without perf](https://github.com/deater/uarch-configure/blob/master/rapl-read/rapl-read.c)
- An AMD RAPL driver without permission checks was available under the kernel `hwmon` interface, but it was removed in Linux 5.13 (9049572fb) also due to security concerns.

References:
- https://web.eece.maine.edu/~vweaver/projects/rapl/
- https://powerapi-ng.github.io/rapl.html

### Power Capping

Call `powercap_register_control_type()` to register the control type object.

Call `powercap_register_zone()` to register a power zone (under a given control type), either as a top-level power zone or as a subzone of another power zone registered earlier. The number of constraints in a power zone and the corresponding callbacks have to be defined before calling `powercap_register_zone()` to register that zone.

To free a power zone, call `powercap_unregister_zone()`.

To free a control type object, call `powercap_unregister_control_type()`.

Detailed API can be generated using kernel-doc on `include/linux/powercap.h`.

References:
- https://www.kernel.org/doc/html/latest/power/powercap/powercap.html

### Command Line Tool - `powercap-info`

[https://manpages.ubuntu.com/manpages/bionic/man1/powercap-info.1.html](https://manpages.ubuntu.com/manpages/bionic/man1/powercap-info.1.html)

[https://manpages.ubuntu.com/manpages/bionic/man1/rapl-info.1.html](https://manpages.ubuntu.com/manpages/bionic/man1/rapl-info.1.html)

```
powercap-info -p intel-rapl
              Print all RAPL zones.

powercap-info -p intel-rapl -z 0
              Print only zone 0, which is usually named package-0.

powercap-info -p intel-rapl -z 0:1
              Print zone 0, subzone 1, which is usually the uncore or dram subzone of package-0, depending on the system.

powercap-info -p intel-rapl -z 0 -c 1
              Print zone 0, constraint 1, which is usually the short-term constraint for package-0.

powercap-info -p intel-rapl -z 0 -j
              Print the energy counter for zone 0, which is usually named package-0.

powercap-info -p intel-rapl -z 1:0 -c 0 -l
              Print the power limit for zone 1, subzone 0, and constraint 0, which is usually the long-term constraint for the core subzone of package-1 (a multi-socket system).
```

### Command Line Tool - `powercap-set`

[https://manpages.ubuntu.com/manpages/bionic/man1/powercap-set.1.html](https://manpages.ubuntu.com/manpages/bionic/man1/powercap-set.1.html)

[https://manpages.ubuntu.com/manpages/bionic/man1/rapl-set.1.html](https://manpages.ubuntu.com/manpages/bionic/man1/rapl-set.1.html)

```
powercap-set -p intel-rapl -z 0 -e 1
              Enable zone 0, which is usually named package-0.

powercap-set -p intel-rapl -z 0:1 -e 1
              Enable zone 0, subzone 1, which is usually the uncore or dram subzone of package-0, depending on the system.

powercap-set -p intel-rapl -z 0 -c 1 -l 25000000
              Set a power cap of 25 Watts (25000000 uW) on zone 0, constraint 1, which is usually the short-term constraint for package-0.

powercap-set -p intel-rapl -z 1:0 -c 0 -l 15000000 -s 976
              Set a power cap of 15 Watts (15000000 uW) and a time window of 976 microseconds on zone 1, subzone 0, constraint 0, which is usually the long-term  (and only) constraint for the core subzone of package-1 (a multi-socket system).
```
