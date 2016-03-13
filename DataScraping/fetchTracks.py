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

def fetch_list():
    chart = billboard.ChartData('hot-100', date='2015-04-11', fetch=True)
    fetchList = []
    for entry in chart:
        if entry.artist.find('Featuring') != -1:
            entry.artist = entry.artist[0:entry.artist.find('Featuring')-1]
        fetchList.append({'title':entry.title, 'artist':entry.artist})
    return fetchList


fetchList = fetch_list()
track = fetchList[1]
trackInfoEchoNest = fetchEchoNest.get_songDict(song_title = track['title'], song_artist = track['artist'], is_saving_analysis = False)
if trackInfoEchoNest['title']:
    track['title'] = trackInfoEchoNest['title']
if trackInfoEchoNest['artist_name']:
    track['artist'] = trackInfoEchoNest['artist_name']

trackInfoLastFM = fetchLastFM.get_song(artist = track['artist'] , name = track['title'])
if 'album_title' in trackInfoLastFM:
    albumInfoLastFM = fetchLastFM.get_album(artist = track['artist'], album = trackInfoLastFM['album_title'])
artistInfoLastFM = fetchLastFM.get_artist(track['artist'])

convert_type_dict = {float:'REAL', unicode:'TEXT', int:'INTEGER', str:'TEXT'}
EN_key_list = trackInfoEchoNest.keys()
LF_key_list = trackInfoLastFM.keys()

table_columns = []
column_names = []
question_mark_sign = []
for key in EN_key_list:
    column_names.append('EN_' + key)
    table_columns1 = ' '.join(['EN_' + key, convert_type_dict[type(trackInfoEchoNest[key])]])
    table_columns.append(table_columns1)
    question_mark_sign.append('?')

for key in LF_key_list:
    column_names.append('LF_' + key)
    table_columns1 = ' '.join(['LF_' + key, convert_type_dict[type(trackInfoLastFM[key])]])
    table_columns.append(table_columns1)
    question_mark_sign.append('?')



con = lite.connect('musicdata.db')
with con:
    cur = con.cursor()
    #cur.execute("DROP TABLE IF EXISTS BoardEntries")
    cur.execute("CREATE TABLE IF NOT EXISTS TrackEntries(ID INTEGER PRIMARY KEY AUTOINCREMENT, " + ', '.join(table_columns) +")")
    single_entry = tuple(trackInfoEchoNest.values() + trackInfoLastFM.values())
    cur.execute('INSERT OR IGNORE INTO TrackEntries(ID, ' + ', '.join(column_names) + ') VALUES (NULL,' + ', '.join(question_mark_sign)+')', single_entry)
con.close()