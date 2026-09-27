"""
Lab 1 — Part 4: Visualise Sensor Data
Generates a synthetic time-series, applies a moving-average filter,
highlights anomaly spikes in red, and saves the plot to a PNG file.

Run this script standalone — no MQTT broker needed.
"""

import random
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")          # headless-safe; removes plt.show() dependency
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ── Reproducibility ─────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

# ── Simulate 60 readings (2-second intervals = 2 minutes of data) ──
N           = 60
ANOMALY_P   = 0.05
THRESHOLD   = 35.0
WINDOW      = 5       # moving-average window
OUTPUT_FILE = "sensor_plot.png"

timestamps = [datetime.datetime.utcnow() + datetime.timedelta(seconds=2 * i) for i in range(N)]
temps      = [22.0 + random.gauss(0, 0.5) for _ in range(N)]
hums       = [60.0 + random.gauss(0, 2)   for _ in range(N)]

# Inject anomalies
anomaly_idx = []
for i in range(N):
    if random.random() < ANOMALY_P:
        temps[i] += random.uniform(10, 20)
        anomaly_idx.append(i)

temps_arr = np.array(temps)
hums_arr  = np.array(hums)

# Moving-average smoothing
smoothed = np.convolve(temps_arr, np.ones(WINDOW) / WINDOW, mode="same")

# ── Rolling 5-minute statistics ──────────────────────────────────
print("=== 5-reading rolling statistics ===")
for i in range(0, N, 5):
    chunk = temps_arr[i : i + 5]
    print(f"  readings {i+1:02d}-{i+5:02d}: "
          f"mean={chunk.mean():.2f} °C  "
          f"max={chunk.max():.2f} °C  "
          f"min={chunk.min():.2f} °C")

# Threshold alerts
alerts = [(i, temps_arr[i]) for i in range(N) if temps_arr[i] > THRESHOLD]
if alerts:
    print(f"\n=== ALERTS (temp > {THRESHOLD} °C) ===")
    for idx, val in alerts:
        print(f"  reading {idx+1:02d}  @ {timestamps[idx].strftime('%H:%M:%S')}  temp={val:.2f} °C")
else:
    print("\nNo alerts this run (anomalies below threshold).")

# ── Plot ─────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
fig.suptitle("IoT Lab 1 — Sensor Simulation", fontsize=14, fontweight="bold")

# Temperature
ax1.plot(timestamps, temps_arr, color="steelblue",   lw=1.2, label="Raw temp")
ax1.plot(timestamps, smoothed,   color="darkorange",  lw=2,   label=f"MA({WINDOW})")
ax1.axhline(THRESHOLD, color="crimson", lw=1, ls="--", label=f"Alert {THRESHOLD} °C")
if anomaly_idx:
    ax1.scatter(
        [timestamps[i] for i in anomaly_idx],
        [temps_arr[i]  for i in anomaly_idx],
        color="red", zorder=5, s=80, label="Anomaly spike",
    )
ax1.set_ylabel("Temperature (°C)")
ax1.legend(loc="upper left")
ax1.grid(True, alpha=0.3)

# Humidity
ax2.plot(timestamps, hums_arr, color="seagreen", lw=1.2, label="Humidity")
ax2.set_ylabel("Humidity (%)")
ax2.set_xlabel("Time (UTC)")
ax2.legend(loc="upper left")
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
fig.autofmt_xdate()

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=120)
print(f"\nPlot saved to '{OUTPUT_FILE}'")
