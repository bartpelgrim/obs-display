from io import BytesIO
from typing import Dict

import pandas
from xarray import open_dataset


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
            wind_speed=row.ff
        )
        station_list.append(station)

    return {
        'observations': station_list,
    }
