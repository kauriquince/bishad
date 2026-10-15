#!/usr/bin/env bash
# Build helper: freeze server.py into a standalone binary (optional)
# Requires: pip3 install pyinstaller
cd "$(dirname "$0")"
python3 -m PyInstaller --onefile --name bishad-server server.py
echo "Built dist/bishad-server"
