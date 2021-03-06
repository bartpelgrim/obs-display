import json

from flask import Flask
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
    try:
        dataset.refresh()
        if len(dataset.obs_data) > 0:
            return json.dumps(dataset.obs_data[-1])
        else:
            return None, 404
    except ApiException as exc:
        print(exc)
        return exc.args[0], 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
