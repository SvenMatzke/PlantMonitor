# PlantMonitor
Whats the goal an esp sending soil moisture temperature, humidity and light to an source in your network.
The source for now is fully functioning webserver backend and a webfrontend written in react.

# ESP setup:
For all wireing we need wires so always keep in mind you will need those in addition to your chips and power. 

# Catch 
Easy plant monitoring in a few steps. 




# Setup
An Esp32 is the base as a controller for micropython. 
Simply because we have plenty of IO and plenty of power for little money and we can measure the 
Analog in even without resistors! On Esp8266 we would need a voltage between 0-1 V

## Additional Sensor
 - dht22 (AM2302) 
 - BH1750FVI GY-30
 - Soil Moisture Sensor
 
# for Comport
 - Reset Switch/Button
 

# Hardware (Power supply Part)
For the Power supply part we use simple AA Rechargeable batteries and a step up chip to get our needed 3.3 V
In the future it is planed that the power and sensor part are seperate in design. Because there are multiple solutions for 
powering up an esp and less variants regarding getting the sensor data we want.
  - 2 AA recharable batteries
  - 1 Booster step-up to 3.3 V (4,49 €)
    https://eckstein-shop.de/Pololu-33V-Step-Up-Spannungsregler-U1V10F3
  - battery holder or
  - Romi Battery Contact Set (2 € for 2 sets) 
 
costs without batteries 7€
    
    
# First Installation
Install micropython on your esp8266 (instructions in the micropython link below)
A fully functioning esp firmware can be found under the source folder.
This firmware is needed because if you dont precompile the userv.py and some the sensor module for the light sensor Tsl,
your esp will run out of memory and will not work.

# Second step 
Wire your sensors there is a folder wireing for more details or adjust the sensor.py with your own configuration.
Im the source folder is dist folder which will provide several data from the subfolder python and static_index/dist.
You will need to upload all there files, its the backend, and the webfrontend.

# Third step
Fire up your esp8266. When booting on hardreset you will have 300s to configure your
Plantmonitor via Web. Simply connect to the Wlan 'Plantmonitor' PW: 'Plantmonitor' 
and set the features you need like new ssid and password ;-).

# Running and be happy
From here your Esp will go to Deepsleep for a time set by your config. After this time it will wake up store the current 
sensor data and go offline again for your Deepsleep. To get your data either send them directly to another ip on fireup or
press the reset button to go into configuration-mode again. In this mode you are also able to
read all data saved by your esp yet. 
A webfrontend is reachable if you are connected directly under 192.168.1.4 else the ip used in your network.

# From here on out
We will want to pack power supply and apply your wireing and esp into an casing. 
An 3d printer example will be put in 3d casing

# Infos and Greetings
micropython:
https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html


