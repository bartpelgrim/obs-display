import os

APP_PATH = os.path.dirname(os.path.abspath(__file__))
API_KEY_PATH = os.path.join(APP_PATH, 'api_key.json')
DATABASE_PATH = os.path.join(APP_PATH, '..', 'data', 'obs.db')
OBSERVATION_TTL_DAYS = 5
