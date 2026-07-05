import re
import base64
import os
import json

# --- ANSI Terminal Color Profiles ---
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def render_banner():
    print(f"{CYAN}{BOLD}" + "="*60)
    print("        LOGSHREDDER v1.5 // ADVANCED CTF FORENSICS         ")
    print("="*60 + f"{RESET}")

def shred_logs(filepath):
    if not os.path.exists(filepath):
        print(f"{RED}❌ Target log matrix file not found at: {filepath}{RESET}")
        return

    # Tracking structures
    failed_ssh_counts = {}
    directory_traversals = []
    encoded_payloads = []
    malicious_ips = set()

    print(f"\n{YELLOW}⚙️  Ingesting and shredding threat data streams...{RESET}\n")

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # 1. Parse IP addresses using regex bounds
            ip_match = re.search(r'IP:\s*([\d\.]+)', line)
            ip = ip_match.group(1) if ip_match else "UNKNOWN_IP"

            # 2. Vector Analysis: SSH Brute Force
            if "SSH - Failed password" in line:
                failed_ssh_counts[ip] = failed_ssh_counts.get(ip, 0) + 1
                if failed_ssh_counts[ip] >= 3:
                    malicious_ips.add(ip)

            # 3. Vector Analysis: Web Directory Traversal
            if any(indicator in line for indicator in ["../", "etc/passwd", "boot.ini"]):
                directory_traversals.append({"ip": ip, "log_string": line})
                malicious_ips.add(ip)

            # 4. Vector Analysis: Base64 Obfuscated Exploits
            b64_match = re.search(r'cmd=([a=A-Z0-9+/=]+)', line, re.IGNORECASE)
            if b64_match:
                encoded_string = b64_match.group(1)
                try:
                    decoded_bytes = base64.b64decode(encoded_string)
                    decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
                    encoded_payloads.append({
                        "ip": ip,
                        "encoded": encoded_string,
                        "decoded": decoded_str
                    })
                    malicious_ips.add(ip)
                except Exception:
                    pass

    # ==========================================
    # --- RENDER TERMINAL FORENSICS REPORT ---
    # ==========================================
    
    # Report 1: SSH Brute Force Anomalies
    print(f"{BOLD}[🚨] SSH AUTHENTICATION ANOMALY MATRIX{RESET}")
    print("-" * 60)
    has_ssh_threat = False
    for ip, count in failed_ssh_counts.items():
        if count >= 3:
            print(f" ▸ {RED}{BOLD}SUSPECT IP:{RESET} {ip:<15} | {RED}{count} consecutive failed login cycles{RESET}")
            has_ssh_threat = True
    if not has_ssh_threat:
        print(f" {GREEN}✔ No malicious auth spikes detected below tracking threshold.{RESET}")
    print("-" * 60 + "\n")

    # Report 2: Local File Inclusion / Traversal Probes
    print(f"{BOLD}[🎯] LOCAL FILE INCLUSION / DIRECTORY TRAVERSAL PROBES{RESET}")
    print("-" * 60)
    if directory_traversals:
        for item in directory_traversals:
            print(f" ▸ {YELLOW}{BOLD}SOURCE IP:{RESET} {item['ip']:<15}")
            print(f"   {RED}Payload Vector:{RESET} {item['log_string']}")
    else:
        print(f" {GREEN}✔ No web directory traversal strings matched profile layers.{RESET}")
    print("-" * 60 + "\n")

    # Report 3: Hidden / Obfuscated Command Exploits
    print(f"{BOLD}[🔓] OBFUSCATED PAYLOAD ENVELOPE CORRELATION{RESET}")
    print("-" * 60)
    if encoded_payloads:
        for item in encoded_payloads:
            print(f" ▸ {YELLOW}{BOLD}SOURCE IP:{RESET} {item['ip']:<15}")
            print(f"   {CYAN}Raw Encoded Base64:{RESET} {item['encoded']}")
            print(f"   {GREEN}Decoded Executable String:{RESET} {item['decoded']}")
    else:
        print(f" {GREEN}✔ Zero base64 payload strings identified in query logs.{RESET}")
    print("-" * 60 + "\n")

    # ==========================================
    # --- AUTOMATED DEFENSE EXTRACTION ---
    # ==========================================
    if malicious_ips:
        # Module 1: Write Linux Firewall Bash Script
        bash_script_path = "blocklist.sh"
        with open(bash_script_path, "w") as bf:
            bf.write("#!/bin/bash\n# LOGSHREDDER Automated Incident Mitigation Script\n")
            bf.write("# Execute with sudo privileges to apply kernel network blocks\n\n")
            for ip in sorted(malicious_ips):
                bf.write(f"echo 'Blocking malicious threat vector actor: {ip}'\n")
                bf.write(f"iptables -A INPUT -s {ip} -j DROP\n")
                bf.write(f"ufw deny from {ip}\n\n")
        
        print(f"{GREEN}🛡️  Mitigation Matrix Compiled:{RESET} Generated network containment rule deck at '{BOLD}{bash_script_path}{RESET}'")
        
        # Module 2: Write Structured Threat Intel JSON
        json_report_path = "threat_intel.json"
        intel_payload = {
            "threat_actors_detected": sorted(list(malicious_ips)),
            "ssh_brute_force_summary": failed_ssh_counts,
            "directory_traversal_incidents": directory_traversals,
            "obfuscated_payloads_extracted": encoded_payloads
        }
        with open(json_report_path, "w") as jf:
            json.dump(intel_payload, jf, indent=4)
            
        print(f"{GREEN}📊 Threat Intelligence Exported:{RESET} High-fidelity JSON telemetry payload dropped at '{BOLD}{json_report_path}{RESET}'\n")
    else:
        print(f"{GREEN}✔ Clean scan. Network architecture threat baseline stable. No defensive files created.{RESET}\n")

if __name__ == "__main__":
    render_banner()
    shred_logs("server_logs.txt")