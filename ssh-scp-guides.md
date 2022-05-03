## SSH/SCP Guide

### Forward Display

Enable forwarding graphical display from `dvorak` to your PC:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -X ubuntu@dvorak
```

Enable forwarding graphical display from `dvorak-2-1` to your PC by using `dvorak` as the middle jumping point:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -J ubuntu@dvorak -X ubuntu@dvorak-2-1
```

Difference bewteen `-X` and `-Y`:

- If you use `ssh -X remotemachine`, the remote machine is treated as an **untrusted** client. So your local client sends a command to the remote machine and receives the graphical output. If your command violates some security settings you'll receive an error instead.
- If you use `ssh -Y remotemachine`, the remote machine is treated as a **trusted** client. This last option can open security problems. Because other graphical (X11) clients could sniff data from the remote machine (make screenshots, do keylogging and other nasty stuff) and it is even possible to alter those data.


### GUI Program Forwarding

Forward Firefox program from `dvorak` to your PC:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -f -T -X ubuntu@dvorak firefox
```

Forward Firefox program from `dvorak-2-1` to your PC by using `dvorak` as the middle jumping point:

```
jamesqiu@jamesqiu-OptiPlex-7050:~$ ssh -J ubuntu@dvorak -f -T -X ubuntu@dvorak-2-1 firefox
```

### Passwordless Login

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

### Execute Commands Remotely

```
ssh user1@server1 command1
ssh user1@server1 'command2'

# pipe
ssh user1@server1 'command1 | command2'

# multiple commands (must enclose in quotes, ' or ")
ssh admin@box1 "command1; command2; command3"
```

### SCP

Pass a literal escape to use the wild card:

```
scp 'SERVERNAME:/DIR/\*' .
```
