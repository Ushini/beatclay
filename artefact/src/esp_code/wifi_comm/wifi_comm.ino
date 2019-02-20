/*
  ESP8266 Blink by Simon Peter
  Blink the blue LED on the ESP-01 module
  This example code is in the public domain

  The blue LED on the ESP-01 module is connected to GPIO1
  (which is also the TXD pin; so we cannot use Serial.print() at the same time)

  Note that this sketch uses LED_BUILTIN to find the pin with the internal LED
*/
#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <WebSocketClient.h>
#include <Hash.h>
#include <ArduinoOTA.h>  

char host[] = "192.168.1.16"; // Google //"192.168.56.1";  // IP serveur - Server IP
char path[] = "8765";
const int   port = 80;            // Port serveur - Server Port
WebSocketClient webSocketClient;
WiFiClient client;

void setup() {
  Serial.begin(57600);
  Serial.print("Connecting to network");
  // byte module_IP[] = {192, 168, 56, 17};
  IPAddress ip(192, 168, 1, 17);
  IPAddress gateway(192, 168, 1, 1); 
  Serial.print(F("Setting static ip to : "));
  Serial.println(ip);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(ip, gateway, subnet);
  //WiFi.config(ip);
//  pinMode(2, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  WiFi.begin("your_ssid", "your_network_password");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");}
  Serial.println("Connected to network");
  Serial.println(WiFi.localIP());
  if(client.connect(host, 80)) {
    Serial.println("Connected");
  }else {
    Serial.println("Connection to server failed.");
  }
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
  }
  Serial.println("Server listening");
}

// the loop function runs over and over again forever
void loop() {
  String data;
 
  if (client.connected()) {
 
    webSocketClient.sendData("Yooooo");
 
    webSocketClient.getData(data);
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
    }
 
  } else {
    Serial.println("Client disconnected.");
  }
 
  delay(3000);
  
}

//void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
//
//  Serial.println("in Websocketevent")
//
//}
