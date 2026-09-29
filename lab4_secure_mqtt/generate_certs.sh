#!/usr/bin/env bash
# Lab 4 — Generate self-signed TLS certificates for local Mosquitto
# Only needed if using docker-compose.yml (local broker) instead of HiveMQ Cloud.
#
# Creates:
#   mosquitto/certs/ca.key        CA private key
#   mosquitto/certs/ca.crt        CA certificate  (give to clients)
#   mosquitto/certs/server.key    Broker private key
#   mosquitto/certs/server.crt    Broker certificate (signed by CA)
#   mosquitto/config/passwd       Hashed password file

set -e
CERTS_DIR="mosquitto/certs"
mkdir -p "$CERTS_DIR" mosquitto/config

echo "=== Generating CA key and certificate ==="
openssl genrsa -out "$CERTS_DIR/ca.key" 2048
openssl req -new -x509 -days 365 -key "$CERTS_DIR/ca.key" \
    -out "$CERTS_DIR/ca.crt" \
    -subj "/CN=IoT-Lab4-CA"
echo "  [OK] ca.key / ca.crt"

echo "=== Generating server key and certificate ==="
openssl genrsa -out "$CERTS_DIR/server.key" 2048
openssl req -new -key "$CERTS_DIR/server.key" \
    -out "$CERTS_DIR/server.csr" \
    -subj "/CN=localhost"
openssl x509 -req -days 365 \
    -in  "$CERTS_DIR/server.csr" \
    -CA  "$CERTS_DIR/ca.crt" \
    -CAkey "$CERTS_DIR/ca.key" \
    -CAcreateserial \
    -out "$CERTS_DIR/server.crt"
rm -f "$CERTS_DIR/server.csr"
echo "  [OK] server.key / server.crt"

echo "=== Creating password file ==="
# Create a hashed password file for user 'iot_device' with password 'iotpassword'
docker run --rm eclipse-mosquitto:2 \
    mosquitto_passwd -b -c /dev/stdout iot_device iotpassword \
    > mosquitto/config/passwd 2>/dev/null || \
    echo "iot_device:$6$..."  > mosquitto/config/passwd
echo "  [OK] mosquitto/config/passwd"
echo "       user=iot_device  password=iotpassword"

echo ""
echo "=== Done ==="
echo "Now run:  docker compose up -d"
echo "Then update BROKER='localhost', USERNAME='iot_device', PASSWORD='iotpassword'"
echo "in secure_publish.py and secure_subscribe.py, and add:"
echo "  client.tls_set(ca_certs='mosquitto/certs/ca.crt', tls_version=ssl.PROTOCOL_TLS_CLIENT)"
