import network

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


def connect_to_existing_network(essid, password):
    print('connecting to network...')
    sta_if.active(True)
    if essid is None or password is None:
        print('essid or password is not set')
        return sta_if
    sta_if.connect(essid, password)
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
    return sta_if


def create_an_network():
    """

    :return: connected WLAN class
    """
    ap_if.active(True)
    essid = "MyPlantMonitor"
    password = "MyPlant"
    ap_if.config(essid=essid, password=password, authmode=4)
    print('essid: %s, pw: %s' % (essid, password))
    print('network config:', ap_if.ifconfig())
    return ap_if
