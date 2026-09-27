"""
Lab 1 — Part 3: MQTT Subscriber + Anomaly Alert
Subscribe to the sensor topic and print alerts when temperature > 35 °C.

Run publisher.py first in a separate terminal, then run this script.
"""

import json
import paho.mqtt.client as mqtt

# ── Configuration ──────────────────────────────────────────────
BROKER    = "broker.hivemq.com"
PORT      = 1883
TOPIC     = "iot/lab/sensor1"
THRESHOLD = 35.0   # °C — alert above this
# ───────────────────────────────────────────────────────────────


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to {BROKER}")
        client.subscribe(TOPIC)
        print(f"Subscribed to '{TOPIC}'  (threshold={THRESHOLD} °C)\n")
    else:
        print(f"Connection failed: reason_code={reason_code}")


def on_message(client, userdata, message):
    try:
        data   = json.loads(message.payload.decode())
        temp   = data["temp_c"]
        hum    = data["hum_pct"]
        ts     = data["ts"]
        status = "*** ALERT ***" if temp > THRESHOLD else "OK"
        print(f"[{ts}]  Temp={temp:6.2f} °C  Hum={hum:5.1f} %  {status}")
    except Exception as exc:
        print(f"[parse error] {exc}  raw={message.payload}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)

print("Waiting for messages — press Ctrl+C to stop.")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber stopped.")
    client.disconnect()
