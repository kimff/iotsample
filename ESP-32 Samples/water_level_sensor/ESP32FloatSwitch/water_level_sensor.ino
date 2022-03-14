/*
 * Board: Node32 Lite (ESP32 Dev Module)
 */
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>



#define APIKEY  "<api_key>"
#define DEVICE_DEV_ID "<device_id>"        //change id device
#define DEPLOYMENT_URL "https://yourappname.herokuapp.com/streams" //Heroku Free hobby-dev

const char ssid[] = "Your WIFI Name";             //change SSID wifi
const char password[] = "Your WIFI Password";     //change password wifi


const int FloatSensor = 2;
int FloatSensorState = 0;



void setup()
{
  pinMode(13,OUTPUT);
  pinMode(FloatSensor,INPUT);
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  Serial.print("Connecting to ");
  Serial.print(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

}

void loop()
{
   FloatSensorState = digitalRead(FloatSensor);

   StaticJsonDocument<200> doc;
  
    JsonObject root = doc.to<JsonObject>(); // Json Object refer to { }
    root["device_id"] = DEVICE_DEV_ID;
    JsonObject data = root.createNestedObject("data");
    
    
    
    
    if(FloatSensorState == HIGH){
      data["water Level"] = "High";
      // data["other sensor data"] = "other data";  // Add other sensor data
      String body;
      serializeJson(root, body);
      Serial.println(body);
      HTTPClient http;
      Serial.print(FloatSensorState);
      http.begin(DEPLOYMENT_URL);
      http.addHeader("Content-Type", "application/json");
      http.addHeader("apikey", APIKEY);
    
      int httpCode = http.POST(body);
      delay(10000);
      if (httpCode > 0) {
        Serial.printf("[HTTP] POST... code: %d\n", httpCode);
        if (httpCode == HTTP_CODE_OK) {
          String payload = http.getString();
          Serial.println(payload);
        }
      }
      else {
        Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }
      http.end();
    }
}
