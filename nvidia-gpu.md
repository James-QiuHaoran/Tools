# Commands Related to Nvidia GPU Management

## NVIDIA SMI

The NVIDIA System Management Interface (`nvidia-smi`) is a command line utility, based on top of the NVIDIA Management Library (NVML), intended to aid in the management and monitoring of NVIDIA GPU devices. 

### GPU Stats

Wrapper: https://github.com/pmav99/nvsmi/tree/master

```
nvidia-smi --query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu,clocks.max.sm,clocks.current.sm,power.draw --format=csv,noheader,nounits
nvidia-smi --query-compute-apps=pid,process_name,gpu_uuid,gpu_name,used_memory --format=csv,noheader,nounits
```

### GPU Frequency

```
nvidia-smi -q -d CLOCK
nvidia-smi --lock-gpu-clocks=<freq-in-mhz>
```

## CUDA

CUDA is a parallel computing platform and programming model invented by NVIDIA.
CUDA was developed for the following two reasons:

- Provides a small set of extensions to standard programming languages, like C, that enable a straightforward implementation of parallel algorithms
- Supports hetergeneous computation where applications use both the CPU and GPU which are treated as separate devices so that there's no memory contention and can support simultaneous computations

## Other GPU Monitoring Tools

- `gpustat`: `pip install --user gpustat`
- `nvtop`: `sudo apt install nvtop` (may cause driver and library version mismatch)
- `nvitop`: `pip install --user nvitop`; `nvitop -1`

For `pip` installation, one needs to add to `PATH`: `export PATH=$PATH:${HOME}/.local/bin`.

## NVIDIA Drivers are Troublesome

Consider just forbidding the automatic update of NVIDIA packages by modifying `/etc/apt/sources.list.d/` files.
In my experience, the best way is to simply hold the packages to prevent them from automatic updates by executing the commands below:

```
sudo apt-mark hold nvidia-dkms-<version_number>
sudo apt-mark hold nvidia-driver-<version_number>
sudo apt-mark hold nvidia-utils-<version_number>
```

To show a list of packages that are on hold: `apt-mark showhold`
