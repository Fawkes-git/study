#define iter_max 300

void setup(){
  Serial.begin(9600); // set the data rate in bits per second for serial data transmission
}
 

void loop(){
  int pin0;
  long int sum_pin0 = 0;
  long int ave_pin0 = 0;

  int input_char = 0;
  int iter = 0;

  input_char = Serial.read();

  if (input_char == ' ') {
    while (iter < iter_max) {
      pin0 = analogRead(0);
      sum_pin0 = sum_pin0 + pin0;
      delay(10);
      iter++;
    }

    ave_pin0 = sum_pin0 / iter_max;

    Serial.print(ave_pin0);
    Serial.print('\t');
    Serial.println();
  }
}
