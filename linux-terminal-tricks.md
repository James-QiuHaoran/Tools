## Linux Terminal Tricks

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
