# CTF Write-up: Undo (picoCTF)

## Challenge Information
* **Platform:** picoCTF
* **Challenge Name:** Undo
* **Category:** General Skills
* **Difficulty:** Easy
* **Author:** YAHAYA MEDDY

## Objective
Connect to the server via Netcat (`nc`), and use basic Linux commands to step-by-step reverse a series of text transformations to recover the original flag.

## Provided Hints & Resources
The challenge provided the following hint regarding text manipulation tools:

> "For text translation and character replacement, see https://man7.org/linux/man-pages/man1/tr.1.html."

---

## Walkthrough

First, launch the instance and connect to the server as instructed:

```bash
nc foggy-cliff.picoctf.net 55197
```

*(Note: The port might change depending on your specific instance.)*

The server presents an interactive **5-step challenge**. At each step, you receive a transformed string and a hint.

---

## Step 1: Base64 Decoding

**Hint:** Base64 encoded the string.

**Analysis:**  
The current string is Base64 encoded. The standard Linux syntax for decoding is `base64 -d`. However, the challenge blocks the exact string `base64 -d`. We can bypass this filter by wrapping the parameter in quotes.

**Command executed:**

```bash
base64 '-d'
```

---

## Step 2: Reverse the String

**Hint:** Reversed the text.

**Analysis:**  
The text has been reversed from right to left. The most convenient Linux command for this is `rev`.

**Command executed:**

```bash
rev
```

---

## Step 3: Replace `-` with `_`

**Hint:** Replaced underscores with dashes.

**Analysis:**  
Underscores `_` were replaced with dashes `-`. To revert them we use the `tr` (translate) command.

**Command executed:**

```bash
tr "-" "_"
```

---

## Step 4: Replace Parentheses with Curly Braces

**Hint:** Replaced curly braces with parentheses.

**Analysis:**  
Curly braces `{}` were replaced with parentheses `()`. Again we use `tr` to restore the normal flag format.

**Command executed:**

```bash
tr "()" "{}"
```

---

## Step 5: ROT13 Decoding

**Hint:** Applied ROT13 to letters.

**Analysis:**  
The resulting string looks like:

```
cvpbPGS{...}
```

The prefix `cvpbPGS` is **picoCTF** encoded with **ROT13**.  
ROT13 shifts each letter **13 positions** in the alphabet. Since the alphabet has **26 letters**, applying ROT13 again decodes it.

**Command executed:**

```bash
tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

---

## The Flag

After executing the command in step 5, the final layer of transformation is removed and the original flag appears:

```
picoCTF{Revers1ng_t3xt_Tr4nsf0rm@t10ns_8deed4b6}
```
