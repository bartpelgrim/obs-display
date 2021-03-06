from io import BytesIO
from typing import Dict

import pandas
from xarray import open_dataset

from app.conversions import mps_to_bft
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
            dew_point=row.td,
            air_pressure=row.pp,
            weather_code=row.ww,
            wind_direction=row.dd,
            wind_speed=row.ff,
            wind_speed_bft=mps_to_bft(row.ff),
        )
        station_list.append(station)

    return {
        'time': str(df.index[0][1]),
        'observations': station_list,
    }


class ObservationData:
    MAX_OBS_IN_CACHE = 10

    def __init__(self):
        self.obs_data = []
        api_key = read_api_key()
        self.api = KnmiApi(api_key)

    def refresh(self):
        file_content = self.api.get_latest_obs()
        df = file_content_to_dataframe(file_content)
        new_obs = obs_to_dict(df)
        self.obs_data.append(new_obs)

        # delete oldest observations when max size is reached
        while len(self.obs_data) > self.MAX_OBS_IN_CACHE:
            self.obs_data.pop(0)
