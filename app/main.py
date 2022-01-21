import json

from flask import Flask, request
from flask_cors import CORS

from app.exception import ApiException
from app.dataset import ObservationReader

app = Flask(__name__, static_folder='../ui/build', static_url_path='/')
CORS(app)

reader = ObservationReader()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/obs')
def get_obs():
    timestamp = request.args.get('timestamp')
    try:
        if timestamp:
            data = reader.with_timestamp(round(int(timestamp) / 1000))  # from javascript to python timestamp
        else:
            data = reader.latest()
        if data:
            return json.dumps(data)
        else:
            return "Timestamp not found", 404
    except ApiException as exc:
        print(exc)
        return exc.args[0], 500


@app.route('/station')
def get_station_timeseries():
    station_id_str = request.args.get('id')
    history_hours_str = request.args.get('historyHours', 3)
    try:
        station_id = int(station_id_str)
    except ValueError:
        return f"Invalid station_id: {station_id_str}", 400
    try:
        history_hours = int(history_hours_str)
    except ValueError:
        return f"Invalid history_hours: {history_hours_str}", 400

    result = reader.timeseries(station_id, history_hours=history_hours)

    return json.dumps({'timeseries': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
