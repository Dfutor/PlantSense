#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define pinAnalogico A0

// Nombre del sensor al que pertenece este codigo: Este sensor debe tener un registro en la base de datos
const int id_sensor = 1;

// Nombre de red 
 const char* SSID = "VIRUS_GRATIS";
//const char* SSID = "A15 de Bryan";

// Contraseña de red 
const char* PASSWORD = "Qu13n_Pr3gunt4?";
// const char* PASSWORD = "12345678910";

// ip del fastapi
const char* SERVER_URL = "http://192.168.80.15:3000/insert/lecturas"; // Dirección de tu FastAPI

// Taño de memoria de esta variable
char serverUrlRAM[128];

// Velocidad de transmición de datos (Serial)
const uint32_t SERIAL_SPEED = 115200;

void setup() {
  Serial.begin(SERIAL_SPEED);

  // Buffers en RAM
  char ssidRAM[32];
  char passwordRAM[64];

  // Copiar desde Flash a RAM
  strncpy(ssidRAM, SSID, sizeof(ssidRAM));
  strncpy(passwordRAM, PASSWORD, sizeof(passwordRAM));
  strncpy(serverUrlRAM, SERVER_URL, sizeof(serverUrlRAM));


  Serial.println();
  Serial.print("Conectando a");
  Serial.println(ssidRAM);

  WiFi.begin(ssidRAM, passwordRAM);
  

  int timeout = 20; // 20 segundos para conectar

  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado!");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED){
    HTTPClient http; // Un solo objeto HTTPClient es suficiente
    WiFiClient client;// Crear un objeto WiFiClient

    // Usar serverUrlRAM (¡en RAM!)
    http.begin(client, serverUrlRAM); // Pasar WiFiClient y la URL al método begin
    Serial.println(http.getString());

    http.addHeader("Content-Type", "application/json");

    // Crear JSON en RAM

    char json[128];
    int valor = analogRead(pinAnalogico);

    snprintf(json, sizeof(json), "{\"id_sensor\":%d,\"valor\":%d}",id_sensor,valor);
    
    int httpCode = http.POST(json);
    Serial.println(httpCode);
    http.end();
    
  }else {
    Serial.println("WiFi no conectado");
  }

  

  delay(10000); // Cada 10 segundos
}
