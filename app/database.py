from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, select, delete
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
    def __init__(self, filepath: Path):
        self.db_path = filepath
        new_database = False
        if not self.db_path.exists():
            print(f'creating new database at {str(self.db_path)}')
            self.db_path.parent.mkdir(exist_ok=True)  # creates data directory if doesn't exist
            new_database = True
        self.engine = create_engine(
            f'sqlite+pysqlite:///{filepath}',
            echo=False,
            future=True,
            connect_args={"check_same_thread": False}
        )
        if new_database:
            Base.metadata.create_all(self.engine)

    def add_station(self, station: Station):
        # check if station already exists
        with Session(self.engine) as session:
            statement = select(Station).where(Station.id == station.id)
            result = session.execute(statement).first()
            if not result:
                session.add(station)
                session.commit()

    def get_station_by_id(self, station_id: int) -> Station | None:
        with Session(self.engine) as session:
            return session.get(Station, station_id)

    def get_all_stations(self) -> list[Station]:
        statement = select(Station)
        with Session(self.engine) as session:
            result = session.execute(statement).all()
        return [row.Station for row in result]

    def add_observations(self, observations: list[Observation]):
        with Session(self.engine) as session:
            for obs in observations:
                session.add(obs)
            session.commit()

    def get_observations_for_station(self, station_id: int, start_timestamp: int) -> list[dict]:
        statement = select(Observation).where(Observation.station_id == station_id)\
            .where(Observation.timestamp > start_timestamp)\
            .order_by(Observation.timestamp)
        with Session(self.engine) as session:
            result = session.execute(statement).all()
            return [row.Observation.to_dict() for row in result]

    def get_latest_timestamp(self) -> int | None:
        statement = select(Observation.timestamp).order_by(Observation.timestamp.desc()).limit(1)
        with Session(self.engine) as session:
            row = session.execute(statement).first()
        if row:
            return row.timestamp
        return None

    def get_observations_for_timestamp(self, timestamp: int) -> list[dict]:
        statement = select(Observation).\
            where(Observation.timestamp == timestamp).\
            order_by(Observation.timestamp).\
            join(Station)
        with Session(self.engine) as session:
            result = session.execute(statement).all()
            return [row.Observation.to_dict() for row in result]

    def delete_observations_before_timestamp(self, timestamp: int) -> int:
        statement = delete(Observation).where(Observation.timestamp < timestamp)
        with Session(self.engine) as session:
            result = session.execute(statement)
            deleted_row_count = result.rowcount
            session.commit()
        return deleted_row_count
