"""
Created on Thur Apr 7 07:45 2016
process billboard ranking info
@author: xhong
"""

import sqlite3 as lite
import json

def form_track(song):
    track={}
    track['artist'] = track['EN_artist'] = song[1]
    track['title'] = track['EN_title'] = song[0]
    if track['artist'].find('Featuring') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('Featuring')-1]
    if track['artist'].find('With') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('With')-1]
    if track['artist'].find('&') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('&')-1]
    if track['artist'].find('/') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('/')-1]
    return track


def insert_into_DB(track):
    con_aDB = lite.connect('analyzeDB.db')
    with con_aDB:
        cur_aDB = con_aDB.cursor()
        question_mark_list = ['?'] * 39

        cur_aDB.execute('INSERT OR IGNORE INTO TrackEntries(ID,Title,Artist,EN_title,EN_artist,\
        Track_MBID,Artist_MBID,EN_ID,EN_artist_ID,LF_url,track_length,release_date,release_mbid,\
        artist_type,artist_gender,artist_begin_area,artist_begin_date,artist_country,artist_tags,\
        EN_artist_discovery,EN_artist_familiarity,EN_artist_hotness,EN_duration,EN_tempo,EN_valence,\
        EN_speechiness,EN_acousticness,EN_loudness,EN_liveness,EN_instrumentalness,EN_danceability,\
        EN_song_discovery,EN_song_hotness,EN_song_currency,EN_energy,LF_tags,LF_similar_songs,Lyrics,\
        RankInfo,Rating) VALUES (NULL,' + ', '.join(question_mark_list) + ')', single_entry)
    con_aDB.close()

def read_trackRank_DB(ID):
    con_tDB = lite.connect('trackRank.db')
    with con_tDB:
        cur_tDB = con_tDB.cursor()
        cur_tDB.execute("SELECT * FROM TrackEntries WHERE ID = ? ", ID)
        track_info = cur_tDB.fetchone()
    con_tDB.close()
    return track_info

def read_musicData_DB(title, artist):
    con_mDB = lite.connect('musicdata.db')
    with con_mDB:
        cur_mDB = con_mDB.cursor()
        cur_mDB.execute("SELECT * FROM TrackEntries WHERE SearchTitle = ? AND SearchArtist = ?", (title, artist))
        track_info = cur_mDB.fetchone()
    con_mDB.close()
    return track_info

def read_musicBrainz():
    return

track_list = get_distinct_tracks()
con = lite.connect('trackRank.db')
for enum, track1 in enumerate(track_list):
    print(enum, track1)
    track1_info = get_info(track1)
    rating = sum([(101 - item[1]) for item in track1_info])
    single_entry = tuple([track1[0], track1[1], json.dumps(track1_info), rating])
con.close()
'''track1 = track_list[0]
track1_info = get_info(track1)
print(track1_info)
rating = (sum([(101 - appear[1]) for appear in track1_info]))
single_entry = tuple([track1[0], track1[1], json.dumps(track1_info), rating])
'''