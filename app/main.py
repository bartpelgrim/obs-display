import json

from flask import Flask, request
from flask_cors import CORS

from app.exception import ApiException
from app.dataset import ObservationData

app = Flask(__name__, static_folder='../ui/build', static_url_path='/')
CORS(app)

dataset = ObservationData()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/obs')
def get_obs():
    timestamp = request.args.get('timestamp')
    try:
        if timestamp:
            data = dataset.with_timestamp(timestamp)
        else:
            dataset.refresh()
            data = dataset.latest()
        if data:
            return json.dumps(data)
        else:
            return None, 404
    except ApiException as exc:
        print(exc)
        return exc.args[0], 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
