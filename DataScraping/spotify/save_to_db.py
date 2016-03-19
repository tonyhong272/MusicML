from playlist import get_tracks_from_popular_playlists as get_playlists
from token_management import init_token

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_base import Spotify_Playlist, Base

from datetime import datetime, timedelta
from random import random

import json

def random_date(start, end):

    delta = end - start
    delta_seconds = delta.total_seconds()
    random_seconds = 1.0*delta_seconds*random()

    return start + timedelta(seconds=random_seconds)

engine = create_engine('sqlite:///spotify.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

end = datetime.now()
start = datetime.strptime('2015-01-01T00:00:01', '%Y-%m-%dT%H:%M:%S')

count = 0
searched = {}

headers, expire_sec = init_token()

expire_start = datetime.now()

while count < 1000:

    time_stamp = random_date(start, end)

    print('using time_stamp: ', time_stamp)
    time_stamp_string = time_stamp.strftime('%Y-%m-%dT%H:%M:%S')

    if time_stamp_string in searched:
        continue

    searched[time_stamp_string] = True
    playlists_data = get_playlists(headers, timestamp=time_stamp_string)

    for playlist_data in playlists_data:

        serialized_data = json.dumps(playlist_data['tracks_data'])

        new_playlist = Spotify_Playlist(playlist_id=playlist_data['playlist_id'],
                                    name=playlist_data['playlist_name'],
                                    owner=playlist_data['owner_id'],
                                    playlist_url=playlist_data['playlist_url'],
                                    track_data=serialized_data,
                                    timestamps=time_stamp)
        session.add(new_playlist)

    count = count + 1

    print(count)

    if count % 10 == 0:
        session.commit()

    delta_time = datetime.now() - expire_start
    if delta_time.total_seconds() >= expire_sec: # retrive another token
        headers, expire_sec = init_token()
        session.commit()


session.commit()