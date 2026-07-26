#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ==========================
// WiFi Credentials
// ==========================
const char* ssid = "Dhanu";
const char* password = "Dhanu...";
const char* serverUrl = "https://smart-footwear-api.onrender.com/log";

// ==========================
// Variables
// ==========================
int sampleCount = 0;

float sumFSR1 = 0;
float sumFSR2 = 0;
float sumFSR3 = 0;
float sumFSR4 = 0;
float sumTemp1 = 0;

unsigned long startTime = 0;

// ==========================
// Setup
// ==========================
void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  startTime = millis();
}

// ==========================
// Main Loop
// ==========================
void loop() {

  // Replace these with your actual sensor readings
  sumFSR1 += analogRead(34);
  sumFSR2 += analogRead(36);
  sumFSR3 += analogRead(32);
  sumFSR4 += analogRead(33);

  // Replace with actual temperature sensor
  sumTemp1 += 29.25;

  sampleCount++;

  if (millis() - startTime >= 10000) {

    float avgFSR1 = sumFSR1 / sampleCount;
    float avgFSR2 = sumFSR2 / sampleCount;
    float avgFSR3 = sumFSR3 / sampleCount;
    float avgFSR4 = sumFSR4 / sampleCount;
    float avgTemp1 = sumTemp1 / sampleCount;

    Serial.println();
    Serial.println("==============================");
    Serial.println("Sending Averaged Sensor Data");
    Serial.println("==============================");

    Serial.printf("FSR1 : %.2f\n", avgFSR1);
    Serial.printf("FSR2 : %.2f\n", avgFSR2);
    Serial.printf("FSR3 : %.2f\n", avgFSR3);
    Serial.printf("FSR4 : %.2f\n", avgFSR4);
    Serial.printf("TEMP : %.2f\n", avgTemp1);

    sendData(avgFSR1, avgFSR2, avgFSR3, avgFSR4, avgTemp1);

    // Reset
    sumFSR1 = 0;
    sumFSR2 = 0;
    sumFSR3 = 0;
    sumFSR4 = 0;
    sumTemp1 = 0;

    sampleCount = 0;
    startTime = millis();
  }

  delay(100);
}

// ==========================
// Send Data
// ==========================
void sendData(float f1, float f2, float f3, float f4, float t1) {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi Disconnected");
    return;
  }

  HTTPClient http;

  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<256> doc;

  // REQUIRED by FastAPI
  doc["scenario"] = "Walking";

  doc["fsr1"] = f1;
  doc["fsr2"] = f2;
  doc["fsr3"] = f3;
  doc["fsr4"] = f4;
  doc["temp1"] = t1;

  String jsonData;
  serializeJson(doc, jsonData);

  Serial.println();
  Serial.println("JSON Sent:");
  Serial.println(jsonData);

  int httpResponseCode = http.POST(jsonData);

  Serial.print("HTTP Response Code: ");
  Serial.println(httpResponseCode);

  if (httpResponseCode > 0) {

    String response = http.getString();

    Serial.println("Server Response:");
    Serial.println(response);

  } else {

    Serial.print("POST Failed: ");
    Serial.println(http.errorToString(httpResponseCode));

  }

  http.end();
}
