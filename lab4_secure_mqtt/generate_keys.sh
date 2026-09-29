#!/usr/bin/env bash
# Lab 4 — Generate RSA key pair for JWT signing
# Run this once before running secure_publish.py / secure_subscribe.py
#
# Requires: openssl (installed by default on macOS/Linux)
# On Windows: use Git Bash, WSL, or install OpenSSL

set -e

echo "=== Generating RSA-2048 key pair for JWT ==="

# Private key
openssl genrsa -out device_private_key.pem 2048
echo "  [OK] device_private_key.pem"

# Public key (extracted from private)
openssl rsa -in device_private_key.pem -pubout -out device_public_key.pem
echo "  [OK] device_public_key.pem"

echo ""
echo "Keys generated successfully."
echo "  Private key → device_private_key.pem  (keep secret!)"
echo "  Public key  → device_public_key.pem   (share with subscribers)"
echo ""
echo "Next steps:"
echo "  1. Sign up for a free HiveMQ Cloud cluster at https://www.hivemq.com/mqtt-cloud/"
echo "     (or run Mosquitto locally via Docker — see README)"
echo "  2. Edit BROKER / USERNAME / PASSWORD at the top of secure_publish.py"
echo "  3. Run: python secure_publish.py"
echo "  4. Run: python secure_subscribe.py  (in a second terminal)"
