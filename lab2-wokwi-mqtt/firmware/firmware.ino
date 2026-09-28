/*
 * Lab 2 — ESP32 + DHT22 → MQTT (Wokwi Simulator)
 *
 * Simulator:  https://wokwi.com  → New Project → ESP32
 * Wiring:     DHT22 DATA → GPIO 15 | VCC → 3.3V | GND → GND
 * Libraries needed in Wokwi (add to wokwi.toml or Libraries Manager):
 *   - DHT sensor library by Adafruit
 *   - PubSubClient by Nick O'Leary
 *
 * Wokwi virtual Wi-Fi:  SSID "Wokwi-GUEST", password ""
 * MQTT broker:          broker.hivemq.com:1883  (public, no account)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// ── Pin / sensor config ─────────────────────────────────────────
#define DHTPIN   15
#define DHTTYPE  DHT22
DHT dht(DHTPIN, DHTTYPE);

// ── Network / MQTT config ───────────────────────────────────────
const char* WIFI_SSID  = "Wokwi-GUEST";
const char* WIFI_PASS  = "";
const char* MQTT_HOST  = "broker.hivemq.com";
const int   MQTT_PORT  = 1883;
const char* PUB_TOPIC  = "wokwi/iot/dht22";
const char* SUB_TOPIC  = "wokwi/iot/led/control";

// ── LED (built-in on most ESP32 boards = GPIO 2) ────────────────
const int LED_PIN = 2;

WiFiClient   wifiClient;
PubSubClient mqtt(wifiClient);

// ── Callback: handle incoming control messages ──────────────────
void onMessage(char* topic, byte* payload, unsigned int length) {
  String msg = "";
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.print("Control msg: "); Serial.println(msg);

  if (msg == "ON")  { digitalWrite(LED_PIN, HIGH); Serial.println("LED ON");  }
  if (msg == "OFF") { digitalWrite(LED_PIN, LOW);  Serial.println("LED OFF"); }
}

// ── Connect / reconnect to MQTT broker ─────────────────────────
void mqttConnect() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect("wokwi-esp32")) {
      Serial.println("connected");
      mqtt.subscribe(SUB_TOPIC);
      Serial.print("Subscribed to: "); Serial.println(SUB_TOPIC);
    } else {
      Serial.print("failed rc="); Serial.print(mqtt.state());
      Serial.println(" — retry in 2 s");
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();

  // Connect Wi-Fi
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWi-Fi connected  IP: " + WiFi.localIP().toString());

  // Setup MQTT
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(onMessage);
  mqttConnect();
}

void loop() {
  if (!mqtt.connected()) mqttConnect();
  mqtt.loop();

  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT read failed — retrying");
    delay(2000);
    return;
  }

  // Build JSON payload
  char buf[80];
  snprintf(buf, sizeof(buf), "{\"temp\":%.1f,\"hum\":%.1f}", temp, hum);

  mqtt.publish(PUB_TOPIC, buf);
  Serial.print("Published: "); Serial.println(buf);

  delay(2000);
}
