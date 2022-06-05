#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>


int interval = 30000;

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;


bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;

//UUIDs

#define SERVICE_UUID     "7e012e56-4b9e-406d-ac99-fd59d978e55e"
#define METHANE_UUID     "23525a15-ecb5-43c6-bd51-1310529ef001"
#define HYDROGEN_UUID    "3a19c1db-eccd-4efe-ab6a-9cb5f5a49896"
#define TEMPERATURE_UUID "290cfd1d-f970-408b-831f-e4a224d1b922"
#define HUMIDITY_UUID    "3ddc2244-d4fe-4e45-bd38-b810c9d29509"


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};


void setup() {
  Serial.begin(115200);

  // Create the BLE Device
  BLEDevice::init("ESP32");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create Methane Characteristic
  addCharacteristic(pService, METHANE_UUID);
  // Create Hydrogen Characteristic
  addCharacteristic(pService, HYDROGEN_UUID);
    // Create Temperature Characteristic
  addCharacteristic(pService, TEMPERATURE_UUID);
    // Create Humidity Characteristic
  addCharacteristic(pService, HUMIDITY_UUID);
  
  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting a client connection to notify...");
}

void loop() {
  pCharacteristic
}

int addCharacteristic(BLEService* service, const char* UUID){
  pCharacteristic = service->createCharacteristic(
                      UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_INDICATE
                    );

  // Create a BLE Descriptor
  pCharacteristic->addDescriptor(new BLE2902());

  return 0;
}
