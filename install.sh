#!/bin/bash
echo -e "\e[38;2;0;255;255m[+] Installing dependencies...\e[0m"
pip install -r requirements.txt
mkdir -p output
echo -e "\e[38;2;0;255;0m[✓] Installation complete\e[0m"
