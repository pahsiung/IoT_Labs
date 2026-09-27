"""
Lab 1 — Part 1 & 3: Sensor Simulation + MQTT Publisher
Generates synthetic temperature/humidity data with noise and anomalies,
then publishes as JSON to the public HiveMQ broker.

Run this first, then run subscriber.py in a second terminal.
"""

import json
import time
import random
import datetime
import paho.mqtt.client as mqtt

# ── Configuration ──────────────────────────────────────────────
BROKER = "broker.hivemq.com"
PORT   = 1883
TOPIC  = "iot/lab/sensor1"
INTERVAL_SEC = 2       # publish every 2 seconds
ANOMALY_PROB = 0.05    # 5 % chance of a spike per reading
# ───────────────────────────────────────────────────────────────

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()


def read_sensor() -> dict:
    """Simulate a temperature/humidity sensor with occasional spikes."""
    temp = 22.0 + random.gauss(0, 0.5)          # base 22 °C ± noise
    if random.random() < ANOMALY_PROB:
        temp += random.uniform(10, 20)            # inject spike anomaly
    return {
        "ts":       datetime.datetime.utcnow().isoformat(),
        "temp_c":   round(temp, 2),
        "hum_pct":  round(60 + random.gauss(0, 2), 1),
    }


print(f"Publishing to {BROKER}:{PORT}  topic='{TOPIC}'")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        payload = json.dumps(read_sensor())
        result  = client.publish(TOPIC, payload)
        status  = "OK" if result.rc == 0 else f"ERR rc={result.rc}"
        print(f"[{status}] {payload}")
        time.sleep(INTERVAL_SEC)
except KeyboardInterrupt:
    print("\nPublisher stopped.")
finally:
    client.loop_stop()
    client.disconnect()
