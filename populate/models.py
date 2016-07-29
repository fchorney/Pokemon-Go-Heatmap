from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from geoalchemy2 import Geometry

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = 'pokemons'
    encounter_id = Column(String, primary_key=True, nullable=False)
    spawnpoint_id = Column(String, nullable=False)
    disappear_time = Column(DateTime(timezone=True), nullable=False)
    pokemon_id = Column(Integer, nullable=False)
    pokemon_name = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))


class Gym(Base):
    __tablename__ = 'gyms'
    gym_id = Column(String, primary_key=True, nullable=False)
    gym_points = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False)
    guard_pokemon_id = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=False)
    last_modified = Column(DateTime(timezone=True), nullable=False)
    time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
