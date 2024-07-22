# Conda

Conda is an open-source, cross-platform, language-agnostic package manager and environment management system.

## Create a Conda Environment

```
conda create -n myenv python=3.9 -y
conda activate myenv
conda deactivate
```

## Package Management

List all packages installed into the environment `myenv`:

```
conda list
```

Install a package, e.g., `cuda 12.1`:

```
conda install nvidia/label/cuda-12.1.0::cuda
```

## Export/Import Packages

```
conda list -e > requirements.txt
conda create --name <env> --file requirements.txt
```
