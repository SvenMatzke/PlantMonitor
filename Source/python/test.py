from sensor import get_soil_moisture, get_temperature_and_humidity, get_light_measure

#
#
data = dict()
data.update(get_soil_moisture(0))
data.update(get_temperature_and_humidity(2))
data.update(get_light_measure(5, 4))
print(data)
print("hi")
