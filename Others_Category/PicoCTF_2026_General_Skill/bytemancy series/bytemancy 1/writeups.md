# bytemancy 1

**Category:** General Skills  
**Difficulty:** Very Easy  
**Author:** LT 'SYREAL' JONES  

---

## Challenge Description
Can you conjure the right bytes? The program's source code can be downloaded here.

Connect to the program with netcat:

```
nc foggy-cliff.picoctf.net 49714 ( Check your instance port )
```

---

## Hints
1. No copy-pasta, please - use Python!

---

# Write-up

## 1. Analyzing the Source Code

Reviewing the provided `app.py` script shows that this challenge is a continuation of **bytemancy 0**, but with a larger input requirement.

Relevant code snippet:

```python
user_input = input("==> ")
if user_input == "\x65"*1751:
  print(open("./flag.txt", "r").read())
```

Explanation:

- `\x65` represents the hexadecimal byte `0x65`.
- ASCII `0x65` corresponds to the character **`e`**.
- The expression `"\x65"*1751` means the program expects **the character `e` repeated 1751 times**.

Therefore, the required input is:

```
eeeeee.... (1751 times)
```

---

## 2. Method A: Manual Approach

One way to solve the challenge is to manually generate a string of **1751 `e` characters** and paste it into the netcat prompt.

Example:

```bash
nc foggy-cliff.picoctf.net 49714
```

When prompted:

```
==>
```

Paste the generated string:

```
eeeeeeeeee.... (1751 e's)
```

This satisfies the condition and the program prints the flag.

However, this approach is inefficient and error-prone.

---

## 3. Method B: Python One-Liner (Intended Solution)

A more reliable method is to generate the required input using a **Python one-liner** and pipe it directly into the netcat connection.

Command:

```bash
python3 -c "print('e' * 1751)" | nc foggy-cliff.picoctf.net 49714
```

Explanation:

- `python3 -c` executes Python code directly from the command line
- `'e' * 1751` generates a string containing **1751 `e` characters**
- `|` pipes the output into the `nc` connection

This sends the correct input instantly and triggers the flag output.

---

## Flag

```
picoCTF{h0w_m4ny_e's???_e0d51f4b}
```

---

## Key Takeaway

This challenge reinforces several useful command-line techniques:

- Generating large strings programmatically
- Using **Python one-liners** for quick payload creation
- Using **pipes (`|`)** to send generated input directly into network connections

These techniques are frequently used in CTF challenges involving **network services and scripted inputs**.