void setup() {
    Serial.begin(9600);

}

void loop() {
    int readPin0 = analogRead(A0);
    int readPin1 = analogRead(A1);
    int readPin2 = analogRead(A2);
    int readPin3 = analogRead(A3);

    Serial.print(readPin0);
    Serial.print(",");
    Serial.print(readPin1);
    Serial.print(",");
    Serial.print(readPin2);
    Serial.print(",");
    Serial.println(readPin3);

}
