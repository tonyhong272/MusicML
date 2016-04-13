# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 13:25:55 2016
Fetch tracks info from EchoNest and LastFM
@author: xhong
"""
 
from musicBrainz import recordingSearch
import sqlite3 as lite

def form_track(song):
    track={}
    track['artist'] = song[1]
    track['title'] = song[0]
    if track['artist'].find('Featuring') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('Featuring')-1]
    if track['artist'].find('With') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('With')-1]
    if track['artist'].find('&') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('&')-1]
    if track['artist'].find('/') != -1:
        track['artist'] = track['artist'][0:track['artist'].find('/')-1]
    return track

def fetch_infos(track):
    recording_info = recordingSearch.fetch_recording(track['artist'], track['title'])
    artist_info = recordingSearch.fetch_artist(recording_info['artist_mbid'])
    info = track.copy()
    info.update(recording_info)
    info.update(artist_info)
    return info

def save_sqlite(track_info):
    con = lite.connect('mbInfo.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS TrackEntries(ID INTEGER PRIMARY KEY, title TEXT, artist TEXT, recording_length TEXT, \
                    recording_mbid TEXT, artist_mbid TEXT, release_date TEXT, release_mbid TEXT,artist_type TEXT, \
                    artist_gender TEXT, artist_begin_area TEXT, artist_begin_date TEXT, artist_country TEXT, artist_tags TEXT)")
        single_entry = tuple(track_info.values())
        print ','.join(track_info.keys())
        cur.execute('INSERT OR IGNORE INTO TrackEntries(ID,' + ','.join(track_info.keys()) + ') VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)', single_entry)
    con.close()

def fetch_BBSong_list():
    con1 = lite.connect('trackRank.db')
    cur1 = con1.cursor()
    cur1.execute("SELECT Title, Artist FROM TrackEntries ORDER BY ROWID")
    BBSong_List = cur1.fetchall()
    con1.close()
    return BBSong_List

if __name__ == '__main__':
    BBSongList = fetch_BBSong_list()
    count = 0
    for song in BBSongList:
        track = form_track(song)
        count += 1
        track_info = fetch_infos(track)
        save_sqlite(track_info)
        print count, str(track)
