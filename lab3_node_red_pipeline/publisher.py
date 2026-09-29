"""
Lab 3 — MQTT Publisher (feeds the Node-RED pipeline)
Identical to Lab 1 publisher — run this to generate sensor data for Node-RED.

Start this BEFORE opening the Node-RED dashboard.
"""

import json
import time
import random
import datetime
import paho.mqtt.client as mqtt

BROKER       = "broker.hivemq.com"
PORT         = 1883
TOPIC        = "iot/lab/sensor1"
INTERVAL_SEC = 2
ANOMALY_PROB = 0.05

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()


def read_sensor() -> dict:
    temp = 22.0 + random.gauss(0, 0.5)
    if random.random() < ANOMALY_PROB:
        temp += random.uniform(10, 20)
    return {
        "ts":      datetime.datetime.utcnow().isoformat(),
        "temp_c":  round(temp, 2),
        "hum_pct": round(60 + random.gauss(0, 2), 1),
    }


print(f"Publishing to {BROKER}:{PORT}  topic='{TOPIC}'")
print("Keep this running while you work in Node-RED.")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        payload = json.dumps(read_sensor())
        client.publish(TOPIC, payload)
        print(f"  {payload}")
        time.sleep(INTERVAL_SEC)
except KeyboardInterrupt:
    print("\nPublisher stopped.")
finally:
    client.loop_stop()
    client.disconnect()
