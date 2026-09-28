# Lab 2 — ESP32 + DHT22 on Wokwi + MQTT to HiveMQ

**Topic:** Embedded firmware, browser-based ESP32 simulation, MQTT  
**No physical hardware required** — runs entirely in the Wokwi browser simulator.

## What you need

| Tool | Link | Cost |
|------|------|------|
| Wokwi simulator | https://wokwi.com | Free (no account needed) |
| HiveMQ public broker | broker.hivemq.com:1883 | Free |
| Python 3 + paho-mqtt | `pip install -r requirements.txt` | Free |

## Step 1 — Set up the Wokwi circuit (10 min)

1. Go to https://wokwi.com → **New Project** → **ESP32**
2. In the component library (left panel), search **DHT22** and drag it onto the canvas
3. Wire it:
   - DHT22 **DATA** → ESP32 **GPIO 15**
   - DHT22 **VCC**  → ESP32 **3.3V**
   - DHT22 **GND**  → ESP32 **GND**
4. Copy the contents of `firmware/firmware.ino` into the Wokwi code editor
5. Click **▶ Start Simulation**

The Serial Monitor in Wokwi will show MQTT connection messages and published readings.

## Step 2 — Verify from your laptop (5 min)

```bash
pip install -r requirements.txt
python python_subscriber.py
```

You should see temperature and humidity readings arrive every 2 seconds.

## Step 3 — LED control (5 min)

While the simulation is running, send control commands:

```bash
python python_subscriber.py --led ON
python python_subscriber.py --led OFF
```

The simulated LED (GPIO 2) will respond.

## Alternative: HiveMQ WebSocket Client

If you prefer a GUI, open https://www.hivemq.com/demos/websocket-client/ and subscribe to `wokwi/iot/dht22`.

## Files

| File | Description |
|------|-------------|
| `firmware/firmware.ino` | Arduino/ESP32 firmware for Wokwi |
| `firmware/wokwi.toml` | Library dependencies for Wokwi |
| `python_subscriber.py` | Python script to receive readings + send LED commands |
