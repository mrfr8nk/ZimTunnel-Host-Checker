

---

# 🇿🇼 ZimTunnel Host Response Checker

A fast, interactive **Termux-based host response scanner** designed for Zimbabwean networks  
(Econet / NetOne / Telecel).

This tool scans large host lists, checks **HTTP & HTTPS responses**, detects **Cloudflare**, and helps identify **working / zero-rated candidate hosts**.

---

## 👤 Author

**Mr Frank OFC 🇿🇼**  
📢 Telegram: https://t.me/mrfrankofc  

---

## ✨ Features

- ✅ Scan **1 to 1000+ hosts**
- 📂 Load hosts from **any file on your phone**
- 🔄 Supports **comma-separated or line-by-line** host files
- 🌐 Detects:
  - HTTP status codes (`200`, `301`, `403`, `404`, etc.)
  - HTTPS status
  - Server header
  - Cloudflare usage
- 📊 Live scan progress per host
- 🎨 Clean RGB-colored CLI output
- 💾 After scan:
  - Option to **save results**
  - Enter **custom filename**
- ❌ Cancel scan safely (`Ctrl + C`)
- 📱 Built specifically for **Termux**

---

## 📂 Project Structure

ZimTunnel-Host-Checker/ ├── install.sh ├── zimtunnel.sh ├── zimtunnel.py ├── utils/ │   └── color.py ├── output/ │   └── (generated results) └── README.md

---

## 📲 Requirements

- Android phone
- **Termux**
- Internet connection (mobile data recommended)

---

## 🔧 Installation (Termux)

### 1️⃣ Update packages
```bash
pkg update && pkg upgrade -y

2️⃣ Install required dependencies

pkg install python git curl termux-api -y

3️⃣ Allow storage access (VERY IMPORTANT)

termux-setup-storage

> Allow permission when prompted.
This enables access to:



storage/downloads/
storage/documents/
storage/shared/


---

4️⃣ Clone the repository

git clone https://github.com/YOUR_USERNAME/ZimTunnel-Host-Checker.git
cd ZimTunnel-Host-Checker


---

🚀 First-Time Setup

Run the installer once:

chmod +x install.sh zimtunnel.sh
./install.sh

This will:

Install Python dependencies

Prepare required folders

Make scripts executable



---

▶️ Running the Tool

Start the tool using:

./zimtunnel.sh


---

🖥️ Main Menu

[1] Start Scan
[0] Exit

Press 1 → Begin scanning

Press 0 → Exit



---

📂 Host File Selection

When scanning starts, choose how to load hosts:

[1] Enter file path manually
[2] Pick file from phone (recommended)
[0] Exit

✅ Option 1: Pick file from phone (Recommended)

Opens Android file picker

Select your .txt file

Fast and error-free


> Requires termux-api (installed during setup)




---

✅ Option 2: Enter file path manually

All formats below are accepted:

hosts.txt
Download/hosts.txt
storage/downloads/hosts.txt
/storage/emulated/0/Download/hosts.txt

Paths are normalized automatically.


---

📄 Host File Format

Supported formats:

✔ Line by line

econet.co.zw
cbz.co.zw
zbcnews.co.zw

✔ Comma separated

econet.co.zw,cbz.co.zw,zbcnews.co.zw

✔ Mixed

econet.co.zw
cbz.co.zw,zbcnews.co.zw


---

🔍 Live Scan Output

Example:

[5/120] Scanning → ecocash.co.zw
→ HTTP:301 | HTTPS:200 | Server:cloudflare | CF:yes

Color meanings

🟢 Green → 200 OK

🟡 Yellow → Redirects / 403 / 404

🔴 Red → Errors / unreachable



---

⌨️ Controls

Ctrl + C → Cancel scan safely



---

💾 Saving Results

After scan completion, you’ll be asked:

Save results? (y/n)

If yes, enter a filename.

📁 Output files

Saved inside output/

Example:

output/
├── myscan.csv
└── myscan_200.txt


---

🔄 Updating an Existing Clone

cd ZimTunnel-Host-Checker
git pull

If conflicts occur:

git stash
git pull
git stash pop

If broken:

cd ..
rm -rf ZimTunnel-Host-Checker
git clone https://github.com/YOUR_USERNAME/ZimTunnel-Host-Checker.git


---

⚠️ Disclaimer

This tool is intended for:

Network testing

Research

Educational use


You are responsible for how you use it.


---

⭐ Support

If this tool helps you:

⭐ Star the repository

📢 Share it

💬 Join Telegram: https://t.me/mrfrankofc



---

Built with ❤️ for the Zimbabwe tech community 🇿🇼

---
