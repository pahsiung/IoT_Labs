"""
Lab 4 — TLS-Secured MQTT Publisher with JWT Payload Signing
Connects to HiveMQ Cloud (TLS port 8883) and signs each payload with RS256 JWT.

Prerequisites:
    1. bash generate_keys.sh                      # create RSA key pair
    2. Sign up at https://www.hivemq.com/mqtt-cloud/ (free, no credit card)
    3. Create a cluster → copy the hostname, create a user/password
    4. Fill in BROKER, USERNAME, PASSWORD below
    pip install -r requirements.txt
"""

import ssl
import time
import datetime
import jwt
import paho.mqtt.client as mqtt

# ── Configuration — edit these ──────────────────────────────────
BROKER   = "YOUR_CLUSTER_ID.s1.eu.hivemq.cloud"   # from HiveMQ Cloud dashboard
PORT     = 8883                                     # TLS port
USERNAME = "your_username"
PASSWORD = "your_password"
TOPIC    = "iot/secure/device001/telemetry"
DEVICE_ID = "esp32-001"
PRIVATE_KEY_FILE = "device_private_key.pem"
PUBLISH_INTERVAL = 5   # seconds
# ───────────────────────────────────────────────────────────────


def load_private_key() -> str:
    with open(PRIVATE_KEY_FILE) as f:
        return f.read()


def make_jwt_payload(private_key: str, data: dict) -> str:
    """Sign data dict as a JWT with 5-minute expiry."""
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    claims = {
        "device_id": DEVICE_ID,
        "scope":     "telemetry:write",
        "data":      data,
        "iat":       now,
        "exp":       now + datetime.timedelta(minutes=5),
    }
    return jwt.encode(claims, private_key, algorithm="RS256")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected (TLS) to {BROKER}:{PORT}")
    else:
        print(f"Connection failed: reason_code={reason_code}")


def main():
    private_key = load_private_key()
    print(f"Loaded private key from '{PRIVATE_KEY_FILE}'")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    import time as t; t.sleep(1)   # wait for on_connect

    print(f"Publishing to '{TOPIC}' every {PUBLISH_INTERVAL}s — Ctrl+C to stop\n")
    try:
        while True:
            sensor_data = {
                "temp_c":  round(22.5 + __import__("random").gauss(0, 0.3), 2),
                "hum_pct": round(65   + __import__("random").gauss(0, 1.0), 1),
            }
            token = make_jwt_payload(private_key, sensor_data)
            result = client.publish(TOPIC, token)
            status = "OK" if result.rc == 0 else f"ERR rc={result.rc}"
            print(f"[{status}] JWT published  data={sensor_data}")
            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        print("\nPublisher stopped.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
