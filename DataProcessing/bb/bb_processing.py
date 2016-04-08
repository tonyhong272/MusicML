"""
Created on Thur Apr 7 07:45 2016
process billboard ranking info
@author: xhong
"""

import sqlite3 as lite
import json


def get_distinct_tracks():
    con = lite.connect('billboardDB.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT DISTINCT title, artist FROM SongEntries")
        all_tracks = cur.fetchall()
    con.close()
    return all_tracks


def get_info(track):
    con = lite.connect('billboardDB.db')
    with con:
        cur = con.cursor()
        # cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute(
            "SELECT BBdate, Rank FROM SongEntries WHERE title = ? AND artist = ?",
            (track[0], track[1]))
        track_info = cur.fetchall()
    con.close()
    return track_info


track_list = get_distinct_tracks()
con = lite.connect('trackRank.db')
for enum, track1 in enumerate(track_list):
    print(enum, track1)
    track1_info = get_info(track1)
    rating = sum([(101 - item[1]) for item in track1_info])
    single_entry = tuple([track1[0], track1[1], json.dumps(track1_info), rating])
    with con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS TrackEntries(ID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Artist TEXT, RankInfo TEXT, Rating INT)")
        cur.execute('INSERT OR IGNORE INTO TrackEntries(ID, Title, Artist, RankInfo, Rating) VALUES (NULL, ?,?,?,?)',
                    single_entry)
con.close()
'''track1 = track_list[0]
track1_info = get_info(track1)
print(track1_info)
rating = (sum([(101 - appear[1]) for appear in track1_info]))
single_entry = tuple([track1[0], track1[1], json.dumps(track1_info), rating])
'''