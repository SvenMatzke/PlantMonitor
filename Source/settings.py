

# config
def get_settings():
    """
    :rtype: dict
    """
    return dict(
        maschine_config=dict(
            dht_pin=4,
            soil_moisture_pin=0,
            light_pin=None,
        ),
        wlan=dict(
            ssid=None,
            password=None,
        ),
        deepsleep_s=600,    # 10 minutes
        keep_alive_time_s=0,
        max_awake_time_s=0,    # 0 seconds after sending first request data.
        awake_time_for_config=300,  # 5 minutes
        request_retries=3,
        max_data_logt=30,
        request_address="192.168.0.1/plantlog",
        plantid=None,
    )

"""
Plan for awake_time is server will get data from the plant and evaluate if we need watering or not.
if we water the plant, we will request this plant sensor for new sensor data.

For this to be working we will be able to set a max_awake_time_s like 2 minutes and a keep_alive_time_s.
every request will renew the keep_alive_timer. 
if either keep_alive_timer or max_awake_time_s runs out we will go to deep_sleep
"""
