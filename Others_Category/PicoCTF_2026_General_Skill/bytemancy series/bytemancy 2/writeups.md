# picoCTF Writeup: bytemancy 2

## Challenge Information
* **Category:** General Skills  
* **Difficulty:** Easy  
* **Author:** LT 'SYREAL' JONES  

---

## Description

Can you conjure the right bytes? The program's source code can be downloaded here.

Connect to the program with netcat:

```
nc lonely-island.picoctf.net 58221
```

---

## Hints

1. Use pwntools to send raw bytes over the network.  
2. There's no way to print these bytes.

---

# Analysis

By analyzing the provided `app.py` source code, we can see exactly what the server expects.

```python
import sys

while(True):
  try:
    print('⊹──────[ BYTEMANCY-2 ]──────⊹')
    print("☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐")
    print()
    print('Send me the HEX BYTE 0xFF 3 times, side-by-side, no space.')
    print()
    print("☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐☉⟊☽☈⟁⧋⟡☍⟐")
    print('⊹─────────────⟡─────────────⊹')
    print('==> ', end='', flush=True)

    user_input = sys.stdin.buffer.readline().rstrip(b"\n")

    if user_input == b"\xff\xff\xff":
      print(open("./flag.txt", "r").read())
      break
    else:
      print("That wasn't it. I got: " + str(user_input))
      print()
      print()
      print()

  except Exception as e:
    print(e)
    break
```

The script reads input directly from the **standard input buffer** using:

```
sys.stdin.buffer.readline()
```

This means the program compares **raw bytes**, not normal ASCII characters.

The condition we must satisfy is:

```
b"\xff\xff\xff"
```

This corresponds to three consecutive bytes with value **0xFF**.

---

## Why Netcat Alone Fails

If we simply connect with netcat and type something like:

```
FF FF FF
```

or

```
\xff\xff\xff
```

the server receives **ASCII characters**, not raw bytes.

For example:

```
b"\\xff\\xff\\xff"
```

instead of:

```
b"\xff\xff\xff"
```

Therefore the comparison fails.

Additionally, the hint **“There's no way to print these bytes”** refers to the fact that **0xFF is not a printable ASCII character**, so we cannot reliably type it directly from the keyboard.

---

# Solution

To solve this challenge we need to send **raw bytes** over the socket.

The hint suggests using **pwntools**, which makes this easy.

Create a file called `solve.py`. ( Check it more specific on script)

---

# Execution

Run the script:

```bash
python3 solve.py
```

Example output:

```
[+] Opening connection to lonely-island.picoctf.net on port 58221: Done
[+] Receiving all data: Done
[*] Closed connection to lonely-island.picoctf.net port 58221
picoCTF{3ff5_4_d4yz_86a39d4b}
```

---

# Flag

```
picoCTF{3ff5_4_d4yz_86a39d4b}
```

---

# Key Takeaway

This challenge demonstrates the difference between:

- **Printable characters (ASCII)**
- **Raw byte values**

Important concepts:

- `sys.stdin.buffer` reads **raw bytes**
- Some byte values like **0xFF** are **not printable**
- Tools like **pwntools** are useful for sending exact binary payloads over network sockets