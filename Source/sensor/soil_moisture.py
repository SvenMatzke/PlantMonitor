import maschine


def get_soil_moisture(pin_id):
    """
    :return: returns the soil_moisture in percentage
    :rtype: tuple(key, int)
    """
    adc = maschine.ADC(pin_id)
    return "soil moisture", adc.read()/1024
