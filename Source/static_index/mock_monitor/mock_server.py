import json

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


@app.route("/rest/data")
def data():
    return jsonify({"soil moisture": 26, "humidity": 61.1, "light": 0.5, "time": 576133356, "temperature": 18.4})


@app.route("/rest/sensor_history")
def history():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "example_history.json"), "r") as example_history:
        read = "["
        new_read = ""
        while True:
            last_read = new_read
            new_read = example_history.readline().replace("\n", "")
            if new_read == "":
                break
            else:
                if last_read != "":
                    read += ","
                read += new_read

        read += "]"

    return jsonify(json.loads(read)[:100])


@app.route("/rest/settings")
def settings():
    return jsonify(dict(
        wlan=dict(
            ssid="ss",
            password=None,
        ),
        reads_without_send=15,
        deepsleep_s=300,  # 10 minutes
        keep_alive_time_s=5,
        max_awake_time_s=20,  # 120 seconds after sending first request data.
        awake_time_for_config=180,  # 3 minutes
        request_url=None,
        added_infos_to_sensor_data=dict(),  # this dict adds additional information for the posted sensor_data
    ))


if __name__ == '__main__':
    app.run(port=8080)
