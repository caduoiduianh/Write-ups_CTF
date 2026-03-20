# picoCTF Writeup: Printer Shares

## Challenge Information
* **Category:** General Skills  
* **Difficulty:** Easy  
* **Author:** JANICE HE  

---

## Description

Oops! Someone accidentally sent an important file to a network printer—can you retrieve it from the print server?

The printer is on:

```
58707
```

You can test the service with:

```bash
nc -vz mysterious-sea.picoctf.net 58707
```

---

## Hints

1. Knowing how the **SMB protocol** works would be helpful.  
2. `smbclient` and `smbutil` are good tools.

---

# Analysis

The challenge description mentions a **network printer** and a **print server**, while the hints explicitly reference the **SMB (Server Message Block) protocol**.

SMB is commonly used for:

- File sharing
- Printer sharing
- Network resource access

We are given:

- Host: `mysterious-sea.picoctf.net`
- Port: `58707` (non-standard SMB port)

To interact with SMB services from the command line, we can use **`smbclient`**, which behaves similarly to an FTP client.

Since the challenge does not provide credentials, we attempt an **anonymous login** using the `-N` option (no password).

---

# Solution

## Step 1: Enumerate Available Shares

First, list the SMB shares available on the server.

```bash
smbclient -L mysterious-sea.picoctf.net -p 58707 -N
```

Example output:

```
        Sharename       Type      Comment
        ---------       ----      -------
        shares          Disk      Public Share With Guests
        IPC$            IPC       IPC Service (Samba 4.19.5-Ubuntu)

Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to mysterious-sea.picoctf.net failed (Error NT_STATUS_CONNECTION_REFUSED)
Unable to connect with SMB1 -- no workgroup available
```

Important observation:

```
shares  Disk  Public Share With Guests
```

This indicates a **publicly accessible SMB share**.

---

## Step 2: Connect to the Share

Next, connect directly to the `shares` directory.

```bash
smbclient //mysterious-sea.picoctf.net/shares -p 58707 -N
```

You will enter an interactive SMB shell:

```
smb: \>
```

---

## Step 3: List Available Files

Use the `ls` command to view the directory contents.

```bash
smb: \> ls
```

Example output:

```
  .                                   D        0  Sat Mar  7 03:25:39 2026
  ..                                  D        0  Sat Mar  7 03:25:39 2026
  dummy.txt                           N     1142  Thu Feb  5 04:22:17 2026
  flag.txt                            N       37  Sat Mar  7 03:25:39 2026

                65536 blocks of size 1024. 56896 blocks available
```

We can see two files:

- `dummy.txt`
- `flag.txt`

---

## Step 4: Download the Files

Use the `get` command to download the files locally.

```bash
smb: \> get dummy.txt
```

```
getting file \dummy.txt of size 1142 as dummy.txt
```

```bash
smb: \> get flag.txt
```

```
getting file \flag.txt of size 37 as flag.txt
```

Exit the SMB shell:

```bash
smb: \> quit
```

---

## Step 5: Read the Flag

Now read the downloaded file:

```bash
cat flag.txt
```

Output:

```
picoCTF{5mb_pr1nter_5h4re5_8caa47ce}
```

---

# Flag

```
picoCTF{5mb_pr1nter_5h4re5_8caa47ce}
```

---

# Key Takeaway

This challenge introduces basic **SMB enumeration and file retrieval**.

Important techniques:

- Using `smbclient` to interact with SMB services
- Enumerating shares with `-L`
- Connecting anonymously with `-N`
- Downloading files with `get`

Understanding SMB is useful for **network enumeration and penetration testing**, especially when dealing with **file shares or misconfigured network printers**.