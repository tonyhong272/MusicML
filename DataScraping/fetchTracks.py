# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 13:25:55 2016
Fetch tracks info from EchoNest and LastFM
@author: xhong
"""
 
from billboard import billboard
from echonest import fetchEchoNest
from lastfm import fetchLastFM
import sqlite3 as lite
import time
import types
import pickle
import os.path

def form_track(song):
    track={}
    track['artist'] = song[2]
    track['title'] = song[1]
    track['EN_artist'] = song[2]
    track['EN_title'] = song[1]
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
    trackInfoEchoNest = fetchEchoNest.get_songDict(song_title = track['title'].encode('utf8'), song_artist = track['artist'].encode('utf8'), is_saving_analysis = False)
    if trackInfoEchoNest != None:
        if 'title' in trackInfoEchoNest:
            track['EN_title'] = trackInfoEchoNest['title']
        if 'artist_name' in trackInfoEchoNest:
            track['EN_artist'] = trackInfoEchoNest['artist_name']
    else:
        print('Not fetched in EchoNest %s, %s'%(track['title'],track['artist']))
    if not is_in_db(track):
        trackInfoLastFM = fetchLastFM.get_song(artist = track['EN_artist'].encode('utf8'), name = track['EN_title'].encode('utf8'))
        if trackInfoLastFM == None:
            print('Not fetched in LastFM %s, %s'%(track['title'],track['artist']))
    else:
        print('found in database %s, %s'%(track['title'], track['artist']))
        trackInfoLastFM = None
    return [track, trackInfoEchoNest, trackInfoLastFM]

def is_in_db(track):
    con = lite.connect('musicdata.db')
    with con:
        cur = con.cursor()
        #cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute("SELECT rowid FROM TrackEntries WHERE (SearchTitle = ? and SearchArtist = ?) or (EN_title = ? and EN_artist_name = ?)", (track['title'],track['artist'], track['EN_title'],track['EN_artist']))
        existingEntry=cur.fetchone()
        if existingEntry is None:
            return False
        else:
            return True
        con.close()

def save_sqlite(track_info):
    [track, trackInfoEchoNest, trackInfoLastFM] = track_info
    convert_type_dict = {float:'REAL', unicode:'TEXT', int:'INTEGER', str:'TEXT'}
    
    EN_key_list = trackInfoEchoNest.keys()
    LF_key_list = trackInfoLastFM.keys()
    
    table_columns = []
    column_names = []
    question_mark_sign = []
    for key in EN_key_list:
        if type(trackInfoEchoNest[key]) != types.NoneType:
            column_names.append('EN_' + key)
            table_columns1 = ' '.join(['EN_' + key, convert_type_dict[type(trackInfoEchoNest[key])]])
            table_columns.append(table_columns1)
            question_mark_sign.append('?')
        else:
            trackInfoEchoNest.pop(key)
    
    for key in LF_key_list:
        if type(trackInfoLastFM[key]) != types.NoneType:
            column_names.append('LF_' + key)
            table_columns1 = ' '.join(['LF_' + key, convert_type_dict[type(trackInfoLastFM[key])]])
            table_columns.append(table_columns1)
            question_mark_sign.append('?')
        else:
            trackInfoLastFM.pop(key)

    con = lite.connect('musicdata.db')
    with con:
        cur = con.cursor()
        #cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute("SELECT ROWID FROM TrackEntries WHERE EN_title = ? and EN_artist_name = ?", (trackInfoEchoNest['title'],trackInfoEchoNest['artist_name']))
        existingEntry=cur.fetchone()
        if existingEntry is None:
            print('saving into database %s, %s'%(trackInfoEchoNest['title'], trackInfoEchoNest['artist_name']))
            single_entry = tuple([str(time.strftime("%Y-%m-%d %H:%M:%S")), track['title'], track['artist']] + trackInfoEchoNest.values() + trackInfoLastFM.values())
            cur.execute('INSERT OR IGNORE INTO TrackEntries(ID, EntryDate, SearchTitle, SearchArtist, ' + ', '.join(column_names) + ') VALUES (NULL, ?,?,?, ' + ', '.join(question_mark_sign)+')', single_entry)
        else:
            print('found in database %s, %s'%(trackInfoEchoNest['title'], trackInfoEchoNest['artist_name']))
    con.close()

def fetch_BBSong_list():
    con1 = lite.connect('billboardDB.db')
    cur1 = con1.cursor()
    cur1.execute("SELECT DISTINCT ROWID, Title, Artist FROM SongEntries ORDER BY ROWID")
    BBSong_List=cur1.fetchall()
    con1.close()
    return BBSong_List

BBSongList = fetch_BBSong_list()

count = 0
for song in BBSongList:
        time.sleep(3)
        count += 1
        track = form_track(song)
        if not is_in_db(track):
            track_info = fetch_infos(track)
            if track_info[1] != None and track_info[2] != None:
                    save_sqlite(track_info)
        else:
            print('already saved %s, %s'%(track['title'],track['artist']))
        print((count, song, time.strftime("%Y-%m-%d %H:%M:%S")))
