import subprocess, os, re
from utils import color

host_file = input(color("Enter host file path (e.g data/hosts.txt): ", (0,255,255)))

if not os.path.exists(host_file):
    print(color("Host file not found!", (255,0,0)))
    exit()

with open(host_file) as f:
    raw = f.read().replace(",", "\n")
    hosts = [h.strip() for h in raw.splitlines() if h.strip()]

print(color(f"\nScanning {len(hosts)} hosts...\n", (255,255,0)))

for host in hosts:
    try:
        cmd = ["curl", "-I", "-m", "8", "-k", f"https://{host}"]
        res = subprocess.run(cmd, capture_output=True, text=True)

        status = re.search(r"HTTP\/\d\.\d (\d+)", res.stdout)
        server = re.search(r"Server: (.*)", res.stdout)
        cf = "cloudflare" if "cloudflare" in res.stdout.lower() else "no"

        status_code = status.group(1) if status else "N/A"
        server_name = server.group(1) if server else "unknown"

        line = f"{host} | {status_code} | {server_name} | CF:{cf}"

        print(color(line, (0,255,0)) if status_code == "200" else color(line, (255,140,0)))

        with open("output/all_results.txt", "a") as a:
            a.write(line + "\n")

        if status_code == "200":
            with open("output/status_200.txt", "a") as s:
                s.write(host + "\n")

    except:
        print(color(f"{host} | ERROR", (255,0,0)))

print(color("\nScan complete!", (0,255,255)))
