## SSH Guide

### Forward Display

Enable forwarding graphical display from `dvorak` to your PC:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -X ubuntu@dvorak
```

Enable forwarding graphical display from `dvorak-2-1` to your PC by using `dvorak` as the middle jumping point:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -J ubuntu@dvorak -X ubuntu@dvorak-2-1
```

### GUI Program Forwarding

Forward Firefox program from `dvorak` to your PC:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -f -T -X ubuntu@dvorak firefox
```

Forward Firefox program from `dvorak-2-1` to your PC by using `dvorak` as the middle jumping point:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -J ubuntu@dvorak -f -T -X ubuntu@dvorak-2-1 firefox
```

### Passwordloss Login

On the **local** machine, generate SSH keys:

```
ssh-keygen -t rsa
```

You'll be asked for a location and passphrase. Unless you need to do otherwise, just use the default location (`~/.ssh/`) and **skip the passphrase**.
Hit enter when both prompts appear to continue.

Copy the public key in the `id_rsa.pub` file to the **remote** server in the `.ssh/authorized_keys` file.

Set the correct permission on the **remote** server, otherwise it won't work:

```
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Now test it on the **local** machine:

```
ssh $USER@$REMOTE
```
