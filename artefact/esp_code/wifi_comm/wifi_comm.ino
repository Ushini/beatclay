/*
  ESP8266 Blink by Simon Peter
  Blink the blue LED on the ESP-01 module
  This example code is in the public domain

  The blue LED on the ESP-01 module is connected to GPIO1
  (which is also the TXD pin; so we cannot use Serial.print() at the same time)

  Note that this sketch uses LED_BUILTIN to find the pin with the internal LED
*/
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);  

const char* host = "64.233.187.99"; // Google //"192.168.56.1";  // IP serveur - Server IP
const int   port = 80;            // Port serveur - Server Port
const int   watchdog = 5000;        // Fréquence du watchdog - Watchdog frequency
unsigned long previousMillis = millis(); 

void setup() {
  Serial.begin(57600);
  Serial.print("Connecting to network");
//  pinMode(2, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  WiFi.begin("DESKTOP-GH9KF48 7814", ",00964Wp");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");}
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.on("/Python", handlePath); //C:\Users\ushin\COMP3710
  server.begin();    
  Serial.println("Server listening");
}

// the loop function runs over and over again forever
void loop() {
  server.handleClient();
//  unsigned long currentMillis = millis();
//
//  if ( currentMillis - previousMillis > watchdog ) {
//    previousMillis = currentMillis;
//    WiFiClient client;
//  
//    if (!client.connect(host, port)) {
//      Serial.println(client.connect(host, port));
//      Serial.println("connection failed");
//      return;
//    }
//    
  }

void handlePath() { //Handler for the path

    server.send(200, "text/plain", "Hello Python");

}
//  digitalWrite(2, LOW);   // Turn the LED on (Note that LOW is the voltage level
  // but actually the LED is on; this is because
  // it is active low on the ESP-01)
//  delay(1000);                      // Wait for a second
//  digitalWrite(2, HIGH);  // Turn the LED off by making the voltage HIGH
//  delay(2000);                      // Wait for two seconds (to demonstrate the active low LED)
//}
