from flask import Flask
from flask_cors import CORS


app = Flask(__name__, static_folder='../ui/build', static_url_path='/')
CORS(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
