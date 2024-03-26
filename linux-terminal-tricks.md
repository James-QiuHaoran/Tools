## Linux Terminal Tricks

### Auto Clean-up Package Configuration Conflicts Problems

In case there are error messages (when executing `apt update`) related to:

```
W: Target Packages (stable/binary-ppc64el/Packages) is configured multiple times in /etc/apt/sources.list:55 and /etc/apt/sources.list.d/docker.list:1
W: Target Packages (stable/binary-all/Packages) is configured multiple times in /etc/apt/sources.list:55 and /etc/apt/sources.list.d/docker.list:1
W: Target Translations (stable/i18n/Translation-en_US) is configured multiple times in /etc/apt/sources.list:55 and /etc/apt/sources.list.d/docker.list:1
```

There's an automatic tool which can be use to clean up those configurations:
- Install the prerequisites: `sudo apt install python3-apt`
- Download the PYZ bundle (`aptsources-cleanup.pyz`) from the [latest release](https://github.com/davidfoerster/aptsources-cleanup/releases/tag/v0.1.7.5.2).
- Mark the PYZ bundle as executable: `chmod a+x aptsources-cleanup.pyz`
- Run `sudo ./aptsources-cleanup.pyz`
- Check `sudo apt update` again to see if the error messages disappear!

### Check The Location of `apt` Installed Libraries/Packages

```
dpkg -L <package_name>
```

Or:

```
apt-file list <package_name>
```

### Install a Package from `.deb` File

```
sudo dpkg -i package_file.deb
```

### Remove an Installed Package Completely

```
$ sudo apt remove package_name
$ sudo apt purge package_name # remove files and configs
$ sudo apt autoclean          # remove old downloaded archive files
```

### Clear Cache

- To free pagecache:

```
# echo 1 > /proc/sys/vm/drop_caches
```

- To free dentries and inodes:

```
# echo 2 > /proc/sys/vm/drop_caches
```

- To free pagecache, dentries and inodes:

```
# echo 3 > /proc/sys/vm/drop_caches
```

Run the above three commands as root, or you can run a series of commands as below:

```
sudo sh -c 'echo 1 >/proc/sys/vm/drop_caches'
sudo sh -c 'echo 2 >/proc/sys/vm/drop_caches'
sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches'
```

Use `free` to check the memory & usage.

### Figure Display

```
feh <image_name>
```

### Pause a Running Process and Run in Background

```
ctrl-z
$ bg
```

`bg` command moves jobs to the background, as if they had been started with `&`.

### Run a Job Remotely (`ssh`) and Then Exit

```
$ nohup long-running-process &
$ exit
```

### Cron Job

https://phoenixnap.com/kb/set-up-cron-job-linux

### DNS Not Working

Check the status of `systemd-resolved` and restart it if needed:

```
sudo systemctl status systemd-resolved.service
sudo systemctl restart systemd-resolved.service
```

If you have error `sudo: unable to resolve host meta: Temporary failure in name resolution`, check if the host name has been set properly:

```
ubuntu@meta:~/owk-actions$ cat /etc/hostname
meta
ubuntu@meta:~/owk-actions$ cat /etc/hosts
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```

Here we need to add an extra line `127.0.1.1 meta` to the file so it should looks like this:

```
ubuntu@meta:~/owk-actions$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 meta

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```

### Compression and Decompression

```
tar -czvf archive_name.tar.gz /path/to/folder
```

- `tar`: This is the command to create or extract tar archives.
- `c`: This option tells tar to create a new archive.
- `z`: This option instructs tar to compress the archive using gzip compression.
- `v`: This option makes tar output verbose information, showing the files being compressed.
- `f`: This option specifies the filename for the archive.
- `archive_name.tar.gz`: This is the name you want to give to the compressed archive file, with the `.tar.gz` extension indicating that it's a gzipped tar file.
- `/path/to/folder`: This is the path to the folder you want to compress. Replace it with the actual path on your system.

```
tar -xzvf archive_name.tar.gz
```

- `x`: This option tells tar to extract the files from the archive.
- `z`: This option instructs tar to decompress the archive using gzip compression.
- `v`: This option makes tar output verbose information, showing the files being extracted.
- `f`: This option specifies the filename of the archive.
