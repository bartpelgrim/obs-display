from unittest import mock

import pytest

from app.database import Database, Observation, Station
from app.dataset import file_content_to_dataframe, ObservationReader, ObservationWriter

from tests.helpers.mock_data import mock_data


class TestDataset:
    @pytest.fixture(autouse=True)
    def __around(self):
        with mock_data() as self.test_dataset:
            yield

    def test_file_content_to_dataframe(self):
        df = file_content_to_dataframe(self.test_dataset)
        assert df.ta[0] == 4.6


class TestObservationWriter:
    @pytest.fixture(autouse=True)
    def __around(self):
        with open('tests/data/KMDS__OPER_P___10M_OBS_L2_202103060830.nc', 'rb') as test_file:
            with mock.patch('app.dataset.read_api_key', return_value=''):
                with mock.patch('app.knmi_obs.KnmiApi.get_latest_obs', return_value=test_file.read()):
                    with mock.patch('app.dataset.DATABASE_PATH', ':memory:'):
                        self.obs_data = ObservationWriter()
                        yield

    def test_ingest_latest_obs(self):
        self.obs_data.ingest_latest_obs()


class TestObservationReader:
    @pytest.fixture(autouse=True)
    def __around(self):
        with Database(':memory:') as self.db:
            self.de_bilt = Station(
                id=6260,
                name='De Bilt',
                latitude=52.0,
                longitude=6.0,
                height=4.8
            )

            self.eindhoven = Station(
                id=6370,
                name='Eindhoven',
                latitude=51.5,
                longitude=6.5,
                height=14.8
            )
            self.obs1 = Observation(
                timestamp=1637180862,
                station_id=6260,
                air_temperature_2m=11.2,
                dew_point=4.7,
                wind_speed=2.4
            )
            self.obs2 = Observation(
                timestamp=1637180962,
                station_id=6260,
                air_temperature_2m=11.5,
                dew_point=4.9,
                wind_speed=2.1
            )
            self.obs3 = Observation(
                timestamp=1637180862,
                station_id=6370,
                air_temperature_2m=12.2,
                dew_point=4.0,
                wind_speed=1.4
            )
            self.obs4 = Observation(
                timestamp=1637180962,
                station_id=6370,
                air_temperature_2m=13.2,
                dew_point=4.2,
                wind_speed=1.7
            )
            self.db.add_station(self.de_bilt)
            self.db.add_station(self.eindhoven)
            self.db.add_observations([self.obs1, self.obs2, self.obs3, self.obs4])
            with mock.patch('app.database.Database.__enter__', self.db):
                self.reader = ObservationReader()
                yield

    def test_latest(self):
        result = self.reader.latest()
        assert result == {
            'timestamp': 1637180962000,
            'observations': [
                {
                    'timestamp': 1637180962000,
                    'station': {
                        'id': 6260,
                        'name': 'De Bilt',
                        'latitude': 52.0,
                        'longitude': 6.0,
                        'height': 4.8,
                    },
                    'air_temperature_2m': 11.5,
                    'dew_point': 4.9,
                    'wind_speed': 2.1,
                    'wind_speed_bft': 2,
                    'wind_gust_kph': None,
                },
                {
                    'timestamp': 1637180962000,
                    'station': {
                        'id': 6370,
                        'name': 'Eindhoven',
                        'latitude': 51.5,
                        'longitude': 6.5,
                        'height': 14.8,
                    },
                    'air_temperature_2m': 13.2,
                    'dew_point': 4.2,
                    'wind_speed': 1.7,
                    'wind_speed_bft': 2,
                    'wind_gust_kph': None,
                },
            ]

        }

    def test_with_timestamp(self):
        result = self.obs_data.with_timestamp(1615019400000)
        assert result['timestamp'] == 1615019400000

    def test_with_timestamp_returns_none(self):
        assert self.obs_data.with_timestamp(1234) is None

    def test_timeseries(self):
        result = self.obs_data.timeseries('AWG-1')
        assert len(result) == 1
        assert result[0]['name'] == 'AWG-1'

    def test_timeseries_returns_empty_list_with_unknown_station(self):
        result = self.obs_data.timeseries('oops')
        assert len(result) == 0
