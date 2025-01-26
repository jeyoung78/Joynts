const int arraySize = 3;
int data1[arraySize] = { 1, 0, 0 };
int data2[arraySize] = { 0, 1, 0 };
int data3[arraySize] = { 0, 0, 1 };

void setup() {
  Serial.begin(9600);  // Start the serial communication at 9600 baud rate
}

void loop() {
  for (int i = 0; i < arraySize; i++) {
    Serial.print(data1[i]);
    
    // If it's not the last element, send a comma as a delimiter
    if (i < arraySize - 1) {
      Serial.print(",");
    }
  }
  
  Serial.println();  // Send a newline character to mark the end of data
  
  delay(500);  // Delay for 2 seconds before sending the data again

  for (int i = 0; i < arraySize; i++) {
    Serial.print(data2[i]);
    
    // If it's not the last element, send a comma as a delimiter
    if (i < arraySize - 1) {
      Serial.print(",");
    }
  }
  
  Serial.println();  // Send a newline character to mark the end of data
  
  delay(500);  // Delay for 2 seconds before sending the data again

  for (int i = 0; i < arraySize; i++) {
    Serial.print(data3[i]);
    
    // If it's not the last element, send a comma as a delimiter
    if (i < arraySize - 1) {
      Serial.print(",");
    }
  }
  
  Serial.println();  // Send a newline character to mark the end of data
  
  delay(500);  // Delay for 2 seconds before sending the data again
}
