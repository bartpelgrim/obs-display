from unittest import mock

import pytest

from app.dataset import file_content_to_dataframe, obs_to_dict, ObservationData

from tests.helpers.mock_data import mock_data


class TestDataset:
    @pytest.fixture(autouse=True)
    def __around(self):
        with mock_data() as self.test_dataset:
            yield

    def test_file_content_to_dataframe(self):
        df = file_content_to_dataframe(self.test_dataset)
        assert df.ta[0] == 4.6

    def test_obs_to_dict(self):
        df = file_content_to_dataframe(self.test_dataset)
        result = obs_to_dict(df)
        assert len(result['observations']) == 52
        assert result['observations'][12] == {
            'name': 'DE KOOY VK',
            'lat': 52.926865008825,
            'lon': 4.7811453228565,
            'max_temperature_12h': 4.1,
            'min_temperature_12h': -2.9,
            'height': 1.22,
            'air_temperature': 4.1,
            'dew_point': -1.5,
            'air_pressure': 1035.44,
            'weather_code': 2.0,
            'wind_direction': 300.4,
            'wind_gust': 2.66,
            'wind_gust_kph': 10,
            'wind_speed': 1.77,
            'wind_speed_bft': 2,
        }


class TestObservationDataBase:
    @pytest.fixture(autouse=True)
    def __around(self):
        with open('tests/data/KMDS__OPER_P___10M_OBS_L2_202103060830.nc', 'rb') as test_file:
            with mock.patch('app.dataset.read_api_key', return_value=''):
                with mock.patch('app.knmi_obs.KnmiApi.get_latest_obs', return_value=test_file.read()):
                    self.obs_data = ObservationData()
                    self.obs_data.refresh()
                    yield

    def test_refresh(self):
        assert len(self.obs_data._obs_data) > 0

    def test_all(self):
        result = self.obs_data.all()
        assert len(result) == 1

    def test_latest(self):
        result = self.obs_data.latest()
        assert result['timestamp'] == 1615019400000

    def test_with_timestamp(self):
        result = self.obs_data.with_timestamp(1615019400000)
        assert result['timestamp'] == 1615019400000

    def test_with_timestamp_returns_none(self):
        assert self.obs_data.with_timestamp(1234) is None
