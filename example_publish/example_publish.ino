#include <MarkSerial.h>  //include library

MarkSerial ros2Serial;   //create object
float x=1;
float y=2;
float z=3;
void setup() {
  
  Serial.begin(115200);    //create object uart setup SERIAL_8E1
  ros2Serial.begin(&Serial,1);    //initial (&serial,Idmcu)
}

void loop() {
  
  ros2Serial.publish_Pose(x ,y ,z);   //publish topic Pose (x,y,z,...,...) sort by Pose.msg
  x=x+0.001;
  y=y+0.001;
  z=z+0.001;
  delay(1000);
}
