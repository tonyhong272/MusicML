from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Spotify_Playlist(Base):
    __tablename__ = 'spotify_playlist'
    id = Column(Integer, primary_key=True)
    playlist_id = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    owner = Column(String(250), nullable=False)
    timestamps = Column(TIMESTAMP, nullable=False)
    playlist_url = Column(String(250), nullable=False)
    track_data = Column(String(6000), nullable=True)

engine = create_engine('sqlite:///spotify.db')
Base.metadata.create_all(engine)