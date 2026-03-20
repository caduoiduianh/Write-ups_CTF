# picoCTF Write-up: Bytemancy 3

## Challenge Information

| Field          | Value             |
| -------------- | ----------------- |
| Challenge Name | Bytemancy 3       |
| Category       | General Skills    |
| Difficulty     | Medium            |
| Author         | LT 'SYREAL' JONES |

---

## Description

Can you conjure the right bytes?
The program's source code can be downloaded and the compiled `spellbook` binary is also provided.

Connect to the program using:

```bash
nc green-hill.picoctf.net 53684
```

### Hints

1. `objdump -t spellbook` reveals the symbol table.
2. Send the addresses as **4 raw bytes in little-endian order**.
3. `pwnlib.util.packing.p32()` simplifies crafting payloads.

---

# Analysis

The challenge provides two files:

* `spellbook` — compiled binary
* `app.py` — server-side code

From the `app.py` source code, we can see that the server randomly selects **3 out of 4 magical functions** defined in the binary.

```python
SPELLBOOK_FUNCTIONS = [
    "ember_sigil",
    "glyph_conflux",
    "astral_spark",
    "binding_word",
]
```

Our task is to **send back the memory address of the requested function**.

However, the server expects:

* **Exactly 4 raw bytes**
* **Little-endian format**

If we answer correctly **3 rounds in a row**, the server prints the flag.

---

# Step 1 — Extract Function Addresses

Using `objdump`, we inspect the symbol table of the binary.

```bash
objdump -t spellbook | grep -E 'ember_sigil|glyph_conflux|astral_spark|binding_word'
```

From the output, we obtain the following addresses:

| Function      | Address      |
| ------------- | ------------ |
| ember_sigil   | `0x08049176` |
| glyph_conflux | `0x0804919a` |
| astral_spark  | `0x080491c1` |
| binding_word  | `0x080491e3` |

---

# Step 2 — Convert Address to Little Endian

The server expects **raw bytes**, not ASCII strings.

Example:

Address:

```
0x08049176
```

Little-endian byte order:

```
\x76\x91\x04\x08
```

Sending `"08049176"` would **fail** because the server reads **raw bytes**, not text.

---

# Step 3 — Automating with pwntools

Instead of manually crafting payloads, we can automate the process using **pwntools**.

The function:

```python
p32()
```

converts an integer into **32-bit little-endian bytes**.

---

# Solver Script

```
Check out solve.py
```

---

# Execution

Running the solver:

```bash
python3 solve.py
```

Example output:

```bash
[+] Opening connection to green-hill.picoctf.net on port 53684: Done
[*] Round 1: Server is asking for the address of 'astral_spark'
[+] Sending payload: b'\xc1\x91\x04\x08'
[*] Round 2: Server is asking for the address of 'glyph_conflux'
[+] Sending payload: b'\x9a\x91\x04\x08'
[*] Round 3: Server is asking for the address of 'binding_word'
[+] Sending payload: b'\xe3\x91\x04\x08'
[*] Switching to interactive mode
picoCTF{0bjdump_m4g1c_c8c1af72}
```

---

# Flag

```
picoCTF{0bjdump_m4g1c_c8c1af72}
```

---

# Key Takeaways

* `objdump -t` can reveal **symbol addresses** in binaries.
* Network services sometimes require **raw binary input**, not text.
* **Little-endian encoding** is critical when interacting with low-level programs.
* `pwntools` simplifies exploitation tasks like byte packing and remote interaction.

---

# Tools Used

* `objdump`
* `pwntools`
* `netcat`
