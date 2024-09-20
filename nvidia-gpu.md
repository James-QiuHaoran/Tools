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

## GPU Utilization

Note that nvidia-smi only reports coarse-grained GPU utilization
	- 50% means that 50% of the time that at least one of the SM cores is active

One option is to use nsys:
	- https://docs.nvidia.com/nsight-systems/InstallationGuide/index.html
	- https://developer.nvidia.com/blog/measuring-the-gpu-occupancy-of-multi-stream-workloads/

For example:

```
sudo nsys profile --gpu-metrics-devices=0 /home/azrsadmin/.conda/envs/lmm/bin/python test-stable-diffusion.py
nsys stats ./report1.nsys-rep
```

There's also a profile reader that can give us the average GPU utilization across the duration of application execution:
	- https://github.com/James-QiuHaoran/lmm-benchmarks/blob/main/nsys-reader.py

Formally, the quantity reported is an average of SM activity. 50% may mean that all SMs are active 50% of the time, or 50% of the SMs are active 100% of the time, or anything in between, but in practice, our earlier definition prevails.

The other option is to use DCGM:
- https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/getting-started.html![image](https://github.com/user-attachments/assets/f7de583e-70a9-4986-b234-9134d1d6a3ce)

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

## Check NVIDIA Driver Version

```
cat /proc/driver/nvidia/version
cat /sys/module/nvidia/version
```

## NVIDIA Drivers are Troublesome

Consider just forbidding the automatic update of NVIDIA packages by modifying `/etc/apt/sources.list.d/` files.
In my experience, the best way is to simply hold the packages to prevent them from automatic updates by executing the commands below:

```
sudo apt-mark hold nvidia-dkms-<version_number>
sudo apt-mark hold nvidia-driver-<version_number>
sudo apt-mark hold nvidia-utils-<version_number>
```

To show a list of packages that are on hold: `apt-mark showhold`
