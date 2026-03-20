# picoCTF Write-up: KSECRETS

## Challenge Information

-   **Challenge:** KSECRETS\
-   **Category:** General Skills\
-   **Difficulty:** Easy\
-   **Author:** DARKRAICG492

------------------------------------------------------------------------

## Description

We have a kubernetes cluster setup and flag is in the secrets. You think
you can get it?\
Please wait for a minute for the application to be configured!

Kubernetes is running at: `green-hill.picoctf.net:51901`\
You can find your configuration file in the challenge.

### Hints

-   How are Kubernetes secrets stored internally? Can you decode them?
-   Where are secrets usually stored in Kubernetes
-   Please ignore TLS

------------------------------------------------------------------------

## Objective

The challenge provides a running Kubernetes cluster and a configuration
file (**kubeconfig**).\
The goal is to connect to the cluster and extract the flag hidden inside
**Kubernetes secrets**.

------------------------------------------------------------------------

## Step-by-Step Solution

### Step 1: Initial Analysis

When attempting to access:

    http://green-hill.picoctf.net:51901

The browser returns:

    Client sent an HTTP request to an HTTPS server.

This indicates that the endpoint is **not a normal web service**, but a
**Kubernetes API Server**.

Therefore we must interact with it using **kubectl** and the provided
**kubeconfig** file.

------------------------------------------------------------------------

### Step 2: Bypassing the TLS Certificate Error

The hint says **"Please ignore TLS."**

Running kubectl normally results in a certificate verification error:

    tls: failed to verify certificate

To bypass this, use:

    --insecure-skip-tls-verify

Example:

``` bash
kubectl --kubeconfig ./kubeconfig --insecure-skip-tls-verify get pods
```

------------------------------------------------------------------------

### Step 3: Searching for Secrets in the Cluster

In Kubernetes, sensitive information is stored in **Secrets**.

List all secrets across namespaces:

``` bash
kubectl --kubeconfig ./kubeconfig --insecure-skip-tls-verify get secrets -A
```

Output:

    NAMESPACE     NAME                      TYPE                                  DATA   AGE
    kube-system   chart-values-traefik      helmcharts.helm.cattle.io/values      1      16m
    kube-system   chart-values-traefik-crd  helmcharts.helm.cattle.io/values      0      16m
    kube-system   k3s-serving               kubernetes.io/tls                     2      16m
    picoctf       ctf-secret                Opaque                                1      16m

The suspicious secret is:

    ctf-secret

Located in namespace:

    picoctf

------------------------------------------------------------------------

### Step 4: Extracting the Secret

Retrieve the secret in YAML format:

``` bash
kubectl --kubeconfig ./kubeconfig --insecure-skip-tls-verify get secret ctf-secret -n picoctf -o yaml
```

Output:

``` yaml
apiVersion: v1
data:
  flag: cGljb0NURntrczNjcjM3NV80MW43X3M0ZjNfNTJmNjAzYzR9Cg==
kind: Secret
```

------------------------------------------------------------------------

### Step 5: Decoding the Secret

Kubernetes secrets are **Base64 encoded**, not encrypted.

Decode the flag:

``` bash
echo "cGljb0NURntrczNjcjM3NV80MW43X3M0ZjNfNTJmNjAzYzR9Cg==" | base64 -d
```

------------------------------------------------------------------------

## 🚩 Flag

    picoCTF{ks3cr375_41n7_s4f3_52f603c4}
