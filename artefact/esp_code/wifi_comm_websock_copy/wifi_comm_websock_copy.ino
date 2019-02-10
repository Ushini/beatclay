

/*
 * WebSocketClient.ino
 *
 *  Created on: 24.05.2015
 *
 */

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <Wire.h>
#include <WiFiUDP.h>
#include <ESP8266WiFiMulti.h>
#include <WebSocketsClient.h>
#include <Hash.h>
//#include <ArduinoOTA.h>

// MPU6050 Slave Device Address
const uint8_t MPU6050SlaveAddress = 0x68;

// Select SDA and SCL pins for I2C communication 
const uint8_t scl = D6;
const uint8_t sda = D7;

// sensitivity scale factor respective to full scale setting provided in datasheet 
const uint16_t AccelScaleFactor = 16384;
const uint16_t GyroScaleFactor = 131;

// MPU6050 few configuration register addresses
const uint8_t MPU6050_REGISTER_SMPLRT_DIV   =  0x19;
const uint8_t MPU6050_REGISTER_USER_CTRL    =  0x6A;
const uint8_t MPU6050_REGISTER_PWR_MGMT_1   =  0x6B;
const uint8_t MPU6050_REGISTER_PWR_MGMT_2   =  0x6C;
const uint8_t MPU6050_REGISTER_CONFIG       =  0x1A;
const uint8_t MPU6050_REGISTER_GYRO_CONFIG  =  0x1B;
const uint8_t MPU6050_REGISTER_ACCEL_CONFIG =  0x1C;
const uint8_t MPU6050_REGISTER_FIFO_EN      =  0x23;
const uint8_t MPU6050_REGISTER_INT_ENABLE   =  0x38;
const uint8_t MPU6050_REGISTER_ACCEL_XOUT_H =  0x3B;
const uint8_t MPU6050_REGISTER_SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ;

ESP8266WiFiMulti WiFiMulti;
WebSocketsClient webSocket;

const unsigned long duration = 5000;
unsigned long last_cycle = 0;
WiFiClient client;

void setup() {
  Serial.begin(57600);

  //Serial.setDebugOutput(true);
  Serial.setDebugOutput(true);

  WiFiMulti.addAP("Ushini's iPhone", "acshauend418)3!-&/schoolschoolschool");

  while(WiFiMulti.run() != WL_CONNECTED) {
    delay(100);
  }

  // server address, port and URL
//  webSocket.begin("172.20.10.3", 8882, "/");
//  webSocket.onEvent(webSocketEvent);
//  webSocket.setReconnectInterval(5000);

  Wire.begin(sda, scl);
  MPU6050_Init();
//  WiFiUDP.begin("172.20.10.3", 8882)

  client.connect("172.20.10.3", 8882);
  
}

void loop() {
//  ArduinoOTA.handle();

 
  double Ax, Ay, Az, T, Gx, Gy, Gz;
  
  Read_RawValue(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_XOUT_H);
  
  //divide each with their sensitivity scale factor
  Ax = (int)AccelX/AccelScaleFactor;
  Ay = (int)AccelY/AccelScaleFactor;
  Az = (int)AccelZ/AccelScaleFactor;
  T = (int)Temperature/340+36.53; //temperature formula
  Gx = (int)GyroX/GyroScaleFactor;
  Gy = (int)GyroY/GyroScaleFactor;
  Gz = (int)GyroZ/GyroScaleFactor;

//  webSocket.loop();
  if(client.connected()){
//    if(completeCycle()){
        String p = String(Ax)+" "+String(Ay)+" "+String(Az)+" "+String(Gx)+" "+String(Gy)+" "+String(Gz)+" ";
        Serial.println(p);
        client.print(p);
        client.flush();
//        webSocket.sendTXT();
//        webSocket.sendTXT(p);
      
//    }
  }
  else {
    Serial.println("connection failure");
  }

  delay(10);
//  client.stop();
}

boolean completeCycle(){
  boolean complete = false;
  unsigned long tiempo = millis();
  
  if(millis() - last_cycle >= duration){
    last_cycle = millis();
    complete = true;
  }
  return complete;  
}


//void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
//  Serial.println("entered websocket event handler");

//  switch(type) {
//    case WStype_DISCONNECTED:
//      Serial.printf("[WSc] Disconnected!\n");
//      break;
//    case WStype_CONNECTED: {
//      Serial.printf("[WSc] Connected to url: %s\n", payload);
//
//      // send message to server when Connected
////      webSocket.sendTXT("flava flav");
//      break;
//    }
//    case WStype_TEXT:
//      Serial.printf("[WSc] get text: %s\n", payload);
//
//      // send message to server
//      //webSocket.sendTXT("I, client, received messsge and send this back to server");
//      break;
//    case WStype_BIN:
//      Serial.printf("[WSc] get binary length: %u\n", length);
//      hexdump(payload, length);
//
//      // send data to server
//      // webSocket.sendBIN(payload, length);
//      break;
//  }

//}

void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SMPLRT_DIV, 0x07);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_1, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_2, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_CONFIG, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_FIFO_EN, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_INT_ENABLE, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_USER_CTRL, 0x00);
}

void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)14);
  AccelX = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelY = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelZ = (((int16_t)Wire.read()<<8) | Wire.read());
  Temperature = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroX = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroY = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroZ = (((int16_t)Wire.read()<<8) | Wire.read());
}

void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}
