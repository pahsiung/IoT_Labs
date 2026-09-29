// Lab 3 — Node-RED Function Node: "Alert Logic"
//
// Paste this code into a Function node in Node-RED.
// Input:  msg.payload = { ts, temp_c, hum_pct }
// Output: msg.payload with alert and heatIndex added
//         output 1 → normal readings (gauge / chart)
//         output 2 → alert readings (debug + MQTT-out 'iot/alerts')
//
// In the Function node settings, set "Outputs" to 2.

const TEMP_HIGH = 35.0;  // °C upper threshold
const TEMP_LOW  = 10.0;  // °C lower threshold

const temp = msg.payload.temp_c;
const hum  = msg.payload.hum_pct;

// Classify reading
msg.payload.alert =
    temp > TEMP_HIGH ? "HIGH_TEMP" :
    temp < TEMP_LOW  ? "LOW_TEMP"  : "OK";

// Approximate heat index (Steadman formula simplified)
msg.payload.heatIndex = +(
    temp + 0.33 * (hum / 100 * 6.105 *
    Math.exp(17.27 * temp / (237.7 + temp))) - 4.0
).toFixed(2);

// ISO timestamp for InfluxDB (bonus part)
msg.payload.timestamp = new Date().toISOString();

// Route: output 1 = normal, output 2 = alert
if (msg.payload.alert !== "OK") {
    return [null, msg];   // alert branch
} else {
    return [msg, null];   // normal branch
}
