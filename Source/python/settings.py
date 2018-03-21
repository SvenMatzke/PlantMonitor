import gc
import ujson
import os

_settings_file = "settings.json"
_loaded_config = None


# config
def get_settings():
    """
    :rtype: dict
    """
    global _loaded_config
    if _loaded_config is None:
        if _settings_file not in os.listdir():
            return dict(
                wlan=dict(
                    ssid=None,
                    password=None,
                ),
                deepsleep_s=600,  # 10 minutes
                keep_alive_time_s=5,
                max_awake_time_s=20,  # 120 seconds after sending first request data.
                awake_time_for_config=180,  # 3 minutes
                request_url=None,
                added_infos_to_sensor_data=dict(),  # this dict adds additional information for the posted sensor_data
            )
        file_ptr = open(_settings_file, "r")
        try:
            settings = ujson.loads(file_ptr.read())
        except ValueError:
            os.remove(_settings_file)
            return dict(
                wlan=dict(
                    ssid=None,
                    password=None,
                ),
                deepsleep_s=600,  # 10 minutes
                keep_alive_time_s=5,
                max_awake_time_s=20,  # 120 seconds after sending first request data.
                awake_time_for_config=180,  # 3 minutes
                request_url=None,
                added_infos_to_sensor_data=dict(),  # this dict adds additional information for the posted sensor_data
            )
        finally:
            file_ptr.close()
        _loaded_config = settings
    return _loaded_config


def save_settings(old_config, new_config):
    """

    :type old_config: dict
    :type new_config: dict
    :rtype: dict
    """
    # Wlan
    if new_config.get("wlan", None) is None:
        new_config['wlan'] = old_config.get('wlan',
                                            dict(
                                                ssid=None,
                                                password=None,
                                            )
                                            )

    # Deepsleep
    deepsleep_s = new_config.get('deepsleep_s', old_config.get('deepsleep_s', 600))
    if deepsleep_s <= 0:  # No Deepsleep
        new_config['deepsleep_s'] = deepsleep_s
    if deepsleep_s >= 3600:  # more only every hour seems odd
        new_config['deepsleep_s'] = 3600

    # timer if connected to a network
    # reset time till max_awake_time_s
    keep_alive_time_s = new_config.get('keep_alive_time_s', old_config.get('keep_alive_time_s', 30))
    max_awake_time_s = new_config.get('max_awake_time_s', old_config.get('max_awake_time_s', 120))
    if max_awake_time_s < keep_alive_time_s:
        keep_alive_time_s = max_awake_time_s
    new_config['keep_alive_time_s'] = keep_alive_time_s
    new_config['max_awake_time_s'] = max_awake_time_s

    # timer if connecting to a network failed
    awake_time_for_config = new_config.get('awake_time_for_config', old_config.get('awake_time_for_config', 180))
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
        file_ptr.write(ujson.dumps(old_config))
    finally:
        file_ptr.close()
    gc.collect()
    # return new config
    return new_config
