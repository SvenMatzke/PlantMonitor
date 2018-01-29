import json
import os

_settings_file = "settings.json"
# config

_default_config = dict(
    wlan=dict(
        ssid=None,
        password=None,
    ),
    deepsleep_s=600,  # 10 minutes
    keep_alive_time_s=30,  # reset time till max_awake_time_s
    max_awake_time_s=120,  # 120 seconds after sending first request data.
    awake_time_for_config=300,  # 5 minutes
    request_retries=3,  # max retries after awake_time_for_config will be aktive
    request_url=None,
    added_infos_to_sensor_data=dict(),  # this dict adds additional information for the posted sensor_data
)


def get_settings():
    """
    :rtype: dict
    """
    if _settings_file not in os.listdir():
        return _default_config
    file_ptr = open(_settings_file, "r")
    try:
        settings = json.load(file_ptr)
    finally:
        file_ptr.close()
    return settings


def save_settings(old_config, new_config):
    """

    :type old_config: dict
    :type new_config: dict
    :rtype: dict
    """
    # Wlan
    if new_config.get("wlan", None) is None:
        new_config['wlan'] = old_config.get('wlan', _default_config['wlan'])

    # Deepsleep
    deepsleep_s = new_config.get('deepsleep_s', old_config.get('deepsleep_s', _default_config['deepsleep_s']))
    if deepsleep_s <= 0:  # No Deepsleep
        new_config['deepsleep_s'] = deepsleep_s
    if deepsleep_s >= 3600:  # more only every hour seems odd
        new_config['deepsleep_s'] = 3600

    # timer if connected to a network
    keep_alive_time_s = new_config.get('keep_alive_time_s',
                                       old_config.get('keep_alive_time_s',
                                                      _default_config['keep_alive_time_s']))
    max_awake_time_s = new_config.get('max_awake_time_s',
                                      old_config.get('max_awake_time_s',
                                                     _default_config['max_awake_time_s']))
    if max_awake_time_s < keep_alive_time_s:
        keep_alive_time_s = max_awake_time_s
    new_config['keep_alive_time_s'] = keep_alive_time_s
    new_config['max_awake_time_s'] = max_awake_time_s

    # timer if connecting to a network failed
    request_retries = new_config.get('request_retries',
                                     old_config.get('request_retries',
                                                    _default_config['request_retries']))
    if request_retries <= 0:
        request_retries = 1
    new_config['request_retries'] = request_retries

    awake_time_for_config = new_config.get('awake_time_for_config',
                                           old_config.get('awake_time_for_config',
                                                          _default_config['awake_time_for_config']))
    if awake_time_for_config <= 60:
        awake_time_for_config = 60
    new_config['awake_time_for_config'] = awake_time_for_config

    # request and additional information
    if new_config.get('added_infos_to_sensor_data', None) is None:
        new_config['added_infos_to_sensor_data'] = old_config.get('added_infos_to_sensor_data', dict())

    if new_config.get('request_url', None) is None:
        new_config['request_url'] = old_config.get('request_url', None)

    # save config
    file_ptr = open(_settings_file, "w")
    try:
        json.dump(file_ptr, old_config)
    finally:
        file_ptr.close()
    # return new config
    return new_config
