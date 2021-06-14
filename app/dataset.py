from io import BytesIO
from typing import Dict, Optional

import pandas
from xarray import open_dataset

from app.conversions import mps_to_bft, mps_to_kph
from app.knmi_obs import KnmiApi


def read_api_key() -> str:
    with open('api_key.txt') as key_file:
        return key_file.read()


def file_content_to_dataframe(file_content: bytes) -> pandas.DataFrame:
    with BytesIO(file_content) as input_file:
        with open_dataset(input_file) as dataset:
            df = dataset.to_dataframe()
            return df


def obs_to_dict(df: pandas.DataFrame) -> Dict[str, list]:
    # replace NaN with None
    df_with_nones = df.where(pandas.notnull(df), None)
    station_list = []
    for row in df_with_nones.itertuples():
        station = dict(
            name=row.stationname,
            lat=row.lat,
            lon=row.lon,
            height=row.height,
            air_temperature=row.ta,
            max_temperature_12h=row.Tx12,
            min_temperature_12h=row.Tn12,
            dew_point=row.td,
            air_pressure=row.pp,
            weather_code=row.ww,
            wind_direction=row.dd,
            wind_speed=row.ff,
            wind_speed_bft=mps_to_bft(row.ff),
            wind_gust=row.gff,
            wind_gust_kph=mps_to_kph(row.gff),
        )
        station_list.append(station)

    timestamp = int(df.index[0][1].timestamp() * 1000)
    return {
        'timestamp': timestamp,
        'observations': station_list,
    }


class ObservationData:
    MAX_OBS_IN_CACHE = 10

    def __init__(self):
        self._obs_data = {}
        api_key = read_api_key()
        self.api = KnmiApi(api_key)

    def refresh(self):
        file_content = self.api.get_latest_obs()
        df = file_content_to_dataframe(file_content)
        new_obs = obs_to_dict(df)
        self._obs_data[new_obs['timestamp']] = new_obs

        # delete oldest observations when max size is reached
        while len(self._obs_data) > self.MAX_OBS_IN_CACHE:
            oldest_key = sorted(list(self._obs_data.keys()))[0]
            self._obs_data.pop(oldest_key)

    def latest(self):
        latest_key = sorted(list(self._obs_data.keys()))[-1]
        return self._obs_data[latest_key]

    def all(self):
        return list(self._obs_data.values())

    def with_timestamp(self, timestamp: int) -> Optional[dict]:
        return self._obs_data.get(timestamp)
