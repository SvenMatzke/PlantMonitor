# PlantMonitor
Whats the goal an esp sending soil moisture temperature, humidity and light to an source in your network.
After we created these plantsensors we will create an little sanic or flask application to log or monitor these. 

# ESP setup for this is:
# The Hardware:
  - adafruit breakout esp8266
  - dht22
  - tsl2561
  - soil moisture sensor mit LM393 chip
  - TODO Soil moisture sensor hat als output 3-3.3 v den müsste ich auf max 1 v runterbrechen 
# First step
Install micropython on your esp8266 (instructions in the micropython link below)

# Second step 
Wire your sensors and clone or download this repository.
In the src folder are python files you need to upload via ... 

#TODO installation description

# TODO
- the case for 3d printer
- the wireing
- powersupply on batteries

# Infos and Greetings
micropython:
https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

uploading files:
https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy#upgrade-ampy

pico web
https://techtutorialsx.com/2017/09/01/esp32-micropython-http-webserver-with-picoweb/