# LOGSHREDDER: Tactical Linux Security & CTF Log-Analysis Engine

A automated command-line security utility engineered for Capture The Flag (CTF) incident response, threat hunting, and defensive log analysis. `LOGSHREDDER` parses raw server logs, isolates indicators of compromise (IoCs), decrypts obfuscated commands, and compiles automated mitigation artifacts.

---

## 🛡️ Core Capability Matrix

### 1. Brute-Force Authentication Tracking
- Scans system authorization vectors for high-frequency failures from singular IP nodes.
- Flags suspicious entities surpassing the threshold metrics for brute-force attacks.

### 2. LFI & Directory Traversal Detection
- Implements targeted pattern checking to scan HTTP records for manipulation attempts (e.g., `../`, `/etc/passwd`).
- Isolates attack footprints to trace exactly what file vectors were targeted by malicious nodes.

### 3. Base64 De-obfuscation Pipeline
- Extracts obfuscated values embedded within query loops (`cmd=`).
- Decodes hidden strings inline to instantly map target payloads (e.g., catching malicious backdoors executing commands like `whoami`).

### 4. Automated Forensic & Mitigation Output
- **Structured Threat Intel:** Compiles incident metrics into a machine-readable `threat_intel.json` file.
- **Firewall Rule Engine:** Automatically writes a specialized `blocklist.sh` shell script loaded with `iptables` and `ufw` drop commands to neutralize offending hosts instantly.

---

## 🚀 Deployment Operations

1. Ingest your targets into `server_logs.txt`.
2. Execute the engine file via the terminal:
   ```bash
   python log_shredder.py
---

### Step 2: Push It Live via the Web Browser

Since you are running without the Git CLI installed locally, we will use the clean browser method:

1. **Create the Repository:** Go to GitHub, click **New Repository**, and name it `log-shredder-ctf`. Leave it public, check the box to **"Add a README file"**, and hit **Create**.
2. **Upload Assets:** Click **Add file** -> **Upload files**, and drag in your three complete files:
   - `log_shredder.py`
   - `server_logs.txt`
   - `README.md` *(This overwrites the template README)*
3. **Commit changes:** Scroll down, type `"Initial commit: Deploy tactical log parser engine"`, and hit **Commit changes**.

---