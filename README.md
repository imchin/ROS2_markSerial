
# ROS2_markSerial

ROS2 packages uartprotocol


# Installation

Install my packages
```bash
  mkdir -p ~/mark_serial_ws/scr
  cd ~/mark_serial_ws/scr
  git clone https://github.com/imchin/ROS2_markSerial .
  cd ~/mark_serial_ws
  colcon build
  source ~/mark_serial_ws/install/setup.bash
```
    
# Usage/Examples

```
cd ~/mark_serial_ws/src/markserial_pkg/config
code setup_markSerial.yaml

```

yaml is contain : (Idmcu,Port,Setup_Pub,path_arduino)



  ## Setup parameter
  
  - Idmcu : The mcu Id may range from 0 to 16.
    -
      
      In example Idmcu is 1.
      
  

  * Port : Port of mcu  
    -
    

      In example Idmcu is "/dev/ttyUSB0".

  - Setup_Pub : is setup list 
    -
    
    Informat : 
    [  [Idtopic,Name_topic,XXX.msg], [Idtopic2,Name_topic2,XXX2.msg], ........   ]

      Idtopic : The Topic Id may range from 0 to 16.
      -

      Name_topic : Name of the topic  to be published.
      -

      XXX.msg :Name of the file interface to be used on the topic.
      -

      In example is [           [1,"Pose","Pose.msg"]        ]

  - path_arduino : path to arduino shell script from ~
    -
     In example is "arduino"



  ## Run python to generate Library for Arduino.

  ```
cd ~/mark_serial_ws/src/markserial_pkg/scripts
python create_library_arduino.py

```

can now operate the library in arduino ide.

## upload sample code to arduino.

## Run ROS2 markserial node
```
ros2 run markserial_pkg markserial_node

```
## This topic is now published.

