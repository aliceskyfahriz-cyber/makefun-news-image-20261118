#!/bin/sh
# Reproduce output.png from scratch.
# No network access, no API keys. Requires only python3 + Pillow.
set -e
cd "$(dirname "$0")"
python3 generate.py
