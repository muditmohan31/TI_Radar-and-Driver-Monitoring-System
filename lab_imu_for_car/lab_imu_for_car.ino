#include "MPU9250.h"
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>


const char * ssid = "TP-Link_866C"; //ROG   ROG-NET
const char * pwd = "connect2nw";
// IP address to send UDP data to.
// it can be ip address of the server or
// a network broadcast address
// here is broadcast address

char qw[255], qx[255], qy[255], qz[255], qroll[255], qpitch[255], qyaw[255], roll[255], pitch[255], yaw[255], accx[255], accy[255], accz[255], gyrx[255], gyry[255], gyrz[255], magx[255], magy[255], magz[255], gravaccx[255], gravaccy[255], gravaccz[255];
unsigned long timer=0;
unsigned long counter = 0;
int hs = 0;
int distance = 0;

const char * udpAddress = "192.168.0.198";    //100, 101, 102,103, 110, 120, 130, 140,150
const int udpPort = 9898;  //A=4848, B=5858, C=6868, D=3838, E=7878, F=9898
MPU9250 mpu;
WiFiUDP udp;



void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(2000);

  WiFi.begin(ssid, pwd);
  Serial.println(WiFi.localIP());
  udp.begin(udpPort);

  if (!mpu.setup(0x68)) {  // change to your own address
    while (1) {
      Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
      delay(5000);
    }
  }


  
  mpu.selectFilter(QuatFilterSel::MAHONY);  //MAHONY, NONE, MADGWICK
  // calibrate anytime you want to
  Serial.println("Accel Gyro calibration will start in 5sec.");
  Serial.println("Please leave the device still on the flat plane.");
  mpu.verbose(true);
  mpu.calibrateAccelGyro();
  //    delay(5000);

  //    mpu.setAccBias(-33.86, -86.74, -17.77);
  //    mpu.setGyroBias(-1.09, 1.84, -0.94);
  //    mpu.setMagBias(291.18, 498.07, -397.01);
  //    mpu.setMagScale(0.95, 1.65, 0.74);

  //    Serial.println("Mag calibration will start in 5sec.");
  //    Serial.println("Please Wave device in a figure eight until done.");
  //    delay(5000);
  //    mpu.calibrateMag();
  print_calibration();
  mpu.verbose(false);

  Serial.print("X, Y, Z: ");
  Serial.print(mpu.getMagBiasX(), 2);
  Serial.print(", ");
  Serial.print(mpu.getMagBiasY(), 2);
  Serial.print(", ");
  Serial.println(mpu.getMagBiasZ(), 2);

  float Mx = mpu.getMagBiasX();
  float My = mpu.getMagBiasY();
  float Mz = mpu.getMagBiasZ();

  //    mpu.setMagBias(291.18-Mx, 498.07-My, -397.01-Mz);

  Serial.print("X1, Y1, Z1: ");
  Serial.print(mpu.getMagBiasX(), 2);
  Serial.print(", ");
  Serial.print(mpu.getMagBiasY(), 2);
  Serial.print(", ");
  Serial.println(mpu.getMagBiasZ(), 2);
}

void loop() {
  //    if (mpu.update()) {
  //        static uint32_t prev_ms = millis();
  //        if (millis() > prev_ms + 25) {
  //            print_roll_pitch_yaw();
  //            prev_ms = millis();
  //        }
  //    }
  mpu.update();
  float q0 = (float)mpu.getQuaternionW();
  float q1 = (float)mpu.getQuaternionX();
  float q2 = (float)mpu.getQuaternionY();
  float q3 = (float)mpu.getQuaternionZ();

  float accX = (float)mpu.getAccX();
  float accY = (float)mpu.getAccY();
  float accZ = (float)mpu.getAccZ();

  float gyrX = (float)mpu.getGyroX();
  float gyrY = (float)mpu.getGyroY();
  float gyrZ = (float)mpu.getGyroZ();

  float magX = (float)mpu.getMagX();
  float magY = (float)mpu.getMagY();
  float magZ = (float)mpu.getMagZ();

  float gravaccX = (float)mpu.getLinearAccX();
  float gravaccY = (float)mpu.getLinearAccY();
  float gravaccZ = (float)mpu.getLinearAccZ();

  float QYaw   = atan2(2.0f * (q1 * q2 + q0 * q3), q0 * q0 + q1 * q1 - q2 * q2 - q3 * q3);
  float QPitch = -asin(2.0f * (q1 * q3 - q0 * q2));
  float QRoll  = atan2(2.0f * (q0 * q1 + q2 * q3), q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3);

  QPitch *= 180.0f / PI;
  QYaw   *= 180.0f / PI;
  QRoll  *= 180.0f / PI;



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
  timer =millis();

//  udp.beginPacket(udpAddress, udpPort);
//  udp.print(accx);      //0
//  udp.print(',');
//  udp.print(accy);      //1
//  udp.print(',');
//  udp.print(accz);      //2
//  udp.print(',');
//  udp.print(gyrx);      //3
//  udp.print(',');
//  udp.print(gyry);      //4
//  udp.print(',');
//  udp.print(gyrz);      //5
//  udp.print(',');
//  udp.print(qw);        //6
//  udp.print(',');
//  udp.print(qx);        //7
//  udp.print(',');
//  udp.print(qy);        //8
//  udp.print(',');
//  udp.print(qz);        //9
//  udp.print(',');
//  udp.print(qyaw);      //10    -9
//  udp.print(',');
//  udp.print(qpitch);    //11    -8
//  udp.print(',');
//  udp.print(qroll);     //12    -7
//  udp.print(',');
//  udp.print(yaw);       //13    -6
//  udp.print(',');
//  udp.print(pitch);     //14    -5
//  udp.print(',');
//  udp.print(roll);      //15    -4
//  udp.print(',');
//  udp.print(gravaccx);  //16    -3
//  udp.print(',');
//  udp.print(gravaccy);  //17    -2
//  udp.print(',');
//  udp.print(gravaccz);  //18    -1
//  udp.endPacket();

  udp.beginPacket(udpAddress, udpPort);
  udp.print(counter);
  udp.print(',');
    udp.print(accx);      //0
    udp.print(',');
    udp.print(accy);      //1
    udp.print(',');
    udp.print(accz);      //2
    udp.print(',');
    udp.print(gravaccx);  //20    -3
    udp.print(',');
    udp.print(gravaccy);  //21    -2
    udp.print(',');
    udp.print(gravaccz);  //22    -1
    udp.endPacket();
  

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
//291.18, 498.07, -397.01


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
