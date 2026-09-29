# Lab 3 — Node-RED Edge Pipeline: Sensor → Alert Logic → Dashboard

**Topic:** Edge processing, visual flow programming, IoT dashboards  
**Requires:** Node.js 18+, Node-RED, and the Lab 1 Python publisher running in parallel

## Quick-start (3 steps)

### 1 — Install Node-RED

**Option A — npm (requires Node.js 18+):**
```bash
npm install -g --unsafe-perm node-red
node-red
```

**Option B — Docker (easiest, no Node.js needed):**
```bash
docker run -it -p 1880:1880 -v node_red_data:/data nodered/node-red
```

Open http://localhost:1880 in your browser.

### 2 — Install the Dashboard palette

Inside Node-RED:
1. Click the ☰ menu → **Manage palette** → **Install** tab
2. Search for `node-red-dashboard` and click **Install**
3. Restart Node-RED if prompted

### 3 — Import the flow

1. Click ☰ menu → **Import**
2. Click **select a file to import** and choose `flow.json` from this directory
3. Click **Import** → then **Deploy** (red button, top right)
4. Open the dashboard: http://localhost:1880/ui

## Run the data source

In a separate terminal:
```bash
pip install -r requirements.txt
python publisher.py
```

Temperature readings will start flowing through the pipeline. Anomaly spikes will appear in the **ALERT** debug tab and be re-published to `iot/alerts`.

## What the flow does

```
MQTT-in (iot/lab/sensor1)
    └─► JSON parse
            ├─► Debug (raw readings)
            └─► Alert Logic (Function node)
                    ├─► [normal] Gauge + Chart → Dashboard at /ui
                    └─► [alert]  Debug + MQTT-out (iot/alerts)
```

## Files

| File | Description |
|------|-------------|
| `publisher.py` | Python script that generates and publishes sensor data |
| `flow.json` | Complete Node-RED flow — import via ☰ → Import |
| `alert_logic.js` | Reference copy of the Function node code |

## Dashboard URL

http://localhost:1880/ui
