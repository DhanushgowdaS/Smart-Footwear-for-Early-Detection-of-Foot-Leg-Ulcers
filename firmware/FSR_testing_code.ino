const int fsrPins[5] = {32, 33, 34, 35, 36}; 

void setup() {
  Serial.begin(115200);
  
  // Print titles side-by-side ONCE at the start
  Serial.println("FSR1\tFSR2\tFSR3\tFSR4\tFSR5");
  Serial.println("------------------------------------");
}

void loop() {
  // Print each reading side-by-side separated by a tab
  Serial.print(analogRead(fsrPins[0])); Serial.print("\t");
  Serial.print(analogRead(fsrPins[1])); Serial.print("\t");
  Serial.print(analogRead(fsrPins[2])); Serial.print("\t");
  Serial.print(analogRead(fsrPins[3])); Serial.print("\t");
  
  // The last one uses 'println' to start a new row
  Serial.println(analogRead(fsrPins[4]));

  delay(200); 
}
