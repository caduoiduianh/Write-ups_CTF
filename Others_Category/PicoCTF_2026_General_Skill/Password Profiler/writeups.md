# picoCTF Write-up: Password Profiler

## Challenge Information

  Field            Value
  ---------------- -------------------
  Challenge Name   Password Profiler
  Category         General Skills
  Difficulty       Very Easy
  Author           Yahaya Meddy

------------------------------------------------------------------------

# Description

We intercepted a suspicious file from a system, but instead of the
password itself, it only contains its **SHA‑1 hash**.

Using **OSINT techniques**, we are given personal details about the
target. The goal is to generate a **custom password wordlist** and
recover the original password by matching its SHA‑1 hash.

Hint: **CUPP** (Common User Passwords Profiler) can generate targeted
password lists based on personal information.

------------------------------------------------------------------------

# Provided Files

### hash.txt

Contains the SHA‑1 hash of the target password:

    968c2349040273dd57dc4be7e238c5ac200ceac5

------------------------------------------------------------------------

### userinfo.txt

Contains personal information gathered via OSINT:

    First Name: Alice
    Surname: Johnson
    Nickname: AJ
    Birthdate: 15-07-1990

    Partner's Name: Bob
    Child's Name: Charlie

------------------------------------------------------------------------

### check_password.py

A Python script that:

1.  Reads passwords from `passwords.txt`
2.  Hashes each entry using **SHA‑1**
3.  Compares the result with the hash in `hash.txt`
4.  Prints the password if a match is found

Running the script initially results in:

    FileNotFoundError: passwords.txt

This means we must **generate the password list first**.

------------------------------------------------------------------------

# Understanding CUPP

CUPP (Common User Passwords Profiler) generates custom password
dictionaries using personal information.

Repository:

    https://github.com/Mebus/cupp

Many users create passwords using personal details such as:

-   Names
-   Birthdates
-   Nicknames
-   Family member names
-   Pets

CUPP automatically combines these values into thousands of possible
password variations.

------------------------------------------------------------------------

# Solution

## Step 1 --- Generate a Wordlist with CUPP

Run CUPP in interactive mode:

``` bash
python3 cupp.py -i
```

Fill in the victim's information ( You can press enter if you don't have information ):

    First Name: Alice
    Surname: Johnson
    Nickname: AJ
    Birthdate (DDMMYYYY): 15071990

    Partners name: Bob
    Partners nickname: Charlie
    Partners birthdate:

    Child's name:
    Child's nickname:
    Child's birthdate:

    Pet's name:
    Company name:

    Add keywords? 
    Add special chars? 
    Add random numbers? 
    Leet mode? 

CUPP generates a targeted dictionary file:

    alice.txt

------------------------------------------------------------------------

## Step 2 --- Prepare the Wordlist

The provided script expects a file called:

    passwords.txt

Rename the generated wordlist:

``` bash
mv alice.txt passwords.txt
```

------------------------------------------------------------------------

## Step 3 --- Run the Password Check Script

Execute the provided script:

``` bash
python3 check_password.py
```

The script hashes each password candidate and compares it with the
target SHA‑1 hash.

Eventually it finds the correct password.

Example output:

    Password found: picoCTF{Aj_15901990}

------------------------------------------------------------------------

# Flag

    picoCTF{Aj_15901990}

------------------------------------------------------------------------

# Why This Works

People often create passwords using personal information because they
are easy to remember.

Examples include:

-   Names
-   Birth years
-   Partner names
-   Child names
-   Nicknames

CUPP generates many combinations such as:

    Alice1990
    AJ1990
    Bob1507
    Charlie90
    Aj_15901990

One of these combinations matches the SHA‑1 hash.

------------------------------------------------------------------------

# Security Lesson

Using personal information for passwords makes them vulnerable to
**OSINT-based attacks**.

Attackers can easily collect public data and generate targeted password
lists.

Recommended defenses:

-   Use **random strong passwords**
-   Use a **password manager**
-   Enable **multi-factor authentication**
-   Avoid using personal information in passwords

------------------------------------------------------------------------

# Summary

Attack workflow:

1.  Analyze the provided files.
2.  Extract OSINT data from `userinfo.txt`.
3.  Generate a targeted password list using **CUPP**.
4.  Rename the list to `passwords.txt`.
5.  Run the password checking script.
6.  Recover the password and obtain the flag.

------------------------------------------------------------------------

# Key Takeaway

**OSINT-based password attacks are effective when users rely on
predictable personal data for passwords.**
