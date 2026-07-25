#include <WiFi.h>
#include <esp_now.h>

// ---------------- Motor Pins ----------------
#define ENA 25
#define ENB 26

#define IN1 32
#define IN2 23
#define IN3 33
#define IN4 22

// Speed (0 - 255)
int motorSpeed = 255;

// Structure
typedef struct struct_message {
  char command;
} struct_message;

struct_message receiveData;

// ---------------- Motor Functions ----------------

void stopMotor() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  Serial.println("STOP");
}

void backward() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  Serial.println("FORWARD");
}

void forward() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  Serial.println("BACKWARD");
}

void right() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  Serial.println("RIGHT");
}

void left() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  Serial.println("LEFT");
}

// ---------------- ESP-NOW Callback ----------------

void OnDataRecv(const esp_now_recv_info_t *info,
                const uint8_t *incomingData,
                int len) {

  memcpy(&receiveData, incomingData, sizeof(receiveData));

  switch(receiveData.command) {

    case 'F':
      forward();
      break;

    case 'B':
      backward();
      break;

    case 'L':
      left();
      break;

    case 'R':
      right();
      break;

    case 'S':
      stopMotor();
      break;

    default:
      stopMotor();
      break;
  }
}

void setup() {

  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotor();

  // PWM
  ledcAttach(ENA, 1000, 8);
  ledcAttach(ENB, 1000, 8);

  ledcWrite(ENA, motorSpeed);
  ledcWrite(ENB, motorSpeed);

  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {

    Serial.println("ESP-NOW Init Failed");
    return;
  }

  esp_now_register_recv_cb(OnDataRecv);

  Serial.println("==================================");
  Serial.println("Wheelchair Ready");
  Serial.println("==================================");
}

void loop() {

}
