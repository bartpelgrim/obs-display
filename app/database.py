from typing import List, Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Station(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Float)

    def to_dict(self) -> dict:
        result = self.__dict__
        # remove unneeded keys
        result.pop('_sa_instance_state')

        return result


class Observation(Base):
    __tablename__ = 'observation'
    id = Column(Integer, autoincrement=True, primary_key=True)
    timestamp = Column(Integer)
    station_id = Column(Integer, ForeignKey('station.id'))

    # Temperature
    air_temperature_2m = Column(Float)
    air_temperature_2m_minimum_over_10min = Column(Float)
    air_temperature_2m_minimum_over_6h = Column(Float)
    air_temperature_2m_minimum_over_12h = Column(Float)
    air_temperature_2m_minimum_over_14h = Column(Float)
    air_temperature_10cm_minimum_over_10min = Column(Float)
    air_temperature_10cm_minimum_over_6h = Column(Float)
    air_temperature_10cm_minimum_over_12h = Column(Float)
    air_temperature_10cm_minimum_over_14h = Column(Float)
    air_temperature_2m_maximum_over_10min = Column(Float)
    air_temperature_2m_maximum_over_6h = Column(Float)
    air_temperature_2m_maximum_over_12h = Column(Float)
    air_temperature_2m_maximum_over_24h = Column(Float)

    # Humidity
    dew_point = Column(Float)
    relative_humidity = Column(Float)

    # Wind
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    wind_gust = Column(Float)

    # Pressure
    air_pressure_at_sea_level = Column(Float)

    # Precipitation
    rain_duration_past_1h = Column(Float)
    rain_amount_past_1h = Column(Float)
    rain_amount_past_6h = Column(Float)
    rain_amount_past_12h = Column(Float)
    rain_amount_past_24h = Column(Float)
    precipitation_duration_past_10min_rain_gauge = Column(Float)
    precipitation_duration_past_10min_pws = Column(Float)
    precipitation_intensity_past_10min_rain_gauge = Column(Float)
    precipitation_intensity_past_10min_pws = Column(Float)

    # Clouds
    cloud_base_height = Column(Float)
    cloud_base_height_layer_1 = Column(Float)
    cloud_base_height_layer_2 = Column(Float)
    cloud_base_height_layer_3 = Column(Float)
    cloud_cover_total = Column(Float)
    cloud_cover_layer_1 = Column(Float)
    cloud_cover_layer_2 = Column(Float)
    cloud_cover_layer_3 = Column(Float)

    # Radiation
    global_solar_radiation_past_10min = Column(Float)
    sunshine_duration = Column(Float)

    # Weather
    visibility = Column(Float)
    weather_code = Column(Integer)
    weather_code_past_10min = Column(Integer)
    present_weather = Column(Integer)

    station = relationship('Station')

    def to_dict(self) -> dict:
        result = self.__dict__
        result['station'] = self.station.to_dict()
        # remove unneeded keys
        result.pop('id')
        result.pop('_sa_instance_state')
        return result


class Database:
    def __init__(self, filepath, read=False):
        self.engine = create_engine(
            f'sqlite+pysqlite:///{filepath}',
            echo=False,
            future=True,
            connect_args={"check_same_thread": read}
        )
        self.session = None
        Base.metadata.create_all(self.engine)

    def __enter__(self):
        with Session(self.engine) as self.session:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_station(self, station: Station):
        # check if station already exists
        statement = select(Station).where(Station.id == station.id)
        result = self.session.execute(statement).first()
        if not result:
            self.session.add(station)
            self.session.commit()

    def get_station_by_id(self, station_id: int) -> Station:
        return self.session.get(Station, station_id)

    def get_all_stations(self) -> List[Station]:
        statement = select(Station)
        result = self.session.execute(statement).all()
        return [row.Station for row in result]

    def add_observations(self, observations: List[Observation]):
        for obs in observations:
            self.session.add(obs)
        self.session.commit()

    def get_observations_for_station(self, station_id: int, start_timestamp: int) -> List[Observation]:
        statement = select(Observation).where(Observation.station_id == station_id)\
            .where(Observation.timestamp > start_timestamp)\
            .order_by(Observation.timestamp)
        result = self.session.execute(statement).all()
        return [row.Observation for row in result]

    def get_latest_timestamp(self) -> Optional[int]:
        statement = select(Observation.timestamp).order_by(Observation.timestamp.desc()).limit(1)
        row = self.session.execute(statement).first()
        if row:
            return row.timestamp
        return None

    def get_observations_for_timestamp(self, timestamp: int) -> List[Observation]:
        statement = select(Observation).\
            where(Observation.timestamp == timestamp).\
            order_by(Observation.timestamp).\
            join(Station)
        result = self.session.execute(statement).all()
        return [row.Observation for row in result]
