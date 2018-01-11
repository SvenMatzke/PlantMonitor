'''
http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/dht.html
'''
import dht
import machine


def get_temperature_and_humidity(pin_id):
    """
    :return: Returns temperature and humidity at the given pin
    :rtype: tuple[tuple]
    """
    d = dht.DHT22(machine.Pin(pin_id))
    d.measure()
    return ("temperature", d.temperature()), ("humidity", d.humidity())
