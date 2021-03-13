import pytest

from app.dataset import file_content_to_dataframe, obs_to_dict


class TestDataset:
    @pytest.fixture(autouse=True)
    def __around(self):
        with open('tests/data/KMDS__OPER_P___10M_OBS_L2_202103060830.nc', 'rb') as test_file:
            self.test_dataset = test_file.read()
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
