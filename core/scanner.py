## Made By Darrell Mucheri

import subprocess, os, re, json, sys, time
from utils import color

def loading(msg, seconds=1.2):
    chars = "|/-\\"
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{msg} {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 40 + "\r", end="")

print(color("\n[1] Enter file path manually", (0,255,0)))
print(color("[2] Pick file from phone (recommended)", (0,200,255)))
print(color("[0] Back / Exit", (255,80,80)))

choice = input(color("Choose option: ", (255,255,0)))

if choice == "0":
    sys.exit(0)

if choice == "2":
    try:
        picker = subprocess.check_output(
            ["termux-file-picker"],
            text=True
        )
        data = json.loads(picker)
        host_file = data["path"]
    except FileNotFoundError:
        print(color("\n[!] termux-api not installed.", (255,0,0)))
        print(color("Run: pkg install termux-api", (255,200,0)))
        sys.exit(1)
    except Exception:
        print(color("File picker cancelled.", (255,120,0)))
        sys.exit(1)
else:
    host_file = input(color(
        "Enter full path (e.g storage/downloads/hosts.txt): ",
        (0,255,255)
    ))

# Normalize storage path
if host_file.startswith("storage/"):
    host_file = "/storage/emulated/0/" + host_file.replace("storage/", "")

if not os.path.exists(host_file):
    print(color(f"File not found: {host_file}", (255,0,0)))
    sys.exit(1)

# Load hosts
with open(host_file) as f:
    raw = f.read().replace(",", "\n")
    hosts = [h.strip() for h in raw.splitlines() if h.strip()]

total = len(hosts)
print(color(f"\nLoaded {total} hosts\n", (0,255,255)))

os.makedirs("output", exist_ok=True)

loading("Initializing scanner")

for i, host in enumerate(hosts, start=1):
    try:
        print(color(f"[{i}/{total}] Scanning: {host}", (100,180,255)))

        http = subprocess.run(
            ["curl", "-I", "-m", "8", f"http://{host}"],
            capture_output=True, text=True
        )

        https = subprocess.run(
            ["curl", "-I", "-m", "8", "-k", f"https://{host}"],
            capture_output=True, text=True
        )

        def get_code(out):
            m = re.search(r"HTTP\/\d(?:\.\d)? (\d+)", out)
            return m.group(1) if m else "N/A"

        http_code = get_code(http.stdout)
        https_code = get_code(https.stdout)

        server_match = re.search(r"Server:\s*(.*)", https.stdout, re.I)
        server = server_match.group(1).strip() if server_match else "unknown"

        cloudflare = "yes" if "cloudflare" in https.stdout.lower() else "no"

        status_line = f"→ HTTP:{http_code} | HTTPS:{https_code} | Server:{server} | CF:{cloudflare}"

        if https_code == "200" or http_code == "200":
            print(color(status_line, (0,255,120)))
            with open("output/status_200.txt", "a") as s:
                s.write(host + "\n")
        else:
            print(color(status_line, (255,180,0)))

        with open("output/all_results.txt", "a") as a:
            a.write(f"{host},{http_code},{https_code},{server},{cloudflare}\n")

        print()

    except KeyboardInterrupt:
        print(color("\nScan cancelled by user.", (255,0,0)))
        sys.exit(0)

print(color("Scan completed successfully ✔", (0,255,255)))##
