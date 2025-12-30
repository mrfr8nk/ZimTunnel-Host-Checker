import subprocess, os, re, json
from utils import color

print(color("\n[1] Enter file path manually", (0,255,0)))
print(color("[2] Pick file from phone (recommended)", (0,200,255)))

choice = input(color("Choose option: ", (255,255,0)))

if choice == "2":
    try:
        picker = subprocess.check_output(
            ["termux-file-picker"],
            text=True
        )
        data = json.loads(picker)
        host_file = data["path"]
    except:
        print(color("File picker failed. Install termux-api.", (255,0,0)))
        exit()
else:
    host_file = input(color(
        "Enter full path (e.g storage/downloads/hosts.txt): ",
        (0,255,255)
    ))

# Normalize path
host_file = host_file.replace("storage/", "/storage/emulated/0/")

if not os.path.exists(host_file):
    print(color(f"File not found: {host_file}", (255,0,0)))
    exit()

# -------- LOAD HOSTS --------
with open(host_file) as f:
    raw = f.read().replace(",", "\n")
    hosts = [h.strip() for h in raw.splitlines() if h.strip()]

print(color(f"\nLoaded {len(hosts)} hosts\n", (0,255,255)))

os.makedirs("output", exist_ok=True)

for host in hosts:
    try:
        res = subprocess.run(
            ["curl", "-I", "-m", "8", "-k", f"https://{host}"],
            capture_output=True,
            text=True
        )

        status = re.search(r"HTTP\/\d\.\d (\d+)", res.stdout)
        server = re.search(r"Server: (.*)", res.stdout)
        cf = "yes" if "cloudflare" in res.stdout.lower() else "no"

        code = status.group(1) if status else "N/A"
        server_name = server.group(1) if server else "unknown"

        line = f"{host} | {code} | {server_name} | CF:{cf}"

        if code == "200":
            print(color(line, (0,255,0)))
            with open("output/status_200.txt", "a") as s:
                s.write(host + "\n")
        else:
            print(color(line, (255,180,0)))

        with open("output/all_results.txt", "a") as a:
            a.write(line + "\n")

    except Exception as e:
        print(color(f"{host} | ERROR", (255,0,0)))

print(color("\nScan completed successfully ✔", (0,255,255)))
