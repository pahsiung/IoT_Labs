"""
Lab 2 — Python Subscriber
Verifies that the Wokwi ESP32 simulator is publishing MQTT messages.

Run this on your laptop while the Wokwi simulation is running.
You can also send LED control commands from here.

Usage:
    python python_subscriber.py            # subscribe only
    python python_subscriber.py --led ON   # send LED ON command
    python python_subscriber.py --led OFF  # send LED OFF command
"""

import sys
import json
import argparse
import paho.mqtt.client as mqtt

BROKER    = "broker.hivemq.com"
PORT      = 1883
SUB_TOPIC = "wokwi/iot/dht22"
LED_TOPIC = "wokwi/iot/led/control"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to {BROKER}")
        client.subscribe(SUB_TOPIC)
        print(f"Subscribed to '{SUB_TOPIC}'\n")
    else:
        print(f"Connection failed: reason_code={reason_code}")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode())
        print(f"  temp={data['temp']:.1f} °C   hum={data['hum']:.1f} %")
    except Exception:
        print(f"  raw: {message.payload}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--led", choices=["ON", "OFF"], help="Send LED command")
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)

    if args.led:
        # Wait for connection, publish command, then disconnect
        client.loop_start()
        import time; time.sleep(1)
        client.publish(LED_TOPIC, args.led)
        print(f"Sent LED command: {args.led}")
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
    else:
        print("Waiting for ESP32 messages — press Ctrl+C to stop.")
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nSubscriber stopped.")
            client.disconnect()


if __name__ == "__main__":
    main()
