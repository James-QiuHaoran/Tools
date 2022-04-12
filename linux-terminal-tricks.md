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
