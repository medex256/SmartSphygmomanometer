# micro:bit SmartSphygmomanometer
A sphygmomanometer is a medical device that measures a person's blood pressure. In this project, we have created a smart version of the sphygmomanometer using a microbit. This smart device can automatically measure a person's blood pressure and heart rate.

## Outline of a project

 - Measure the blood pressure and heart rate automatically once the data is well-received.

 - Enhance the user’s awareness and experience throughout the measurement.

 - Find the adaptive range of result based on the user’s input to verify whether it is normal or not.

 - Handle the errors and exceptions during the automatic measurement without instant crash or quit.

 - Understand how to prepare and store the data for easier data processing without the data overflow and memory limit exceeds.
## Hardware
To complete this project microbit and Lab kit is required

 - micro:bit(v1 or v2)
   
   ![image](https://github.com/medex256/SmartSphygmomanometer/assets/144814946/7f6fec12-e8c9-48ac-93a6-08dd93e95142)

 
 - Lab kit
   
  ![image](https://github.com/medex256/SmartSphygmomanometer/assets/144814946/569f9e65-7440-4ecd-8fb8-ed79a9bc0be2)

  A pressure pump will be installed on top of the lab kit as shown below 
  
  ![image](https://github.com/medex256/SmartSphygmomanometer/assets/144814946/32368a33-181f-464d-971b-b5675a17ef6e)
  ## Software
  The whole software for automatic measurment is written in python.
  ### Libraries needed
  
  For this project we need several libraries shown below:
 
``` python
from microbit import *
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
import gc
from utime import ticks_ms
from sys import exit
```

You can install ssd1306 library package and browse its functions here https://github.com/fizban99/microbit_ssd1306
  ## Demonstration
  ### User Input mode with the normal range
https://youtu.be/4NGQ6APOWqM

  ### Non-user input and alert


https://youtu.be/2fEp0UV6zo0 


### Special alert to remeasure
https://youtu.be/oayR6AXWeyc 









   






