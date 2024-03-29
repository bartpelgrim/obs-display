from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO
import json
import time

import pandas
from xarray import open_dataset

from app.config import OBSERVATION_TTL_DAYS, DATABASE_PATH, API_KEY_PATH
from app.conversions import mps_to_bft, mps_to_kph, weather_code_to_text
from app.database import Database, Observation, Station
from app.knmi_obs import KnmiApi
from app.language import Language


def read_api_key() -> str:
    with open(API_KEY_PATH) as key_file:
        content = key_file.read()
        return json.loads(content)['key']


def file_content_to_dataframe(file_content: bytes) -> pandas.DataFrame:
    with BytesIO(file_content) as input_file:
        with open_dataset(input_file) as dataset:
            df = dataset.to_dataframe()
            return df


@dataclass(frozen=True)
class ElementMapping:
    unit: str
    knmi_alias: str


mappings = {
    'air_temperature_2m': ElementMapping(unit='C', knmi_alias='ta'),
    'air_temperature_2m_minimum_over_10min': ElementMapping(unit='C', knmi_alias='tn'),
    'air_temperature_2m_minimum_over_6h': ElementMapping(unit='C', knmi_alias='Tn6'),
    'air_temperature_2m_minimum_over_12h': ElementMapping(unit='C', knmi_alias='Tn12'),
    'air_temperature_2m_minimum_over_14h': ElementMapping(unit='C', knmi_alias='Tn14'),
    'air_temperature_10cm_minimum_over_10min': ElementMapping(unit='C', knmi_alias='tgn'),
    'air_temperature_10cm_minimum_over_6h': ElementMapping(unit='C', knmi_alias='Tgn6'),
    'air_temperature_10cm_minimum_over_12h': ElementMapping(unit='C', knmi_alias='Tgn12'),
    'air_temperature_10cm_minimum_over_14h': ElementMapping(unit='C', knmi_alias='Tgn14'),
    'air_temperature_2m_maximum_over_10min': ElementMapping(unit='C', knmi_alias='tx'),
    'air_temperature_2m_maximum_over_6h': ElementMapping(unit='C', knmi_alias='Tx6'),
    'air_temperature_2m_maximum_over_12h': ElementMapping(unit='C', knmi_alias='Tx12'),
    'air_temperature_2m_maximum_over_24h': ElementMapping(unit='C', knmi_alias='Tx24'),
    'dew_point': ElementMapping(unit='C', knmi_alias='td'),
    'relative_humidity': ElementMapping(unit='%', knmi_alias='rh'),
    'wind_speed': ElementMapping(unit='m/s', knmi_alias='ff'),
    'wind_direction': ElementMapping(unit='degree', knmi_alias='dd'),
    'wind_gust': ElementMapping(unit='m/s', knmi_alias='gff'),
    'air_pressure_at_sea_level': ElementMapping(unit='hPa', knmi_alias='pp'),
    'rain_duration_past_1h': ElementMapping(unit='min', knmi_alias='D1H'),
    'rain_amount_past_1h': ElementMapping(unit='mm', knmi_alias='R1H'),
    'rain_amount_past_6h': ElementMapping(unit='mm', knmi_alias='R6H'),
    'rain_amount_past_12h': ElementMapping(unit='mm', knmi_alias='R12H'),
    'rain_amount_past_24h': ElementMapping(unit='mm', knmi_alias='R24H'),
    'precipitation_duration_past_10min_rain_gauge': ElementMapping(unit='sec', knmi_alias='dr'),
    'precipitation_duration_past_10min_pws': ElementMapping(unit='sec', knmi_alias='pr'),
    'precipitation_intensity_past_10min_rain_gauge': ElementMapping(unit='mm/h', knmi_alias='rg'),
    'precipitation_intensity_past_10min_pws': ElementMapping(unit='mm/h', knmi_alias='pg'),
    'cloud_base_height': ElementMapping(unit='ft', knmi_alias='hc'),
    'cloud_base_height_layer_1': ElementMapping(unit='ft', knmi_alias='hc1'),
    'cloud_base_height_layer_2': ElementMapping(unit='ft', knmi_alias='hc2'),
    'cloud_base_height_layer_3': ElementMapping(unit='ft', knmi_alias='hc3'),
    'cloud_cover_total': ElementMapping(unit='octa', knmi_alias='nc'),
    'cloud_cover_layer_1': ElementMapping(unit='octa', knmi_alias='nc1'),
    'cloud_cover_layer_2': ElementMapping(unit='octa', knmi_alias='nc2'),
    'cloud_cover_layer_3': ElementMapping(unit='octa', knmi_alias='nc3'),
    'global_solar_radiation_past_1min': ElementMapping(unit='W/m2', knmi_alias='qg'),
    'sunshine_duration': ElementMapping(unit='min', knmi_alias='ss'),
    'visibility': ElementMapping(unit='m', knmi_alias='zm'),
    'weather_code': ElementMapping(unit='', knmi_alias='ww'),
    'weather_code_past_10m': ElementMapping(unit='', knmi_alias='ww-10'),
    'present_weather': ElementMapping(unit='', knmi_alias='pwc'),
}


class ObservationWriter:
    UPDATE_INTERVAL_SECONDS = 300

    def __init__(self):
        api_key = read_api_key()
        self.api = KnmiApi(api_key)
        self.db = Database(DATABASE_PATH)

    def run(self):
        while True:
            self.ingest_latest_obs()
            self._delete_old_observations()
            time.sleep(self.UPDATE_INTERVAL_SECONDS)

    def ingest_latest_obs(self):
        file_content = self.api.get_latest_obs()
        if file_content:
            df = file_content_to_dataframe(file_content)
            obs_list = []
            timestamp = int(df.ta.index[0][1].timestamp())
            if (latest_timestamp := self.db.get_latest_timestamp()) and latest_timestamp == timestamp:
                print(f'timestep already in database: {datetime.fromtimestamp(timestamp).isoformat()}')
                return
            for row in df.itertuples():
                station_id = int(row.Index[0])
                station = Station(
                    id=station_id,
                    name=row.stationname,
                    latitude=row.lat,
                    longitude=row.lon,
                    height=row.height,
                )
                self.db.add_station(station)
                obs = Observation(
                    timestamp=int(row.Index[1].timestamp()),
                    station_id=station_id,
                )
                for element_name, mapping in mappings.items():
                    setattr(obs, element_name, getattr(row, mapping.knmi_alias, None))
                obs_list.append(obs)
            self.db.add_observations(obs_list)

    def _delete_old_observations(self):
        dt = (datetime.utcnow() - timedelta(days=OBSERVATION_TTL_DAYS))
        print(f'Deleting observations before {dt.isoformat()} UTC')
        deleted_row_count = self.db.delete_observations_before_timestamp(int(dt.timestamp()))
        print(f'{deleted_row_count} rows deleted from database')


class ObservationReader:
    def __init__(self):
        self.db = Database(DATABASE_PATH)

    @staticmethod
    def _calculate_alternative_units(obs_dict: dict):
        return {
            'wind_speed_bft': mps_to_bft(obs_dict.get('wind_speed')),
            'wind_gust_kph': mps_to_kph(obs_dict.get('wind_gust')),
        }

    @staticmethod
    def _post_process_obs(obs: list[dict]) -> list[dict]:
        result = []
        for o in obs:
            o['timestamp'] = o['timestamp'] * 1000  # from python to javascript timestamp
            o['wind_speed_bft'] = mps_to_bft(o.get('wind_speed'))
            o['wind_gust_kph'] = mps_to_kph(o.get('wind_gust'))
            if weather_code := o.get('weather_code'):
                o['weather_code_text'] = weather_code_to_text(weather_code, Language.NL)
            result.append(o)

        return result

    def latest(self) -> dict | None:
        latest_timestamp = self.db.get_latest_timestamp()
        latest_obs = self.db.get_observations_for_timestamp(latest_timestamp)

        if not latest_obs:
            return None

        obs_list = self._post_process_obs(latest_obs)
        result = {
            'timestamp': latest_timestamp * 1000,  # from python to javascript timestamp
            'observations': obs_list,
        }

        return result

    def with_timestamp(self, timestamp: int) -> dict | None:
        obs = self.db.get_observations_for_timestamp(timestamp)
        if not obs:
            return None

        obs_list = self._post_process_obs(obs)
        result = {
            'timestamp': timestamp * 1000,  # from python to javascript timestamp
            'observations': obs_list,
        }

        return result

    def timeseries(self, station_id: int, history_hours: int) -> list[dict]:
        start_timestamp = int((datetime.utcnow() - timedelta(hours=history_hours)).timestamp())
        obs = self.db.get_observations_for_station(station_id, start_timestamp)

        obs_list = self._post_process_obs(obs)

        return obs_list


if __name__ == '__main__':
    writer = ObservationWriter()
    writer.run()

