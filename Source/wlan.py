import network
import time

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


def connect_to_existing_network(essid, password):
    print('connecting to network...')
    sta_if.active(True)
    if essid is None or password is None:
        print('essid or password is not set')
        return False
    sta_if.connect(essid, password)
    start_time = time.time()
    print("connecting")
    while not sta_if.isconnected() and start_time+10 >= time.time():
        print(".")
        time.sleep(1)
    if not sta_if.isconnected():
        sta_if.active(False)
        print('Connection NOT establisched')
    else:
        print('network config:', sta_if.ifconfig())
    return sta_if.isconnected()


def create_an_network():
    """

    :return: connected WLAN class
    """
    ap_if.active(True)
    essid = "MyPlantMonitor"
    password = "MyPlantMonitor"
    ap_if.config(essid=essid, password=password, authmode=4)
    print('essid: %s, pw: %s' % (essid, password))
