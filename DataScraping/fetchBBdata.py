# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:53:47 2016

@author: XH
"""

import billboard
import sqlite3 as lite


def insertChart2DB (chart):
    with con:
        cur = con.cursor()    
        #cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute("CREATE TABLE IF NOT EXISTS SongEntries(ID TEXT PRIMARY KEY, BBDate TEXT, Title TEXT, Artist TEXT, Rank INT, PeakPos INT, LastPos INT, Weeks INT, Change TEXT, SpotifyLink TEXT)")
        for entry in chart:
            ID = chart.date + '-' + str(entry.rank)
            single_entry = [(ID, chart.date, entry.title, entry.artist, entry.rank, entry.peakPos, entry.lastPos, entry.weeks,entry.change, entry.spotifyLink)]
            cur.executemany('INSERT INTO SongEntries VALUES (?,?,?,?,?,?,?,?,?,?)', single_entry)

chart = billboard.ChartData('hot-100', date=None, fetch=True)
con = lite.connect('billboardDB.db')
insertChart2DB(chart)
con.close()
