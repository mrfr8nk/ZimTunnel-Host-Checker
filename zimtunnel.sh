#!/bin/bash
clear
cat banner/banner.txt
echo -e "\e[38;2;0;200;255mCreated by Mr Frank OFC 🇿🇼\e[0m"
echo -e "\e[38;2;255;0;255mTelegram: t.me/mrfrankofc\e[0m\n"

echo -e "\e[38;2;0;255;0m[1] Start Scan\e[0m"
echo -e "\e[38;2;255;0;0m[0] Exit\e[0m"
read -p "Select option: " opt

if [ "$opt" == "1" ]; then
    python core/scanner.py
else
    exit
fi
