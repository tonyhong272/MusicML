from pyechonest import song
#buckets=["song_hotttnesss", "song_hotttnesss_rank", "artist_familiarity", "artist_familiarity_rank", "artist_hotttnesss", "artist_hotttnesss_rank", 
#"artist_discovery", "artist_discovery_rank", "audio_summary", "artist_location", "tracks", "song_type", "song_discovery", "song_discovery_rank", 
#"song_currency", "song_currency_rank", "id:7digital-US", "id:7digital-AU", "id:7digital-UK", "id:facebook", "id:fma", "id:twitter", "id:spotify-WW", 
#"id:seatwave", "id:lyricfind-US", "id:jambase", "id:musixmatch-WW", "id:seatgeek","id:openaura", "id:spotify", "id:spotify-WW", "id:tumblr",]

buckets=["song_hotttnesss", "song_hotttnesss_rank", "artist_familiarity", "artist_familiarity_rank", "artist_hotttnesss", "artist_hotttnesss_rank", 
"artist_discovery", "artist_discovery_rank", "audio_summary", "artist_location", "song_type", "song_discovery", "song_discovery_rank", 
"song_currency", "song_currency_rank"]

def get_tempo(artist, title):
    "gets the tempo for a song"
    results = song.search(artist=artist, title=title, results=1, buckets=buckets)
    if len(results['response']['songs']) > 0:
        return results['response']['songs'][0]
    else:
        return None

def get_songDict(song_title,song_artist,is_saving_analysis):
    argu = ['',song_artist, song_title]
    tempo = get_tempo(argu[1], argu[2])
    if tempo:
#        print 'Tempo for', argu[1], argu[2], 'is', tempo
        tempo.update(tempo['audio_summary'])
        tempo.update(tempo['artist_location'])
        tempo.pop('audio_summary')
        tempo.pop('artist_location')
        tempo['song_type_string'] = ';'.join(tempo['song_type'])
        tempo.pop('song_type')
        tempo['saveFile'] = ''
        songDict = tempo.copy()
        if is_saving_analysis:
            songDict['saveFile'] = songDict.get('id') + '.txt'
            save_analysis(songDict)
        return songDict
    else:
        print "Can't find track for artist:", argu[1], 'song:', argu[2]

def save_analysis (songDict):
    import urllib, json
    url = songDict['analysis_url']
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    with open(songDict.get('id') + '.txt', 'w') as outfile:
        json.dump(data, outfile)

#newSong = get_songDict(song_title = 'umbrella', song_artist = 'Rihanna', is_saving_analysis = True)