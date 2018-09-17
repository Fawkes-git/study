#define NUM_SENSORS 1// number of sensors used

unsigned int sensorValues[NUM_SENSORS];
int i;

void setup(){
  Serial.begin(9600); // set the data rate in bits per second for serial data transmission
}

void loop() {
  for (i = 0; i < NUM_SENSORS; i++) {
    sensorValues[i] = analogRead(i);
    Serial.print(sensorValues[i]);
    Serial.print('\t');
  }
  Serial.println();
  delay(100);
}
