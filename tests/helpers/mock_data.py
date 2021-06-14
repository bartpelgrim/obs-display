from contextlib import contextmanager


@contextmanager
def mock_data():
    with open('tests/data/KMDS__OPER_P___10M_OBS_L2_202103060830.nc', 'rb') as test_file:
        test_dataset = test_file.read()
        yield test_dataset
