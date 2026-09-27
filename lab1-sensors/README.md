# Lab 1 — Python IoT Pipeline Simulation

**Topic:** Sensor simulation, data processing, MQTT publish/subscribe, visualisation  
**No hardware required** — everything runs in Python.

## Setup

```bash
pip install -r requirements.txt
```

## Files

| File | Description |
|------|-------------|
| `publisher.py` | Simulates a sensor and publishes JSON readings to MQTT |
| `subscriber.py` | Subscribes and prints alerts when temp > 35 °C |
| `visualize.py` | Generates a standalone plot (no broker needed) |

## Running the Lab

### Part 1 & 4 — Standalone visualisation (no network needed)
```bash
python visualize.py
# → saves sensor_plot.png in this directory
```

### Part 3 — MQTT publish/subscribe
Open **two terminals**:

**Terminal 1 — Publisher:**
```bash
python publisher.py
```

**Terminal 2 — Subscriber:**
```bash
python subscriber.py
```

You will see the subscriber printing each reading with `OK` or `*** ALERT ***` status.

## Notes
- Broker: `broker.hivemq.com:1883` (public, no account needed)
- Anomaly probability: 5 % per reading (spike of +10–20 °C)
- Alert threshold: 35 °C (configurable at the top of each script)

