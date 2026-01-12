from contextlib import contextmanager
import os

from app.config import APP_PATH


@contextmanager
def mock_data():
    data_path = os.path.join(APP_PATH, '..', 'tests/data/KMDS__OPER_P___10M_OBS_L2_202103060830.nc')
    with open(data_path, 'rb') as test_file:
        test_dataset = test_file.read()
        yield test_dataset
