## Guideline On Performance Monitoring

Tools included: `perf`, `pcm`, `pmu`, and `pcp`

### Intro to `perf`

`perf` is powerful: it can instrument CPU performance counters, tracepoints, kprobes, and uprobes (dynamic tracing).
It is capable of lightweight profiling.
It is also included in the Linux kernel, under `tools/perf`, and is frequently updated and enhanced.

`perf` began as a tool for using the performance counters subsystem in Linux,
and has had various enhancements to add tracing capabilities.

Performance counters are CPU hardware registers that count hardware events such as instructions executed, cache-misses suffered, or branches mispredicted.
They form a basis for profiling applications to trace dynamic control flow and identify hotspots. 
`perf` provides rich generalized abstractions over hardware specific capabilities.
Among others, it provides per task, per CPU and per-workload counters, sampling on top of these and source code event annotation.

Tracepoints are instrumentation points placed at logical locations in code, such as for system calls, TCP/IP events, file system operations, etc.
These have negligible overhead when not in use, and can be enabled by the `perf` command to collect information including timestamps and stack traces. 
`perf` can also dynamically create tracepoints using the kprobes and uprobes frameworks, for kernel and userspace dynamic tracing.
The possibilities with these are endless.

The userspace `perf` command present a simple to use interface with commands like:
- `perf stat`: obtain event counts
- `perf record`: record events for later reporting
- `perf report`: break down events by process, function, etc.
- `perf annotate`: annotate assembly or source code with event counts
- `perf top`: see live event count
- `perf bench`: run different kernel microbenchmarks

### Examples

- Cache-misses counts for each process: `perf stat -e cache-misses -I 1000 -p pid`
    - Output every 1 second;
- Last-level-cache hit rate: `perf stat -e LLC-loads,LLC-load-misses -I 1000`
- Memory bandwidth for all sockets: `perf stat -M Memory_BW -I 1000`
    - This does not work for my case so I use `perf stat -e cas_count_read,cas_count_write -I 1000`
    - According to `hsx-metrics.json`, `BW = (64*(uncore_imc@cas_count_read@ + uncore_imc@cas_count_write@)/1000000000)/ duration_time`

### Intro to `pcm`

https://github.com/opcm/pcm

### Intro to `pmu`

A top-down approach to identify bottlenecks in CPU pipeline.

- https://github.com/andikleen/pmu-tools/wiki/toplev-manual
- http://halobates.de/blog/p/262

### Intro to `pcp`

https://pcp.io/index.html
https://pcp.io/docs/lab.containers.html

#### Using `pcp` on Containers

```
sudo apt install pcp
pcp verify --containers
```

```
$ pminfo --fetch containers.name containers.state.running
containers.name
    inst [0 or "f4d3b90bea15..."] value "sharp_feynman"
    inst [1 or "d43eda0a7e7d..."] value "cranky_colden"
    inst [2 or "252b56e79da5..."] value "desperate_turing"

containers.state.running
    inst [0 or "f4d3b90bea15..."] value 1
    inst [1 or "d43eda0a7e7d..."] value 0
    inst [2 or "252b56e79da5..."] value 1
```

```
$ pmprobe -I network.interface.up
network.interface.up 5 "p2p1" "wlp2s0" "lo" "docker0" "veth2234780"

$ pmprobe -I --container sharp_feynman network.interface.up
network.interface.up 2 "lo" "eth0"

$ pmprobe -I --container f4d3b90bea15 network.interface.up
network.interface.up 2 "lo" "eth0"
```
