# CTF Write-up: Gamer Returns (TAMUctf)

## Challenge Information

* **Name:** Gamer Returns
* **Category:** Misc
* **Difficulty:** Medium
* **Author:** flocto

**Write-up Author:** BatoiDeA

---

# 1. Challenge Description

> "The gamer is back and returns with a vengeance."
>
> **Note:** No `-` in the flag. Also the flag is case insensitive.

**Provided File:** `gamer-ret...` (A text file containing a single Minecraft `summon` command)

---

# 2. Initial Analysis

Opening the provided file reveals a **very large Minecraft command** beginning with:

```text
summon bat ~ ~69 ~ ...
```

At first glance, this appears to be a **Minecraft NBT (Named Binary Tag)** payload typically used in command blocks.

Breaking down the command structure shows the following:

1. The command summons an **invisible and invulnerable bat**.
2. Attached to the bat is a stack of **10 `chest_minecart` entities** using the `Passengers` attribute.
3. Each minecart contains several **banner items** stored inside its `Items` array.

This structure can be visualized as:

```
Bat
 └── Minecart 1 (Chest)
 └── Minecart 2 (Chest)
 └── Minecart 3 (Chest)
 └── ...
 └── Minecart 10 (Chest)
```

The banners stored in the chests are the key to solving the challenge.

---

# 3. Banner Pattern Encoding

Inside each chest's item data, we see banners such as:

```
red_banner
white_banner
```

Each banner contains a **pattern list** defining the visual layers of the banner.

Example snippet:

```json
{
  "pattern": "stripe_right",
  "color": "white"
},
{
  "pattern": "half_horizontal",
  "color": "red"
}
```

These patterns correspond to **Minecraft banner designs** used to draw **alphabet letters**.

In Minecraft communities, banners are often used to represent characters visually by combining patterns such as:

* `stripe_right`
* `half_horizontal`
* `cross`
* `border`
* `square_top_left`

When layered correctly, these patterns form **letters of the alphabet**.

Therefore, the minecarts collectively encode **text using banner letters**.

---

# 4. Decoding Strategy

A straightforward solution would involve:

1. Parsing the entire command.
2. Extracting all banner NBT data.
3. Mapping banner patterns to letters.
4. Reconstructing the message.

However, the dataset is extremely large.

Fortunately, there is a **visual anomaly** in the banner base items that reveals a shortcut.

---

# 5. Observing the Banner Base Colors

Looking at the **base banner types** used in each minecart reveals a pattern:

| Minecart | Banner Base      |
| -------- | ---------------- |
| 1        | red_banner       |
| 2        | red_banner       |
| 3        | red_banner       |
| 4        | red_banner       |
| 5        | red_banner       |
| 6        | red_banner       |
| **7**    | **white_banner** |
| 8        | red_banner       |
| 9        | red_banner       |
| 10       | red_banner       |

The **7th minecart is the only one using `white_banner`**, making it stand out.

This strongly suggests that the **actual flag is encoded there**, while the other minecarts are likely decoys.

---

# 6. Extracting the Hidden Message

To decode the banners inside the **7th minecart**, we can either:

### Method 1 — Spawn in Minecraft

1. Launch a Minecraft world with **command blocks enabled**.
2. Paste the summon command into a command block.
3. Execute it.
4. Inspect the banners visually.

### Method 2 — Use a Banner Alphabet Guide

Minecraft banner alphabets are well documented online.
By mapping each banner's pattern layers to the corresponding letter, the encoded message becomes clear.

After decoding the banners inside the **7th minecart**, we obtain:

```
GIGEM{T1M3_4_G4M1NG}
```

---

# 7. Decoy Messages

If we decode the banners in the other minecarts, they reveal **troll messages** left by the challenge author, including:

```
TRY_AGAIN
FAKE_FLAG
DONT_SLOP_THIS_PLEASE
```

These are meant to distract solvers who attempt to decode every minecart sequentially.

The **white-banner minecart** is the only one containing the real flag.

---

# 8. Flag

The challenge description states:

* No hyphens
* Case insensitive

Therefore the extracted flag is:

```
gigem{T1M3_4_G4M1NG}
```

---

# 9. Conclusion

This challenge demonstrates a creative use of **Minecraft NBT data and banner pattern encoding**.

Key takeaways:

* Complex looking data structures may hide simple visual clues.
* Identifying anomalies (like the **white banner minecart**) can significantly reduce analysis time.
* Always look for shortcuts before brute-forcing large datasets.

By focusing on the anomalous minecart, we quickly extracted the encoded banner message and recovered the flag.
