# Write-up: MultiCode

## Challenge Information
* **CTF:** picoCTF
* **Name:** MultiCode
* **Category:** General Skills
* **Difficulty:** Easy
* **Author:** YAHAYA MEDDY

## Description
We intercepted a suspiciously encoded message, but it’s clearly hiding a flag. No encryption, just multiple layers of obfuscation. Can you peel back the layers and reveal the truth?

Download the message.

## Hints
1. The flag has been wrapped in several layers of common encodings such as ROT13, URL encoding, Hex, and Base64. Can you figure out the order to peel them back?
2. A tool like CyberChef can be interesting.

---

## Solution & Reasoning

Based on the description and hints, we know the flag isn't encrypted but rather obfuscated using multiple common encoding layers. The best tool for this type of challenge is **[CyberChef](https://gchq.github.io/CyberChef/)** – the "Swiss Army Knife" for decoding.

After downloading the `message` file (or grabbing the initial string), we start peeling back the layers one by one:

### Step 1: Analyze the initial string & Base64 Decode
* **Input:** `NjM3NjcwNjI1MDQ3NTMyNTM3NDI2MTcyNjY2NzcyNzE1ZjcyNjE3MDMwNzE3NjYxNzQ1ZjczNzM2ZjM2NzA2ZTZlMzIyNTM3NDQ=`
* **Reasoning:** The string consists only of alphanumeric characters (uppercase/lowercase) and ends with an `=` padding character. This is a classic signature of **Base64** encoding.
* **Action (CyberChef Recipe):** `From Base64`
* **Output:** `637670625047532537426172666772715f72617030717661745f73736f36706e6e32253744`

### Step 2: Hexadecimal (Hex) Decode
* **Reasoning:** The result from Step 1 is a string consisting entirely of digits from `0-9` and letters from `a-f`. This indicates it's a **Hexadecimal** string.
* **Action (CyberChef Recipe):** `From Hex`
* **Output:** `cvpbPGS%7Barfgrq_rap0qvat_sso6pnn2%7D`

### Step 3: URL Decode
* **Reasoning:** Looking at the string from Step 2, we notice characters like `%7B` and `%7D`. If you are familiar with web encodings, you'll immediately recognize these as the `{` and `}` characters, respectively, encoded using **URL Encoding**.
* **Action (CyberChef Recipe):** `URL Decode`
* **Output:** `cvpbPGS{arfgrq_rap0qvat_sso6pnn2}`

### Step 4: ROT13 Decode
* **Reasoning:** The decoded string now has the format `xxxxXXX{...}`. This looks exactly like the standard flag format: `picoCTF{...}`. If we count the alphabetical distance from `c` to `p`, `v` to `i`, etc., we find they are exactly 13 characters apart. This is a clear indicator of the **ROT13** substitution cipher.
* **Action (CyberChef Recipe):** `ROT13` (Amount: 13)
* **Output (Flag):** `picoCTF{nested_enc0ding_ffb6caa2}`

---

## Final Flag
**`picoCTF{nested_enc0ding_ffb6caa2}`**