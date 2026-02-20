## Quick Usage on Azure Blob

Blob storage account --> Containers (buckets) --> Blobs (objects)

List the containers:

```
az storage container list --account-name hqiublobstorage --auth-mode login --query "[].name" -o tsv
```

Create a container:

```
az storage container create --name opscale --account-name hqiublobstorage --auth-mode login
```

Upload a file:

```
az storage blob upload   --account-name hqiublobstorage   --container-name azure-linux-prebuilt   --name azlinux_hpc_test_rpms_x86_64_0.0.17.tar.gz   --file azlinux_hpc_test_rpms_x86_64_0.0.17.tar.gz   --auth-mode login
```

Verify:

```
az storage blob list   --account-name hqiublobstorage   --container-name azure-linux-prebuilt   --auth-mode login
```

Download a file:

```
az storage blob download   --account-name hqiublobstorage   --container-name azure-linux-prebuilt   --name azlinux_hpc_test_rpms_x86_64_0.0.17.tar.gz   --file azlinux_hpc_test_rpms_x86_64_0.0.17.tar.gz   --auth-mode login
```
