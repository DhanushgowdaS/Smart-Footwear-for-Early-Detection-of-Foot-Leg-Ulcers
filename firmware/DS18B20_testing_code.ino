/*
=========================================================
DS18B20 Temperature Sensor Test
=========================================================

Description:
Reads real-time temperature from a DS18B20 digital
temperature sensor connected to an ESP32 and displays
the temperature in the Serial Monitor.

Hardware:
- ESP32 Development Board
- DS18B20 Temperature Sensor
- 4.7kΩ Pull-up Resistor

Connections:
-----------------------------------
ESP32        DS18B20
-----------------------------------
3.3V   ----> VCC
GPIO4  ----> DATA
GND    ----> GND

Note:
Connect a 4.7kΩ resistor between DATA and 3.3V.

=========================================================
*/

#include <OneWire.h>
#include <DallasTemperature.h>

// -------------------------------
// DS18B20 Data Pin
// -------------------------------
#define ONE_WIRE_BUS 4

// Create OneWire instance
OneWire oneWire(ONE_WIRE_BUS);

// Pass OneWire reference to DallasTemperature library
DallasTemperature tempSensor(&oneWire);

void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println("==================================");
  Serial.println(" DS18B20 Temperature Sensor Test ");
  Serial.println("==================================");

  // Initialize temperature sensor
  tempSensor.begin();
}

void loop() {

  // Request temperature from sensor
  tempSensor.requestTemperatures();

  // Read temperature in Celsius
  float temperature = tempSensor.getTempCByIndex(0);

  if (temperature == DEVICE_DISCONNECTED_C) {

    Serial.println("Temperature Sensor Not Detected!");

  } else {

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");
  }

  delay(1000);
}
