# -*- coding: utf-8 -*-
"""
Created on Sun Mar 06 15:52:13 2016

@author: xhong
"""

"""
http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=2a59114aa8b3e871fe76e14d3380ad98&artist=rihanna&track=umbrella&format=json
"""


import urllib
import httplib
import json

def connection (params):
    lastfm = httplib.HTTPConnection("ws.audioscrobbler.com")
    lastfm.request("GET","/2.0/?",params)
    response = lastfm.getresponse()
    json_response = json.loads(response.read())
    return json_response

def get_song(artist, name):
    params = urllib.urlencode({'method' : 'track.getInfo',
                   'artist' : artist,
                   'track' : name,
                   'limit' : '5',
                   'api_key' : '2a59114aa8b3e871fe76e14d3380ad98',
                   'format':'json'})
    json_response = connection (params)
    
    if 'track' in json_response:
        track_dict_temp = json_response['track']
    else:
        raise ValueError('no track is retrieved')
    
    if 'wiki' in track_dict_temp:
        track_dict_temp.update(track_dict_temp.pop('wiki'))
    if 'streamable' in track_dict_temp:
        track_dict_temp.pop('streamable')
    
    if 'toptags' in track_dict_temp:
        tag_list = []
        for tag_dicts in track_dict_temp.pop('toptags')['tag']:
            tag_list.append(tag_dicts['name'])
        track_dict_temp['tags'] = ";".join(tag_list)
    
    if 'artist' in track_dict_temp:
        artist_info = track_dict_temp.pop('artist')
        artist_info1 = {};
        for artist_key in artist_info:
            artist_info1['artist_' + artist_key] = artist_info[artist_key]      
        track_dict_temp.update(artist_info1)
    
    if 'album' in track_dict_temp:
        album_info = track_dict_temp.pop('album')
        album_info.pop('@attr')
        album_info.pop('image')
        album_info1 = {};
        for album_key in album_info:
            album_info1['album_' + album_key] = album_info[album_key]
        track_dict_temp.update(album_info1)

