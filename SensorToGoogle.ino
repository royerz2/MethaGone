//Include required libraries
#include "WiFi.h"
#include <HTTPClient.h>
#include "time.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>
#include "esp_wpa2.h"

//TODO adjust pin numbers to ESP32 Dev Module

#define DHTPIN 12
#define DHTTYPE DHT22
#define SENSOR_NAME "Sensor2"

bool WPA2 = false;

DHT dht(DHTPIN, DHTTYPE);

int pinMethane = 26;
int pinHydrogen = 35;

struct package
{
  int methane;
  int hydrogen;
  float humidity;
  float temp; 
  int transmitter;
};

typedef struct package Package;
Package data;

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 19800;
const int   daylightOffset_sec = 0;

// WiFi credentials
#define EAP_IDENTITY "i6235319" //if connecting from another corporation, use identity@organisation.domain in Eduroam 
#define EAP_PASSWORD "PandaPanda10001000@" //your Eduroam password
const char* e_ssid = "eduroam"; // Eduroam SSID
int counter = 0;
const char* test_root_ca= \
"-----BEGIN CERTIFICATE-----\n" \
"MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\n" \
"MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\n" \
"d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\n" \
"QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\n" \
"MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\n" \
"b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n" \
"9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\n" \
"CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\n" \
"nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n" \
"43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\n" \
"T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\n" \
"gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\n" \
"BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\n" \
"TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\n" \
"DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\n" \
"hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n" \
"06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\n" \
"PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\n" \
"YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\n" \
"CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=\n" \
"-----END CERTIFICATE-----\n";

const char* ssid = "Pi-Fi";
const char* password = "Pi=3.14159";



// Google script ID and required credentials
String GOOGLE_SCRIPT_ID = "AKfycbz3kSs-GeuxcF9ReLeuahb8xZynn_NSIQlOPmVH5KcE1WQ1UBmx8Jnvvasku-QsqmmTPw";    // change Gscript ID
int count = 0;

void setup() {
  delay(1000);
  Serial.begin(115200);
  delay(1000);
  
  if (WPA2){
    Serial.println();
    Serial.print("Connecting to WIFI: ");
    Serial.println(e_ssid);
    WiFi.disconnect(true);  //disconnect form wifi to set new wifi connection
    WiFi.mode(WIFI_STA); //init wifi mode
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY)); //provide identity
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY)); //provide username --> identity and username is same
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD)); //provide password
    esp_wpa2_config_t config = WPA2_CONFIG_INIT_DEFAULT(); //set config settings to default
    esp_wifi_sta_wpa2_ent_enable(&config); //set config settings to enable function
    WiFi.begin(e_ssid); //connect to wifi
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
      counter++;
      if(counter>=60){ //after 30 seconds timeout - reset board
        ESP.restart();
      }
    }
    Serial.println("");
  }

  else{  
    // connect to WiFi
    Serial.println();
    Serial.print("Connecting to wifi: ");
    Serial.println(ssid);
    Serial.flush();
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
      counter++;
      if(counter>=60){ //after 30 seconds timeout - reset board
        ESP.restart();
      }
    }
    Serial.println("WiFi Connected");
    Serial.println("IP address set: "); 
    Serial.println(WiFi.localIP()); //print LAN IP
    }
  
  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  
}
void loop() {
   if (WiFi.status() == WL_CONNECTED) {
    static bool flag = false;
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
      Serial.println("Failed to obtain time");
      return;
      
    }

    char timeStringBuff[50]; //50 chars should be enough
    strftime(timeStringBuff, sizeof(timeStringBuff), "%d %m %H:%M:%S", &timeinfo);
    String asString(timeStringBuff);
    asString.replace(" ", "-");
    Serial.print("Time:");
    Serial.println(asString);
    
    readSensor(); //Get sensor readings
    
    String urlFinal = "https://script.google.com/macros/s/"+GOOGLE_SCRIPT_ID+"/exec?"+\
                                                                                      "sensor=" SENSOR_NAME + \
                                                                                      "&time=" + asString + \
                                                                                      "&methane=" + String(data.methane) + \
                                                                                      "&hydrogen=" + String(data.hydrogen) + \
                                                                                      "&temperature=" + String(data.temp) + \                                                                                                                                                                            
                                                                                      "&humidity=" + String(data.humidity);
    Serial.print("POST data to spreadsheet:");
    Serial.println(urlFinal);
    
    HTTPClient http;
    http.begin(urlFinal.c_str());
    http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
    
    int httpCode = http.GET(); 
    
    Serial.print("HTTP Status Code: ");
    Serial.println(httpCode);
    
    //---------------------------------------------------------------------
    
    //getting response from google sheet
    
    String payload;
    if (httpCode > 0) {
        payload = http.getString();
        Serial.println("Payload: "+payload);    
    }
    
    //---------------------------------------------------------------------
    
    http.end();
    
  }
  count++;
  delay(1000);
} 

void readSensor(){
  int methaneValue = analogRead(pinMethane);
  int hydrogenValue = analogRead(pinHydrogen);
  float humidityValue = dht.readHumidity();
  float temperatureValue = dht.readTemperature();  

  Serial.println(data.methane);
  Serial.println(data.hydrogen);
  Serial.println(data.humidity);
  Serial.println(data.temp);
  Serial.println(data.transmitter);

  data.temp = temperatureValue;
  data.humidity = humidityValue;
  data.methane = methaneValue;
  data.hydrogen = hydrogenValue;
  data.transmitter = 1;

}
