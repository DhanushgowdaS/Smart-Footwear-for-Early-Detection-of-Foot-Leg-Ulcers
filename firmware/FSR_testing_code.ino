/*
=========================================================
ESP32 FSR (Force Sensitive Resistor) Test
=========================================================

Description:
Reads analog values from four Force Sensitive Resistors
(FSRs) connected to an ESP32 and displays the readings
on the Serial Monitor in real time.

Hardware:
- ESP32 Development Board
- 4 × FSR Sensors
- 4 × 10kΩ Resistors

Connections:
------------------------------------------------
ESP32 GPIO      Sensor
------------------------------------------------
GPIO34   -----> FSR1
GPIO36   -----> FSR2
GPIO32   -----> FSR3
GPIO33   -----> FSR4

Each FSR should be connected as a voltage divider
using a 10kΩ resistor to GND.

Author: Dhanush S
Project: Smart Footwear for Ulcer Detection
=========================================================
*/

// ---------------------------
// FSR Pin Definitions
// ---------------------------
const int FSR1 = 34;
const int FSR2 = 36;
const int FSR3 = 32;
const int FSR4 = 33;

void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println("========================================");
  Serial.println(" ESP32 FSR Sensor Test ");
  Serial.println("========================================");

  pinMode(FSR1, INPUT);
  pinMode(FSR2, INPUT);
  pinMode(FSR3, INPUT);
  pinMode(FSR4, INPUT);
}

void loop() {

  int fsr1 = analogRead(FSR1);
  int fsr2 = analogRead(FSR2);
  int fsr3 = analogRead(FSR3);
  int fsr4 = analogRead(FSR4);

  Serial.print("FSR1: ");
  Serial.print(fsr1);

  Serial.print(" | FSR2: ");
  Serial.print(fsr2);

  Serial.print(" | FSR3: ");
  Serial.print(fsr3);

  Serial.print(" | FSR4: ");
  Serial.print(fsr4);

  Serial.println();

  delay(500);
}
