# Docker + WSL 2 Installation Guide (Recommended: Ubuntu 22.04)

This guide walks you through installing Docker Desktop and setting it up with WSL 2 on Windows, using **Ubuntu 22.04** as your WSL distribution. 

---

## Prerequisites

- WSL 2 installed and enabled
- Ubuntu 22.04 installed and set to use WSL 2

---

## Step 1: Install Docker Desktop

1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Run the installer and **enable "Use WSL 2 instead of Hyper-V"** during setup
3. Complete the installation and restart if prompted

---

## Step 2: Configure Docker Desktop for WSL

1. Open **Docker Desktop**
2. Navigate to **Settings → General**:
   - Enable: **Use the WSL 2 based engine**
3. Go to **Settings → Resources → WSL Integration**:
   - Enable integration for: `Ubuntu-22.04` (or equivalent installed distro)
4. Click **Apply & Restart**

---

## Step 3: Verify from Ubuntu (WSL)

Open your Ubuntu-22.04 WSL terminal and run:

```bash
docker version
docker run hello-world
```

You should see output confirming that Docker is working correctly.

---
**Other References:**
- Please refer to the guide from [Docker Desktop for WSL](https://docs.docker.com/desktop/features/wsl/) for more info. 
- Please refer to this guide on [using WSL from VS Code and distro Installation](https://code.visualstudio.com/docs/remote/wsl). 

