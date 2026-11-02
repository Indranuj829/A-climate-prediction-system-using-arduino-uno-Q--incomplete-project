#include <Arduino_RouterBridge.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define MQ2_PIN A0

DHT dht(DHTPIN, DHTTYPE);

void setup() {

  Monitor.begin();

  Bridge.begin();

  dht.begin();

  delay(2000);

  Monitor.println("SENSOR SYSTEM STARTED");
}


void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  int mq2Raw = analogRead(MQ2_PIN);


  if (isnan(temperature) || isnan(humidity)) {

    Monitor.println("DHT11 ERROR");

    delay(6000);

    return;
  }


  // Send sensor values from MCU → Python
  Bridge.notify(
    "sensor_data",
    temperature,
    humidity,
    mq2Raw
  );


  Monitor.print("T=");
  Monitor.print(temperature);

  Monitor.print(" H=");
  Monitor.print(humidity);

  Monitor.print(" MQ2=");
  Monitor.println(mq2Raw);


  delay(6000);
}
