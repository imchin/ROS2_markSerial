#include <Arduino_LSM6DS3.h>
#include <MarkSerial.h>

MarkSerial ros2Serial;  
float ax, ay, az;  
float gx, gy, gz;  

void setup() {
  // put your setup code here, to run once:
IMU.begin();

Serial.begin(115200);    //create object uart setup baud rate 115200
ros2Serial.begin(&Serial,1);    //initial (&serial,Idmcu)

//Set timer
  TCB0.CTRLB = TCB_CNTMODE_INT_gc; 
  TCB0.CCMP =12500;   //20 Hz.
  TCB0.INTCTRL = TCB_CAPT_bm; 
  TCB0.CTRLA = TCB_CLKSEL_CLKTCA_gc | TCB_ENABLE_bm;
//end of set timer
  
}

void loop() {
  // put your main code here, to run repeatedly:

}

void read_imu_Sendros2(){
  if(IMU.readAcceleration(gx, gy, gz) && IMU.readGyroscope(ax, ay, az)){
    ros2Serial.publish_Imu_arduino(ax*(3.141592/180), ay*(3.141592/180), az*(3.141592/180),gx*(9.80665), gy*(9.80665), gz*(-9.80665));  //publish 
  }

  
}

ISR(TCB0_INT_vect)
{
  read_imu_Sendros2();
  TCB0.INTFLAGS = TCB_CAPT_bm; 
}
