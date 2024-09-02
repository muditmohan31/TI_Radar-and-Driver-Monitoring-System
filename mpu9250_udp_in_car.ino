#include "MPU9250.h"
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>

// Network credentials
const char *ssid = "commander";
const char *password = "connect2jp";

// Static IP address configuration
IPAddress local_IP(192, 168, 0, 4);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);  // optional

// UDP settings
const char* udpServerIPs[] = {
  "192.168.0.2", "192.168.0.3", "192.168.0.5", 
  "192.168.0.6", "192.168.0.7", "192.168.0.8", 
  "192.168.0.9", "192.168.0.10", "192.168.0.11"
};
const int udpPort = 2828;  // Use the same port for sending and receiving

WiFiUDP udp;
char incomingPacket[255];  // buffer for incoming packets

char qw[255], qx[255], qy[255], qz[255], qroll[255], qpitch[255], qyaw[255], roll[255], pitch[255], yaw[255], accx[255], accy[255], accz[255], gyrx[255], gyry[255], gyrz[255], magx[255], magy[255], magz[255], gravaccx[255], gravaccy[255], gravaccz[255];
unsigned long timer = 0;
unsigned long counter = 0;

MPU9250 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(2000);

  // Initialize LED pins
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(15, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  // Ensure LED is off at start
  digitalWrite(15, LOW);
  digitalWrite(14, LOW);
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);

  // Connect to Wi-Fi
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  udp.begin(udpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), udpPort);

  if (!mpu.setup(0x68)) {  // Change to your own address
    while (1) {
      Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
      delay(5000);
    }
  }

  mpu.selectFilter(QuatFilterSel::MAHONY);  // MAHONY, NONE, MADGWICK
  Serial.println("Accel Gyro calibration will start in 5sec.");
  Serial.println("Please leave the device still on the flat plane.");
  mpu.verbose(true);
  mpu.calibrateAccelGyro();
  print_calibration();
  mpu.verbose(false);

  Serial.print("X, Y, Z: ");
  Serial.print(mpu.getMagBiasX(), 2);
  Serial.print(", ");
  Serial.print(mpu.getMagBiasY(), 2);
  Serial.print(", ");
  Serial.println(mpu.getMagBiasZ(), 2);
}

void loop() {
  static unsigned long previousMillis = 0;
  static bool ledState = false;
  const unsigned long interval = 2000; // 2 seconds

  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }

    Serial.printf("UDP packet contents: %s\n", incomingPacket);
    if (strcmp(incomingPacket, "1") == 0) {
      ledState = true;
      previousMillis = millis();
    }
  }

  unsigned long currentMillis = millis();
  if (ledState && (currentMillis - previousMillis >= interval)) {
    ledState = false;
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off
    digitalWrite(15, LOW);
  }

  if (ledState) {
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on
    digitalWrite(15, HIGH);
  }

  mpu.update();
  float q0 = mpu.getQuaternionW();
  float q1 = mpu.getQuaternionX();
  float q2 = mpu.getQuaternionY();
  float q3 = mpu.getQuaternionZ();

  float accX = mpu.getAccX();
  float accY = mpu.getAccY();
  float accZ = mpu.getAccZ();

  float gyrX = mpu.getGyroX();
  float gyrY = mpu.getGyroY();
  float gyrZ = mpu.getGyroZ();

  float magX = mpu.getMagX();
  float magY = mpu.getMagY();
  float magZ = mpu.getMagZ();

  float gravaccX = mpu.getLinearAccX();
  float gravaccY = mpu.getLinearAccY();
  float gravaccZ = mpu.getLinearAccZ();

  float QYaw = atan2(2.0f * (q1 * q2 + q0 * q3), q0 * q0 + q1 * q1 - q2 * q2 - q3 * q3);
  float QPitch = -asin(2.0f * (q1 * q3 - q0 * q2));
  float QRoll = atan2(2.0f * (q0 * q1 + q2 * q3), q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3);

  QPitch *= 180.0f / PI;
  QYaw *= 180.0f / PI;
  QRoll *= 180.0f / PI;

  dtostrf(mpu.getYaw(), 3, 2, yaw);
  dtostrf(mpu.getPitch(), 3, 2, pitch);
  dtostrf(mpu.getRoll(), 3, 2, roll);
  dtostrf(QYaw, 3, 2, qyaw);
  dtostrf(QPitch, 3, 2, qpitch);
  dtostrf(QRoll, 3, 2, qroll);
  dtostrf(q0, 3, 2, qw);
  dtostrf(q1, 3, 2, qx);
  dtostrf(q2, 3, 2, qy);
  dtostrf(q3, 3, 2, qz);
  dtostrf(accX, 3, 2, accx);
  dtostrf(accY, 3, 2, accy);
  dtostrf(accZ, 3, 2, accz);
  dtostrf(gyrX, 3, 2, gyrx);
  dtostrf(gyrY, 3, 2, gyry);
  dtostrf(gyrZ, 3, 2, gyrz);
  dtostrf(magX, 3, 2, magx);
  dtostrf(magY, 3, 2, magy);
  dtostrf(magZ, 3, 2, magz);
  dtostrf(gravaccX, 3, 2, gravaccx);
  dtostrf(gravaccY, 3, 2, gravaccy);
  dtostrf(gravaccZ, 3, 2, gravaccz);
  counter++;
  timer = millis();

  for (int i = 0; i < sizeof(udpServerIPs) / sizeof(udpServerIPs[0]); i++) {
      udp.beginPacket(udpServerIPs[i], udpPort);
      udp.print(accx);      //0
      udp.print(',');
      udp.print(accy);      //1
      udp.print(',');
      udp.print(accz);      //2
      udp.print(',');
      udp.print(gyrx);      //3
      udp.print(',');
      udp.print(gyry);      //4
      udp.print(',');
      udp.print(gyrz);      //5
      udp.print(',');
      udp.print(qw);        //6
      udp.print(',');
      udp.print(qx);        //7
      udp.print(',');
      udp.print(qy);        //8
      udp.print(',');
      udp.print(qz);        //9
      udp.print(',');
      udp.print(qyaw);      //10    -9
      udp.print(',');
      udp.print(qpitch);    //11    -8
      udp.print(',');
      udp.print(qroll);     //12    -7
      udp.print(',');
      udp.print(yaw);       //13    -6
      udp.print(',');
      udp.print(pitch);     //14    -5
      udp.print(',');
      udp.print(roll);      //15    -4
      udp.print(',');
      udp.print(gravaccx);  //16    -3
      udp.print(',');
      udp.print(gravaccy);  //17    -2
      udp.print(',');
      udp.print(gravaccz);  //18    -1
      udp.print(',');
      udp.print(counter);
      udp.endPacket();
  }
  print_roll_pitch_yaw();
}

void print_roll_pitch_yaw() {
  Serial.print("Y, P, R: ");
  Serial.print(mpu.getYaw(), 2);
  Serial.print(", ");
  Serial.print(mpu.getPitch(), 2);
  Serial.print(", ");
  Serial.println(mpu.getRoll(), 2);

  Serial.print("Yaw, Pitch, Roll: ");
  Serial.print(qyaw);
  Serial.print(", ");
  Serial.print(qpitch);
  Serial.print(", ");
  Serial.println(qroll);
}

void print_calibration() {
  Serial.println("< calibration parameters >");
  Serial.println("accel bias [g]: ");
  Serial.print(mpu.getAccBiasX() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getAccBiasY() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getAccBiasZ() * 1000.f / (float)MPU9250::CALIB_ACCEL_SENSITIVITY);
  Serial.println();
  Serial.println("gyro bias [deg/s]: ");
  Serial.print(mpu.getGyroBiasX() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getGyroBiasY() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.print(", ");
  Serial.print(mpu.getGyroBiasZ() / (float)MPU9250::CALIB_GYRO_SENSITIVITY);
  Serial.println();
  Serial.println("mag bias [mG]: ");
  Serial.print(mpu.getMagBiasX());
  Serial.print(", ");
  Serial.print(mpu.getMagBiasY());
  Serial.print(", ");
  Serial.print(mpu.getMagBiasZ());
  Serial.println();
  Serial.println("mag scale []: ");
  Serial.print(mpu.getMagScaleX());
  Serial.print(", ");
  Serial.print(mpu.getMagScaleY());
  Serial.print(", ");
  Serial.print(mpu.getMagScaleZ());
  Serial.println();
}
