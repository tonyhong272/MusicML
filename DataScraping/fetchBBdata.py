# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:53:47 2016

@author: XH
"""
#%%
import billboard
import sqlite3 as lite
import time
#%%
scrapeDepth = 10 #number of charts to scrape
startingDate = None
#startingDate = '1984-01-28'
#%%
def insertChart2DB (chart):
    with con:
        cur = con.cursor()    
        #cur.execute("DROP TABLE IF EXISTS BoardEntries")
        cur.execute("CREATE TABLE IF NOT EXISTS SongEntries(ID TEXT PRIMARY KEY, BBDate TEXT, Title TEXT, Artist TEXT, Rank INT, PeakPos INT, LastPos INT, Weeks INT, Change TEXT, SpotifyLink TEXT)")
        for entry in chart:
            ID = chart.date + '-' + str(entry.rank)
            single_entry = [(ID, chart.date, entry.title, entry.artist, entry.rank, entry.peakPos, entry.lastPos, entry.weeks,entry.change, entry.spotifyLink)]
            cur.executemany('INSERT OR IGNORE INTO SongEntries VALUES (?,?,?,?,?,?,?,?,?,?)', single_entry)
            
def fetchDatesInDB():
    with con:
        cur = con.cursor()
        cur.execute('SELECT DISTINCT BBDate FROM SongEntries')
    return cur
    
def chartIsInDB (chart):
    availableDates = fetchDatesInDB()     
    return chart.date in availableDates
    
def scrapingChart(date):
    chart = billboard.ChartData('hot-100', date=date, fetch=True)
    print ('Now Scraping '+chart.date)
    time.sleep(0.1)
    return chart

#%%
con = lite.connect('billboardDB.db')

chart = scrapingChart(date = startingDate)
if not chartIsInDB(chart):
    insertChart2DB(chart)

for indx in range(scrapeDepth):
    chart = scrapingChart(chart.previousDate)
    if not chartIsInDB(chart):
        insertChart2DB(chart)
    
con.close()



#==============================================================================
# SELECT DISTINCT BBDate FROM SongEntries
# WHERE DATE(substr(BBDate,1,4)
# ||substr(BBDate,6,2)
# ||substr(BBDate,9,2)) 
# BETWEEN DATE(20131020) AND DATE(20161021);
#==============================================================================
