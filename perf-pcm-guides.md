## Guideline On Using `perf` and `pcm`

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
