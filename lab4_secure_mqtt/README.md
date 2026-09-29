# Lab 4 — Secure MQTT with TLS + JWT Authentication

**Topic:** TLS encryption, JWT token signing/verification, threat simulation  
**Requires:** Python 3, openssl, and either a free HiveMQ Cloud account OR Docker

## Setup

```bash
pip install -r requirements.txt
bash generate_keys.sh          # creates device_private_key.pem + device_public_key.pem
```

## Part 2 — JWT demo (no broker needed, run this first)

```bash
python jwt_demo.py
```

This shows JWT creation, valid verification, expired-token rejection, and tampered-token rejection — all locally without any network connection.

## Part 1 — TLS-secured MQTT

### Option A: HiveMQ Cloud (recommended — easiest)

1. Sign up at https://www.hivemq.com/mqtt-cloud/ (free, no credit card)
2. Create a serverless cluster and note the hostname
3. Add a credential (username + password)
4. Edit the config block at the top of `secure_publish.py` and `secure_subscribe.py`:
   ```python
   BROKER   = "YOUR_CLUSTER_ID.s1.eu.hivemq.cloud"
   USERNAME = "your_username"
   PASSWORD = "your_password"
   ```

### Option B: Local Mosquitto via Docker

```bash
bash generate_certs.sh        # creates TLS certs for localhost
docker compose up -d          # starts Mosquitto on ports 1883 + 8883
```

Then in both Python scripts set:
```python
BROKER   = "localhost"
USERNAME = "iot_device"
PASSWORD = "iotpassword"
```
And change the `tls_set` line to:
```python
client.tls_set(ca_certs="mosquitto/certs/ca.crt", tls_version=ssl.PROTOCOL_TLS_CLIENT)
```

## Running publisher + subscriber

**Terminal 1:**
```bash
python secure_publish.py
```

**Terminal 2:**
```bash
python secure_subscribe.py
```

## Part 3 — Threat simulation

| Test | How | Expected result |
|------|-----|-----------------|
| Connect without TLS | Change PORT to 1883 (HiveMQ Cloud) | Connection refused |
| Expired JWT | Edit `make_jwt_payload` — set `expires_in_minutes=-1` | Subscriber prints `REJECTED — JWT expired` |
| Tampered token | Modify a character in the token string mid-flight | Subscriber prints `REJECTED — invalid JWT signature` |

## Files

| File | Description |
|------|-------------|
| `generate_keys.sh` | Generates RSA-2048 key pair for JWT |
| `generate_certs.sh` | Generates self-signed TLS certs for local Mosquitto |
| `jwt_demo.py` | Standalone JWT sign/verify demo (no network needed) |
| `secure_publish.py` | TLS publisher — signs each reading as JWT |
| `secure_subscribe.py` | TLS subscriber — verifies JWT before accepting data |
| `docker-compose.yml` | Local Mosquitto broker with TLS |
| `mosquitto/config/mosquitto.conf` | Mosquitto TLS configuration |
