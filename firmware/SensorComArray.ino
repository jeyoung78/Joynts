#include "GY521.h"

GY521 sensor1(0x68);
GY521 sensor2(0x68);
GY521 sensor3(0x68);
GY521 sensor4(0x68);

float gy1 = 0, gz1 = 0;
float gy2 = 0, gz2 = 0;
float gy3 = 0, gz3 = 0;
float gy4 = 0, gz4 = 0;

float thumbDown = 0, thumbSide = 0;
float pointDown = 0, pointSide = 0;
float middleDown = 0;
float centerDown = 0, centerSide = 0;

int trigger = 0;
bool thumbOne = false;
bool thumbTwo = false;
bool pointOne = false;
bool pointTwo = false;
bool middleOne = false;


void SelectSensor(uint8_t channel){
  Wire.beginTransmission(0x70);  // TCA9548A address is 0x70
  Wire.write(1 << channel);          // send byte to select bus
  Wire.endTransmission(); //this step is being buggy
}


void setup()
{
  
  Serial.begin(2000000);
  //Serial.println("SensorComArrayV1Test");
  Wire.begin();

  //  INITIALIZE SENSOR 1
  delay(100);
  SelectSensor(0);
  while (sensor1.wakeup() == false)
  {
    Serial.print(millis());
    Serial.println("\tCould not connect to sensor1");
    delay(1000);
  }
  sensor1.setAccelSensitivity(2);  //  8g
  sensor1.setGyroSensitivity(1);   //  500 degrees/s

  sensor1.setThrottle();
  //Serial.println("start...");

  //  set calibration values from calibration sketch.
  sensor1.gye = 0;
  sensor1.gze = 0;
//____________________________________________________________________________________________
  //  INITIALIZE SENSOR 2
  delay(100);
  SelectSensor(1);
  while (sensor2.wakeup() == false)
  {
    Serial.print(millis());
    Serial.println("\tCould not connect to sensor2");
    delay(1000);
  }
  sensor2.setAccelSensitivity(2);  //  8g
  sensor2.setGyroSensitivity(1);   //  500 degrees/s

  sensor2.setThrottle();
  //Serial.println("start...");

  //  set calibration values from calibration sketch.
  sensor2.gye = 0;
  sensor2.gze = 0;
//____________________________________________________________________________________________
//  INITIALIZE SENSOR 3
  delay(100);
  SelectSensor(2);
  while (sensor3.wakeup() == false)
  {
    Serial.print(millis());
    Serial.println("\tCould not connect to sensor3");
    delay(1000);
  }
  sensor3.setAccelSensitivity(2);  //  8g
  sensor3.setGyroSensitivity(1);   //  500 degrees/s

  sensor3.setThrottle();
  //Serial.println("start...");

  //  set calibration values from calibration sketch.
  sensor3.gye = 0;
  sensor3.gze = 0;
//____________________________________________________________________________________________
  //  INITIALIZE SENSOR 4
  delay(100);
  SelectSensor(3);
  while (sensor4.wakeup() == false)
  {
    Serial.print(millis());
    Serial.println("\tCould not connect to sensor4");
    delay(1000);
  }
  sensor4.setAccelSensitivity(2);  //  8g
  sensor4.setGyroSensitivity(1);   //  500 degrees/s

  sensor4.setThrottle();
  //Serial.println("start...");

  //  set calibration values from calibration sketch.
  sensor4.gye = 0;
  sensor4.gze = 0;

}


void loop()
{
  gy1 = 0, gz1 = 0;
  gy2 = 0, gz2 = 0;
  gy3 = 0, gz3 = 0;
  gy4 = 0, gz4 = 0;
  
  for(int i = 1; i <= 1; i++){
    //  READ SENSOR 1
    SelectSensor(0);
    sensor1.read();
    gy1 -= sensor1.getGyroY();
    gz1 -= sensor1.getGyroZ();

    //  READ SENSOR 2
    SelectSensor(1);
    sensor2.read();
    gy2 -= sensor2.getGyroY();
    gz2 -= sensor2.getGyroZ();

    //  READ SENSOR 3
    SelectSensor(2);
    sensor3.read();
    gy3 -= sensor3.getGyroY();
    gz3 -= sensor3.getGyroZ();

    //  READ SENSOR 4
    SelectSensor(3);
    sensor4.read();
    gy4 -= sensor4.getGyroY();
    gz4 -= sensor4.getGyroZ();
  }

  thumbDown = gy2 * 0.05;
  thumbSide = gz2 * 0.05;

  pointDown = gy1 * 0.05;
  pointSide = gz1 * 0.05;

  middleDown = gy3 * 0.05;

  centerDown = gy4 * 0.05;
  centerSide = gy4 * 0.05;

  thumbDown = thumbDown - centerDown;
  thumbSide = thumbSide - centerSide;
  pointDown = pointDown - centerDown;
  pointSide = pointSide - centerSide;
  middleDown = middleDown - centerDown;

//  thumbOne = thumbDown - centerDown;
//  thumbTwo = thumbSide - centerSide;
//  pointOne = pointDown - centerDown;
//  pointTwo = pointSide - centerSide;
//  middleOne = middleDown - centerDown;
//
//  if(((pointOne and pointTwo and thumbOne and thumbTwo and middleOne) << 1) and ((pointOne and pointTwo and thumbOne and thumbTwo and middleOne) >> -1)){
//    trigger == 0;
//  }
//  else if(pointOne >> (4 and thumbOne and thumbTwo and pointTwo and middleOne) and pointTwo >> 1 and trigger == 0){
//    pointDown = true;
//    trigger = 1;
//    Serial.print("trig1");
//  }
//  else if(pointTwo >> (1 and thumbOne and thumbTwo and pointTwo and middleOne) and pointOne << pointTwo and trigger == 0){
//    pointSide = true;
//    trigger = 1;
//    Serial.print("trig2");
//  }
//  else if(middleOne >> (4 and thumbOne and thumbTwo and pointOne and pointTwo) and trigger == 0){
//    middleDown = true;
//    trigger = 1;
//    Serial.print("trig3");
//  }
//  else if(thumbOne >> (4 and thumbTwo and pointOne and pointTwo and middleOne) and thumbTwo >> 1 and trigger == 0){
//    thumbDown = true;
//    trigger = 1;
//    Serial.print("trig4");
//  }
//  else if(thumbTwo >> (4 and thumbOne and pointOne and pointTwo and middleOne) and trigger == 0){
//    thumbSide = true;
//    trigger = 1;
//    Serial.print("trig5");
//  }
//  else{
//    pointDown = false;
//    pointSide = false;
//    middleDown = false;
//    thumbDown = false;
//    thumbSide = false;
//    //trigger = 0;
//    //Serial.print("notrig");
//    if(pointOne << (-4 and thumbOne and thumbTwo and pointTwo and middleOne) and pointTwo << -1 and trigger == 0)
//      trigger = 0;
//    else if(pointTwo << (-1 and thumbOne and thumbTwo and pointTwo and middleOne) and pointOne >> pointTwo and trigger == 0)
//      trigger = 0;
//    else if(middleOne << (-4 and thumbOne and thumbTwo and pointOne and pointTwo) and trigger == 0)
//      trigger = 0;
//    else if(thumbOne << (-4 and thumbTwo and pointOne and pointTwo and middleOne) and thumbTwo << -1 and trigger == 0)
//      trigger = 0;
//    else if(thumbTwo << (-4 and thumbOne and pointOne and pointTwo and middleOne) and trigger == 0)
//      trigger = 0;
//  }

  
  Serial.print(thumbDown);
  Serial.print(',');
  Serial.print(thumbSide);
  Serial.print(',');
  Serial.print(pointDown);
  Serial.print(',');
  Serial.print(pointSide);
  Serial.print(',');
  Serial.print(middleDown);
  Serial.print(',');
  Serial.print(centerDown);
  Serial.print(',');
  Serial.print(centerSide);
  Serial.println();

  sensor1.gye += gy1 * 0.05;
  sensor1.gze += gz1 * 0.05;
  sensor2.gye += gy2 * 0.05;
  sensor2.gze += gz2 * 0.05;
  sensor3.gye += gy3 * 0.05;
  sensor3.gze += gz3 * 0.05;
  sensor4.gye += gy4 * 0.05;
  sensor4.gze += gz4 * 0.05;

}