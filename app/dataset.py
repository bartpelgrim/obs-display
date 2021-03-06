from io import BytesIO
from typing import Dict, Union

import pandas
from xarray import open_dataset


def file_content_to_dataframe(file_content: bytes) -> pandas.DataFrame:
    with BytesIO(file_content) as input_file:
        with open_dataset(input_file) as dataset:
            df = dataset.to_dataframe()
            return df


def mps_to_bft(wind_speed: float) -> Union[int, None]:
    if wind_speed is None:
        return None
    elif wind_speed < 0.2:
        return 0
    elif wind_speed < 1.5:
        return 1
    elif wind_speed < 3.3:
        return 2
    elif wind_speed < 5.4:
        return 3
    elif wind_speed < 7.9:
        return 4
    elif wind_speed < 10.7:
        return 5
    elif wind_speed < 13.8:
        return 6
    elif wind_speed < 17.1:
        return 7
    elif wind_speed < 20.7:
        return 8
    elif wind_speed < 24.4:
        return 9
    elif wind_speed < 28.4:
        return 10
    elif wind_speed < 32.6:
        return 11
    else:
        return 12


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
        'observations': station_list,
    }
