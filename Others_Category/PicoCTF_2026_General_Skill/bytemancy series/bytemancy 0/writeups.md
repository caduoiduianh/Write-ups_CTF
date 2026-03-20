# bytemancy 0

**Category:** General Skills  
**Difficulty:** Very Easy  
**Author:** LT 'SYREAL' JONES  

---

## Challenge Description
Can you conjure the right bytes? The program's source code can be downloaded here.

Connect to the program with netcat:

```
nc candy-mountain.picoctf.net 54184 ( check this port if create an instance )
```

---

## Hints
1. Solving this with a one-liner will help with the next challenge in this series.

---

# Write-up

## 1. Analyzing the Source Code

Reviewing the provided `app.py` script reveals the core logic of the challenge.

Relevant code snippet:

```python
if user_input == "\x65\x65\x65":
  print(open("./flag.txt", "r").read())
```

Explanation:

- `\x65` is a hexadecimal byte representation.
- Hex `0x65` corresponds to **decimal 101**.
- ASCII decimal **101** corresponds to the character **`e`**.

Therefore:

```
\x65\x65\x65
```

is equivalent to:

```
eee
```

The program will print the flag only if the user input is exactly **three characters `eee`**.

---

## 2. Executing the Solution

Connect to the challenge instance using **netcat**:

```bash
nc candy-mountain.picoctf.net 54184
```

When the prompt appears:

```
==>
```

Enter:

```
eee
```

If the input matches the condition, the program prints the flag.

---

## 3. Important Note

Be mindful of your keyboard's input method (such as a **Telex IME**).

If you type `eee` while an IME is active, the first `e` might temporarily convert into a character such as `ê`. This can cause the terminal to send **unexpected Unicode bytes** instead of standard ASCII characters.

As a result, the server may receive something like:

```
êee
```

instead of:

```
eee
```

This causes the comparison in the Python script to fail.

To avoid this issue:

- Disable the Vietnamese IME temporarily  
- Ensure you are sending **exactly three ASCII `e` characters**

---

## Flag

```
picoCTF{pr1n74813_ch4r5_15ddc7a7}
```

---

## Key Takeaway

This challenge demonstrates how **byte representations in Python strings** work:

- `\xNN` represents a **hexadecimal byte**
- `\x65` corresponds to ASCII character **`e`**

Understanding ASCII, hexadecimal, and byte representations is an important foundation for later challenges involving **binary data and raw byte input**.