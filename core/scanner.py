## ZimTunnel Host Response Checker
## Created by Mr Frank OFC 🇿🇼
## t.me/mrfrankofc

import subprocess, os, re, json, sys, time
from utils.color import color

# ================== UI HELPERS ==================

def clear():
    os.system("clear")

def loading(msg, seconds=1.5):
    chars = "|/-\\"
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        sys.stdout.write(color(f"\r{msg} {chars[i % 4]}", (0,200,255)))
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 50 + "\r", end="")

def banner():
    clear()
    print(color("""
███████╗██╗███╗   ███╗████████╗██╗   ██╗███╗   ██╗███╗   ██╗███████╗██╗     
╚══███╔╝██║████╗ ████║╚══██╔══╝██║   ██║████╗  ██║████╗  ██║██╔════╝██║     
  ███╔╝ ██║██╔████╔██║   ██║   ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║     
 ███╔╝  ██║██║╚██╔╝██║   ██║   ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║     
███████╗██║██║ ╚═╝ ██║   ██║   ╚██████╔╝██║ ╚████║██║ ╚████║███████╗███████╗
╚══════╝╚═╝╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚══════╝
""", (0,180,255)))
    print(color("ZimTunnel Host Response Checker", (0,255,180)))
    print(color("Created by Mr Frank OFC 🇿🇼 | t.me/mrfrankofc\n", (200,200,200)))

# ================== FILE PICKER ==================

def pick_file():
    print(color("\n[1] Enter file path manually", (0,255,0)))
    print(color("[2] Pick file from phone (recommended)", (0,200,255)))
    print(color("[0] Exit\n", (255,80,80)))

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
            path = data.get("path")
            if not path:
                raise Exception
            return path
        except FileNotFoundError:
            print(color("\n[!] termux-api not installed.", (255,0,0)))
            print(color("Run: pkg install termux-api", (255,200,0)))
            sys.exit(1)
        except Exception:
            print(color("File picker cancelled.", (255,120,0)))
            sys.exit(1)
    else:
        path = input(color(
            "Enter full path (e.g storage/downloads/hosts.txt): ",
            (0,255,255)
        ))
        if path.startswith("storage/"):
            path = "/storage/emulated/0/" + path.replace("storage/", "")
        return path

# ================== MAIN SCANNER ==================

def main():
    banner()
    host_file = pick_file()

    if not os.path.exists(host_file):
        print(color(f"\nFile not found: {host_file}", (255,0,0)))
        sys.exit(1)

    with open(host_file) as f:
        raw = f.read().replace(",", "\n")
        hosts = [h.strip() for h in raw.splitlines() if h.strip()]

    total = len(hosts)
    print(color(f"\nLoaded {total} hosts\n", (0,255,255)))

    os.makedirs("output", exist_ok=True)
    results = []
    ok_200 = []

    loading("Initializing scanner")

    for i, host in enumerate(hosts, start=1):
        try:
            print(color(f"[{i}/{total}] Scanning {host}", (100,180,255)))

            http = subprocess.run(
                ["curl", "-I", "-m", "7", f"http://{host}"],
                capture_output=True, text=True
            )
            https = subprocess.run(
                ["curl", "-I", "-m", "7", "-k", f"https://{host}"],
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

            status = f"→ HTTP:{http_code} | HTTPS:{https_code} | Server:{server} | CF:{cloudflare}"

            if http_code == "200" or https_code == "200":
                print(color(status, (0,255,120)))
                ok_200.append(host)
            else:
                print(color(status, (255,180,0)))

            results.append(f"{host},{http_code},{https_code},{server},{cloudflare}")
            print()

        except KeyboardInterrupt:
            print(color("\nScan cancelled by user.", (255,0,0)))
            sys.exit(0)

    # ================== SAVE RESULTS ==================

    print(color("\nScan completed ✔", (0,255,255)))
    save = input(color("Save results? (y/n): ", (255,255,0))).lower()

    if save == "y":
        name = input(color("Enter file name (without extension): ", (0,255,255)))
        csv_path = f"output/{name}.csv"
        ok_path = f"output/{name}_200.txt"

        with open(csv_path, "w") as f:
            f.write("host,http,https,server,cloudflare\n")
            f.write("\n".join(results))

        with open(ok_path, "w") as f:
            f.write("\n".join(ok_200))

        print(color(f"\nSaved:", (0,255,120)))
        print(color(f"- {csv_path}", (200,200,200)))
        print(color(f"- {ok_path}", (200,200,200)))

    print(color("\nDone. Press Enter to exit.", (180,180,180)))
    input()

if __name__ == "__main__":
    main()
