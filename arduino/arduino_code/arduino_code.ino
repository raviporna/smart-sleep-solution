#include "DHT.h"
#define DHTPIN 2     
#define DHTTYPE DHT11
#define ANALOG_THRESHOLD 256

DHT dht(DHTPIN, DHTTYPE);                             // Sensor

void setup() {
  Serial.begin(9600);                                 // initialize serial communication at 9600 bits per second:
  pinMode(LED_BUILTIN, OUTPUT);                       // Built-in LED
  dht.begin();
}

void loop() {
  // light sensor
  int lightSensorValue = analogRead(A0);              // read the input on analog pin 0:
  float voltage = lightSensorValue * (5.0 / 1023.0);  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  //Serial.println(voltage);                            // print out the value you read:

  if(lightSensorValue >= ANALOG_THRESHOLD)
    digitalWrite(LED_BUILTIN, HIGH); // turn on LED
  else
    digitalWrite(LED_BUILTIN, LOW);  // turn off LED

  // temp sensor
  float humidity    = dht.readHumidity();     // read relative humidity in %
  float tempCelcius = dht.readTemperature();  // read temperature in Celcius in integer

  if (isnan(humidity) || isnan(tempCelcius)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  float hic = dht.computeHeatIndex(tempCelcius, humidity, false);

  // return message format: <light_voltage>,<humidity(%)>,<temperature(*C)>,<feels_like(*C)>
  Serial.print(voltage);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.print(tempCelcius);
  Serial.print(",");
  Serial.println(hic);

  delay(1000);
}
