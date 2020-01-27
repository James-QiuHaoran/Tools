## SSH Guide

### GUI Program Forwarding

Forward Firefox program from `dvorak` to your PC:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -f -T -X ubuntu@dvorak firefox
```

Forward Firefox program from `dvorak-2-1` to your PC by using `dvorak` as the middle jumping point:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -J ubuntu@dvorak -f -T -X ubuntu@dvorak-2-1 firefox
```
