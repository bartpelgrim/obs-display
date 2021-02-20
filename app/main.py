import json

from flask import Flask
from flask_cors import CORS

from app.knmi_obs import KnmiApi
from app.dataset import file_content_to_dataframe, obs_to_dict

app = Flask(__name__, static_folder='../ui/build', static_url_path='/')
CORS(app)


def read_api_key() -> str:
    with open('api_key.txt') as key_file:
        return key_file.read()


api_key = read_api_key()
api = KnmiApi(api_key)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/obs')
def get_obs():
    file_content = api.get_latest_obs()
    df = file_content_to_dataframe(file_content)
    result = obs_to_dict(df)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
