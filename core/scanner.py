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

def print_header():
    print(color("╔" + "═" * 50 + "╗", (0, 200, 255)))
    print(color("║              HOST SCANNER TOOL              ║", (0, 255, 255)))
    print(color("║          Made By Darrell Mucheri            ║", (100, 255, 200)))
    print(color("╚" + "═" * 50 + "╝", (0, 200, 255)))
    print()

def get_file_from_picker():
    """Use termux-file-picker with better error handling"""
    try:
        picker = subprocess.check_output(
            ["termux-file-picker"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        if not picker.strip():
            print(color("\n[!] No file selected.", (255, 120, 0)))
            return None
        
        data = json.loads(picker)
        return data["path"]
        
    except FileNotFoundError:
        print(color("\n[!] termux-api not installed.", (255, 0, 0)))
        print(color("Install: pkg install termux-api", (255, 200, 0)))
        print(color("Then: termux-setup-storage", (255, 200, 0)))
        return None
    except json.JSONDecodeError:
        print(color("\n[!] Invalid response from file picker.", (255, 0, 0)))
        return None
    except Exception as e:
        print(color(f"\n[!] Error: {str(e)}", (255, 0, 0)))
        return None

def get_file_manually():
    """Get file path with better path handling"""
    while True:
        print(color("\n╔══════════════════════════════════════════════╗", (0, 200, 255)))
        print(color("║          ENTER FILE PATH MANUALLY            ║", (0, 255, 255)))
        print(color("╚══════════════════════════════════════════════╝", (0, 200, 255)))
        
        print(color("\nExample paths:", (200, 200, 255)))
        print(color("• /sdcard/downloads/hosts.txt", (150, 255, 150)))
        print(color("• storage/downloads/hosts.txt", (150, 255, 150)))
        print(color("• /storage/emulated/0/DCIM/file.txt", (150, 255, 150)))
        print(color("• ./hosts.txt (current directory)", (150, 255, 150)))
        print(color("• /data/data/com.termux/files/home/file.txt", (150, 255, 150)))
        
        path = input(color("\n📁 Enter file path: ", (0, 255, 255))).strip()
        
        if not path:
            print(color("[!] Path cannot be empty", (255, 120, 0)))
            continue
        
        # Normalize path
        normalized = normalize_path(path)
        
        if os.path.exists(normalized):
            return normalized
        else:
            print(color(f"[!] File not found: {normalized}", (255, 80, 80)))
            retry = input(color("Try again? (y/n): ", (255, 255, 0))).lower()
            if retry != 'y':
                return None

def normalize_path(path):
    """Normalize various path formats"""
    # Remove quotes if present
    path = path.strip('"').strip("'")
    
    # Handle storage paths
    if path.startswith("storage/"):
        path = "/storage/emulated/0/" + path[8:]
    elif path.startswith("sdcard/"):
        path = "/storage/emulated/0/" + path[7:]
    elif path.startswith("~/") or path == "~":
        path = os.path.expanduser(path)
    
    # Handle relative paths
    if not path.startswith("/"):
        path = os.path.join(os.getcwd(), path)
    
    return os.path.normpath(path)

def load_hosts(file_path):
    """Load hosts from file with better parsing"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace common separators with newlines
        for sep in [',', ';', '|', '\t', ' ']:
            content = content.replace(sep, '\n')
        
        # Parse hosts
        hosts = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove http:// or https:// prefix if present
                if line.startswith('http://'):
                    line = line[7:]
                elif line.startswith('https://'):
                    line = line[8:]
                # Remove trailing slash
                line = line.rstrip('/')
                hosts.append(line)
        
        return list(set(hosts))  # Remove duplicates
        
    except Exception as e:
        print(color(f"[!] Error reading file: {str(e)}", (255, 0, 0)))
        return []

def scan_host(host, index, total):
    """Scan a single host with better timeout handling"""
    try:
        print(color(f"\n[{index}/{total}] 📡 Scanning: {host}", (100, 180, 255)))
        
        # Try HTTPS first (more common)
        https_result = subprocess.run(
            ["curl", "-I", "-m", "10", "-s", "-k", f"https://{host}"],
            capture_output=True, text=True
        )
        
        # Try HTTP if HTTPS fails or times out
        if https_result.returncode != 0 or "HTTP" not in https_result.stdout:
            http_result = subprocess.run(
                ["curl", "-I", "-m", "8", "-s", f"http://{host}"],
                capture_output=True, text=True
            )
        else:
            http_result = subprocess.run(
                ["curl", "-I", "-m", "5", "-s", f"http://{host}"],
                capture_output=True, text=True
            )
        
        # Extract status codes
        def get_code(output):
            match = re.search(r"HTTP\/\d(?:\.\d)?\s+(\d{3})", output)
            return match.group(1) if match else "---"
        
        https_code = get_code(https_result.stdout)
        http_code = get_code(http_result.stdout)
        
        # Extract server info
        server_match = re.search(r"Server:\s*([^\r\n]+)", 
                                https_result.stdout or http_result.stdout, 
                                re.IGNORECASE)
        server = server_match.group(1).strip() if server_match else "Unknown"
        
        # Check for Cloudflare
        cf_check = (https_result.stdout + http_result.stdout).lower()
        cloudflare = "Yes" if "cloudflare" in cf_check or "cf-" in cf_check else "No"
        
        # Prepare status line
        status_line = f"   → HTTP: {http_code:3s} | HTTPS: {https_code:3s} | "
        status_line += f"Server: {server[:20]:20s} | CF: {cloudflare:3s}"
        
        # Color coding based on status
        if https_code == "200" or http_code == "200":
            print(color(status_line, (0, 255, 100)))
            return "200", host, http_code, https_code, server, cloudflare
        elif https_code.startswith("3") or http_code.startswith("3"):
            print(color(status_line, (255, 200, 0)))  # Yellow for redirects
            return "3xx", host, http_code, https_code, server, cloudflare
        elif https_code.startswith("4") or http_code.startswith("4"):
            print(color(status_line, (255, 100, 0)))  # Orange for client errors
            return "4xx", host, http_code, https_code, server, cloudflare
        elif https_code.startswith("5") or http_code.startswith("5"):
            print(color(status_line, (255, 50, 50)))  # Red for server errors
            return "5xx", host, http_code, https_code, server, cloudflare
        else:
            print(color(status_line, (150, 150, 150)))  # Gray for unknown
            return "other", host, http_code, https_code, server, cloudflare
            
    except KeyboardInterrupt:
        raise
    except Exception as e:
        error_line = f"   → HTTP: ERR | HTTPS: ERR | Server: Error | CF: ---"
        print(color(error_line, (255, 0, 0)))
        return "error", host, "ERR", "ERR", "Error", "No"

def main():
    print_header()
    
    while True:
        print(color("╔══════════════════════════════════════════════╗", (0, 200, 255)))
        print(color("║                MAIN MENU                     ║", (0, 255, 255)))
        print(color("╠══════════════════════════════════════════════╣", (0, 200, 255)))
        print(color("║ [1] 📁 Pick file from phone                  ║", (0, 255, 120)))
        print(color("║ [2] ⌨️  Enter file path manually              ║", (100, 255, 200)))
        print(color("║ [0] ❌ Exit                                  ║", (255, 100, 100)))
        print(color("╚══════════════════════════════════════════════╝", (0, 200, 255)))
        
        choice = input(color("\nChoose option: ", (255, 255, 0))).strip()
        
        if choice == "0":
            print(color("\n👋 Goodbye!", (0, 255, 255)))
            sys.exit(0)
        
        if choice == "1":
            host_file = get_file_from_picker()
        elif choice == "2":
            host_file = get_file_manually()
        else:
            print(color("[!] Invalid choice", (255, 0, 0)))
            continue
        
        if not host_file:
            continue
        
        # Load hosts
        print(color(f"\n📂 Loading file: {host_file}", (100, 255, 200)))
        loading("Reading hosts file")
        
        hosts = load_hosts(host_file)
        
        if not hosts:
            print(color("[!] No valid hosts found in file", (255, 0, 0)))
            continue
        
        total = len(hosts)
        print(color(f"\n✅ Loaded {total} unique hosts\n", (0, 255, 255)))
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        # Scan hosts
        results = []
        print(color("╔══════════════════════════════════════════════╗", (0, 200, 255)))
        print(color("║             SCANNING RESULTS                 ║", (0, 255, 255)))
        print(color("╚══════════════════════════════════════════════╝", (0, 200, 255)))
        
        try:
            for i, host in enumerate(hosts, 1):
                result = scan_host(host, i, total)
                results.append(result)
                
                # Save progress periodically
                if i % 10 == 0 or i == total:
                    with open("output/all_results.txt", "w") as f:
                        f.write("Host,HTTP_Code,HTTPS_Code,Server,Cloudflare\n")
                        for r in results:
                            f.write(f"{r[1]},{r[2]},{r[3]},{r[4]},{r[5]}\n")
        
        except KeyboardInterrupt:
            print(color("\n\n⏹️  Scan interrupted by user", (255, 120, 0)))
            save = input(color("Save current results? (y/n): ", (255, 255, 0))).lower()
            if save == 'y':
                print(color("Saving current results...", (0, 255, 255)))
            else:
                if os.path.exists("output/all_results.txt"):
                    os.remove("output/all_results.txt")
                sys.exit(0)
        
        # Save final results
        print(color("\n" + "═" * 55, (0, 200, 255)))
        print(color("💾 SAVING RESULTS...", (0, 255, 255)))
        
        # Save all results
        with open("output/all_results.txt", "w") as f:
            f.write("Host,HTTP_Code,HTTPS_Code,Server,Cloudflare\n")
            for r in results:
                f.write(f"{r[1]},{r[2]},{r[3]},{r[4]},{r[5]}\n")
        
        # Save 200 OK hosts separately
        ok_hosts = [r[1] for r in results if r[0] == "200"]
        if ok_hosts:
            with open("output/status_200.txt", "w") as f:
                for host in ok_hosts:
                    f.write(f"{host}\n")
            print(color(f"✅ Saved {len(ok_hosts)} working hosts to: output/status_200.txt", (0, 255, 120)))
        
        # Save other status codes
        for status in ["3xx", "4xx", "5xx", "other", "error"]:
            status_hosts = [r[1] for r in results if r[0] == status]
            if status_hosts:
                with open(f"output/status_{status}.txt", "w") as f:
                    for host in status_hosts:
                        f.write(f"{host}\n")
        
        print(color(f"📊 All results saved to: output/all_results.txt", (100, 200, 255)))
        print(color("=" * 55, (0, 200, 255)))
        
        # Ask to continue
        again = input(color("\n🔁 Scan another file? (y/n): ", (255, 255, 0))).lower()
        if again != 'y':
            print(color("\n👋 Goodbye!", (0, 255, 255)))
            break
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\n👋 Goodbye!", (0, 255, 255)))
        sys.exit(0)
