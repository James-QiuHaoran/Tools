# Commands Related to Nvidia GPU Management

## GPU Stats

Wrapper: https://github.com/pmav99/nvsmi/tree/master

```
nvidia-smi --query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu,clocks.max.sm,clocks.current.sm,power.draw --format=csv,noheader,nounits
nvidia-smi --query-compute-apps=pid,process_name,gpu_uuid,gpu_name,used_memory --format=csv,noheader,nounits
```

## GPU Frequency

```
nvidia-smi -q -d CLOCK
nvidia-smi --lock-gpu-clocks=<freq-in-mhz>
```
