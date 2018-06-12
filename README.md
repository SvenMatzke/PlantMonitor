# PlantMonitor
Whats the goal an esp sending soil moisture temperature, humidity and light to an source in your network.
The source for now is fully functioning webserver backend and a webfrontend written in react.

# ESP setup:
For all wireing we need wires so always keep in mind you will need those in addition to your chips and power. 

# Hardware (Sensor Part):
  - adafruit breakout esp8266  (10 €)
  - dht22 (AM2302) (5 €)
  - Adafruit TSL2561 Digital Luminosity Lux Light Sensor Breakout (7 €)
  - soil moisture sensor mit LM393 chip (4 €)
  - 2 suitable resistor i have 1 *330k and 1*100k Ohm to breakdown the output voltage lower then 1 V for analog in of the esp 
  - usb serial converter to flash software
  - Reset-Push Button (1 €)
 
costs without flasher around 27 € 
 
# 2nd iteration will be an smaller esp
 - AI-Thinker ESP8266 ESP-08 (3.93 €)
    https://eckstein-shop.de/AI-Thinker-ESP8266-ESP-12F-Serial-WIFI-Wireless-Remote-Control-Module
 - dht22 (AM2302) (4.95 €)
   https://eckstein-shop.de/DHT22-Digital-Temperatur-und-Feuchtigkeits-Sensor-Modul-AM2302-mit-Jumperkabel
 - BH1750FVI GY-30 (2.95 €)
    https://eckstein-shop.de/BH1750FVI-GY-30-Licht-Helligkeitssensor-Modul-Digital-Light-intensity-Sensor-fuer-Arduino
 - Soil Moisture Sensor (3.56 €)
    https://eckstein-shop.de/Moisture-Sensor
 - Reset Buttons (1.95 € for 10)
    https://eckstein-shop.de/10-Stk-6x6x6mm-DIP-4-mini-Drucktaster-Eingabetaster-AC-250V-DC-12V-50mA
costs will be lowered to 15,59 €

Conntector
 -  cable
 - ...

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


