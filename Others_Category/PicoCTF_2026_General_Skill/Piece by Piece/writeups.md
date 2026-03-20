# Piece by Piece

**Category:** General Skills  
**Difficulty:** Very Easy  
**Author:** YAHAYA MEDDY  

---

## Challenge Description
After logging in, you will find multiple file parts in your home directory. These parts need to be combined and extracted to reveal the flag.

```
ssh -p 53917 ctf-player@dolphin-cove.picoctf.net ( Check port -p every time open instance )
```

Password:
```
a15d25e1
```

---

## Hints
*(None provided on the platform, but an `instructions.txt` file is included in the challenge environment)*

---

# Write-up

## 1. Initial Access

Connect to the challenge instance using the provided SSH credentials:

```bash
ssh -p 53917 ctf-player@dolphin-cove.picoctf.net
```

Enter the password when prompted:

```
a15d25e1
```

After logging in, you obtain a shell as the user `ctf-player`.

---

## 2. Reconnaissance

List the files in the current directory:

```bash
ls
```

Example output:

```
instructions.txt  part_aa  part_ab  part_ac  part_ad  part_ae
```

This indicates that the flag file has been split into multiple parts.

---

## 3. Reading the Instructions

Open the provided instructions file:

```bash
cat instructions.txt
```

Output:

```
Hint:

- The flag is split into multiple parts as a zipped file.
- Use Linux commands to combine the parts into one file.
- The zip file is password protected. Use this "supersecret" password to extract the zip file.
- After unzipping, check the extracted text file for the flag.
```

From these instructions we learn:

- The files `part_*` belong to a **split zip archive**
- We must **combine them**
- The archive password is **supersecret**

---

## 4. Combining the File Parts

The files `part_aa`, `part_ab`, etc. contain raw binary data belonging to a single zip archive.

We can combine them using the `cat` command:

```bash
cat part_* > part.zip
```

Explanation:

- `cat part_*` concatenates all parts
- `>` redirects the output into a new file
- The resulting file `part.zip` is the reconstructed archive

---

## 5. Extracting the Archive

Now extract the reconstructed zip file:

```bash
unzip part.zip
```

You will be prompted for a password:

```
Archive:  part.zip
[part.zip] flag.txt password:
```

Enter:

```
supersecret
```

Extraction result:

```
 extracting: flag.txt
```

---

## 6. Capturing the Flag

Read the extracted file:

```bash
cat flag.txt
```

Output:

```
picoCTF{z1p_and_spl1t_f1l3s_4r3_fun_da494d2e}
```

---

## Flag

```
picoCTF{z1p_and_spl1t_f1l3s_4r3_fun_da494d2e}
```

---

## Key Takeaway

This challenge demonstrates a common file handling technique in Linux:

- Files can be **split into multiple parts**
- They can be **reconstructed using `cat`**
- Compressed archives may also be **password protected**

Understanding how to manipulate files with basic Linux commands is an essential skill in CTF environments.