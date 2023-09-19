from copy import deepcopy

import pytest


from app.database import Database, Station, Observation


class TestDatabase:
    @pytest.fixture(autouse=True)
    def __around(self):
        self.db = Database(':memory:')
        self.de_bilt = Station(
            id=6260,
            name='De Bilt',
            latitude=52.0,
            longitude=6.0,
            height=4.8
        )

        self.de_bilt_copy = Station(
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

    def test_get_station_by_id(self):
        station = self.db.get_station_by_id(6260)
        assert station.name == 'De Bilt'

    def test_add_station_twice_does_nothing(self):
        self.db.add_station(self.de_bilt_copy)

    def test_get_all_stations(self):
        stations = self.db.get_all_stations()
        assert len(stations) == 2
        station_names = [s.name for s in stations]
        assert 'De Bilt' in station_names
        assert 'Eindhoven' in station_names

    def test_get_observations_for_station(self):
        result = self.db.get_observations_for_station(6260, 1637180800)
        assert len(result) == 2
        assert result[0]['station']['name'] == 'De Bilt'

        result = self.db.get_observations_for_station(6260, 1637180900)
        assert len(result) == 1

    def test_get_observations_for_timestamp(self):
        result = self.db.get_observations_for_timestamp(1637180862)
        assert len(result) == 2
        assert result[0]['timestamp'] == 1637180862

    def test_obs_to_dict(self):
        result = self.db.get_observations_for_station(6260, 1637180900)
        obs_dict = result[0]
        assert obs_dict['air_temperature_2m'] == 11.5
        assert obs_dict['station']['name'] == 'De Bilt'

