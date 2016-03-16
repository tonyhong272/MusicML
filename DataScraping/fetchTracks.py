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

def fetch_list(date = '2015-06-27'):
    chart = billboard.ChartData('hot-100', date, fetch=True)
    fetchList = []
    for entry in chart:
        if entry.artist.find('Featuring') != -1:
            entry.artist = entry.artist[0:entry.artist.find('Featuring')-1]
        if entry.artist.find('With') != -1:
            entry.artist = entry.artist[0:entry.artist.find('With')-1]
        if entry.artist.find('&') != -1:
            entry.artist = entry.artist[0:entry.artist.find('&')-1]
        if entry.artist.find('/') != -1:
            entry.artist = entry.artist[0:entry.artist.find('/')-1]
        fetchList.append({'title':entry.title, 'artist':entry.artist})
    return fetchList

def fetch_infos(track):
    trackInfoEchoNest = fetchEchoNest.get_songDict(song_title = track['title'].encode('utf8'), song_artist = track['artist'].encode('utf8'), is_saving_analysis = False)
    if trackInfoEchoNest != None:
        if 'title' in trackInfoEchoNest:
            track['title'] = trackInfoEchoNest['title']
        if 'artist_name' in trackInfoEchoNest:
            track['artist'] = trackInfoEchoNest['artist_name']
    else:
        print('Not fetched in EchoNest %s, %s'%(track['title'],track['artist']))
    if not is_in_db(track):
        trackInfoLastFM = fetchLastFM.get_song(artist = track['artist'].encode('utf8'), name = track['title'].encode('utf8'))
        if trackInfoLastFM == None:
            print('Not fetched in LastFM %s, %s'%(track['title'],track['artist']))
    else:
        print('found in database 1 %s, %s'%(track['title'], track['artist']))
        trackInfoLastFM = None
    return [trackInfoEchoNest, trackInfoLastFM]

def save_sqlite(track_info):
    [trackInfoEchoNest, trackInfoLastFM] = track_info
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
    
    for key in LF_key_list:
        if type(trackInfoLastFM[key]) != types.NoneType:
            column_names.append('LF_' + key)
            table_columns1 = ' '.join(['LF_' + key, convert_type_dict[type(trackInfoLastFM[key])]])
            table_columns.append(table_columns1)
            question_mark_sign.append('?')

    con = lite.connect('musicdata.db')
    with con:
        cur = con.cursor()
        #cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute("CREATE TABLE IF NOT EXISTS TrackEntries(ID INTEGER PRIMARY KEY AUTOINCREMENT, " + ', '.join(table_columns) +")")
        cur.execute("SELECT rowid FROM TrackEntries WHERE EN_title = ? and EN_artist_name = ?", (trackInfoEchoNest['title'],trackInfoEchoNest['artist_name']))
        existingEntry=cur.fetchone()
        if existingEntry is None:
            print('saving into database %s, %s'%(trackInfoEchoNest['title'], trackInfoEchoNest['artist_name']))
            single_entry = tuple(trackInfoEchoNest.values() + trackInfoLastFM.values())
            cur.execute('INSERT OR IGNORE INTO TrackEntries(ID, ' + ', '.join(column_names) + ') VALUES (NULL,' + ', '.join(question_mark_sign)+')', single_entry)
        else:
            print('found in database %s, %s'%(trackInfoEchoNest['title'], trackInfoEchoNest['artist_name']))
    con.close()

def fetch_BBdates_list():
    con1 = lite.connect('billboardDB.db')
    cur1 = con1.cursor()
    cur1.execute("SELECT DISTINCT BBDate FROM SongEntries WHERE DATE(substr(BBDate,1,4)||substr(BBDate,6,2)||substr(BBDate,9,2))BETWEEN DATE(19950101) AND DATE(20140802);")
    BBdates_list=cur1.fetchall()
    return BBdates_list

def is_in_db(track):
    con = lite.connect('musicdata.db')
    with con:
        cur = con.cursor()
        #cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute("SELECT rowid FROM TrackEntries WHERE EN_title = ? and EN_artist_name = ?", (track['title'],track['artist']))
        existingEntry=cur.fetchone()
        if existingEntry is None:
            return False
        else:
            return True
        con.close()

BBdates_list = fetch_BBdates_list()
for BB_date in reversed(BBdates_list):
    fetchList = fetch_list(BB_date[0])
    print('Now fetching list of ' + BB_date[0])
    count = 0
    for track in fetchList:
        if not is_in_db(track):
            time.sleep(3)
            track_info = fetch_infos(track)
            if track_info[0] != None and track_info[1] != None:
                save_sqlite(track_info)
        else:
            print('already saved %s, %s'%(track['title'],track['artist']))
        count = count + 1
        print((count, time.strftime("%Y-%m-%d %H:%M:%S")))