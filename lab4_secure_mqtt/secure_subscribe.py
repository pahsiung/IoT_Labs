"""
Lab 4 — TLS-Secured MQTT Subscriber with JWT Verification
Connects to HiveMQ Cloud (TLS port 8883) and verifies the RS256 JWT
in each incoming message before accepting the data.

Prerequisites: same as secure_publish.py — run generate_keys.sh first.
Edit BROKER, USERNAME, PASSWORD to match your HiveMQ Cloud cluster.
"""

import ssl
import jwt
import paho.mqtt.client as mqtt

# ── Configuration — edit these ──────────────────────────────────
BROKER          = "YOUR_CLUSTER_ID.s1.eu.hivemq.cloud"
PORT            = 8883
USERNAME        = "your_username"
PASSWORD        = "your_password"
TOPIC           = "iot/secure/device001/telemetry"
PUBLIC_KEY_FILE = "device_public_key.pem"
# ───────────────────────────────────────────────────────────────


def load_public_key() -> str:
    with open(PUBLIC_KEY_FILE) as f:
        return f.read()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected (TLS) to {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"Subscribed to '{TOPIC}'\n")
    else:
        print(f"Connection failed: reason_code={reason_code}")


def make_on_message(public_key: str):
    def on_message(client, userdata, message):
        raw = message.payload.decode()
        try:
            claims  = jwt.decode(raw, public_key, algorithms=["RS256"])
            device  = claims["device_id"]
            data    = claims["data"]
            print(f"  Verified [{device}]  temp={data['temp_c']} °C  hum={data['hum_pct']} %")
        except jwt.ExpiredSignatureError:
            print("  REJECTED — JWT expired")
        except jwt.InvalidSignatureError:
            print("  REJECTED — invalid JWT signature")
        except jwt.DecodeError as e:
            print(f"  REJECTED — malformed token: {e}")
    return on_message


def main():
    public_key = load_public_key()
    print(f"Loaded public key from '{PUBLIC_KEY_FILE}'")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = make_on_message(public_key)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT, keepalive=60)

    print("Waiting for messages — press Ctrl+C to stop.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber stopped.")
        client.disconnect()


if __name__ == "__main__":
    main()
