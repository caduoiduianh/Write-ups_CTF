from pwn import *

# 1. Dictionary of function addresses extracted via objdump earlier
symbols = {
    "ember_sigil": 0x08049176,
    "glyph_conflux": 0x0804919a,
    "astral_spark": 0x080491c1,
    "binding_word": 0x080491e3
}

# 2. Connect to the server
# Make sure to update '53684' to your current instance's port!
p = remote('green-hill.picoctf.net', 53684) 

# 3. Loop through the 3 rounds
for i in range(3):
    # Read the server output until it specifies the procedure name
    p.recvuntil(b"procedure '")

    # Extract the function name (read up to the closing quote and remove it)
    func_name = p.recvuntil(b"'")[:-1].decode()
    log.info(f"Round {i+1}: Server is asking for the address of '{func_name}'")

    # Clean up the rest of the prompt buffer ("==> ")
    p.recvuntil(b"==> ")

    # Retrieve the address from our dictionary and use p32() to pack it into raw bytes (Little-Endian)
    addr = symbols[func_name]
    payload = p32(addr)

    log.success(f"Sending payload: {payload}")

    # Send the payload (using 'send' instead of 'sendline' because the server reads exactly 4 bytes, no newline needed)
    p.send(payload)

# 4. Switch to interactive mode to catch and print the flag
p.interactive()