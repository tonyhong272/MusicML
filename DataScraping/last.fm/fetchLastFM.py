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
#import dateutil.parser
import re

def connection (params, **kwarg):
    '''
    This function connects to the api host and fetch json response.
    '''
    lastfm = httplib.HTTPConnection("ws.audioscrobbler.com")
    lastfm.request("GET","/2.0/?",params)
    response = lastfm.getresponse()
    json_response = json.loads(response.read())
    return json_response

def get_song(artist, name,**kwarg):
    '''
    This function gets the song info in a dictionary.
    '''
    params = urllib.urlencode({'method' : 'track.getInfo',
                   'artist' : artist,
                   'track' : name,
                   'limit' : '5',
                   'api_key' : '2a59114aa8b3e871fe76e14d3380ad98',
                   'format':'json'})
    json_response = connection (params)
    if 'track' in json_response:
        track_dict_temp = json_response['track']
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
        return track_dict_temp
#    else:
#        raise ValueError('no track is retrieved')


def get_similar_song(artist, name, number_of_items,**kwarg):
    '''
    This function gets the song similar to the supplied one in a list.
    '''
    params = urllib.urlencode({'method' : 'track.getSimilar',
               'artist' : artist,
               'track' : name,
               'limit' : number_of_items,
               'api_key' : '2a59114aa8b3e871fe76e14d3380ad98',
               'format':'json'})
    json_response = connection (params)
    if 'similartracks' in json_response:
        if 'track' in json_response['similartracks']:
            similar_tracks = json_response['similartracks']['track']
            track_info_list = [];
            for track in similar_tracks:
                track_info_str = ';'.join([track['name'], track['artist']['name'], 
                                          str(track['match']),str(track['playcount'])])
                track_info_list.append(track_info_str)
        return track_info_list

def get_album(artist, album,**kwarg):
    '''
    This function gets the album info in a dictionary.
    '''
    params = urllib.urlencode({'method' : 'album.getInfo',
               'artist' : artist,
               'album' : album,
               'api_key' : '2a59114aa8b3e871fe76e14d3380ad98',
               'format':'json'})
    json_response = connection (params)
    if 'album' in json_response:
        album_dict_temp = json_response['album']
        album_dict_temp.pop('image')
        if 'wiki' in album_dict_temp:
            album_dict_temp.update(album_dict_temp.pop('wiki'))
        if 'tags' in album_dict_temp:
            tag_list = []
            for tag_dicts in album_dict_temp.pop('tags')['tag']:
                tag_list.append(tag_dicts['name'])
            album_dict_temp['tags'] = ";".join(tag_list)
        if 'tracks' in album_dict_temp:
            track_list = []
            for track_dicts in album_dict_temp.pop('tracks')['track']:
                track_list.append('-'.join([str(track_dicts['@attr']['rank']), track_dicts['name']]))
            album_dict_temp['tracks'] = ";".join(track_list)
        return album_dict_temp

def get_artist (artist, artist_mbid=None, **kwarg):
    '''
    This function gets the artist info in a dictionary.
    '''
    if artist_mbid != None:
        params = urllib.urlencode({'method' : 'artist.getInfo',
               'artist' : artist,
               'mbid': artist_mbid,
               'api_key' : '2a59114aa8b3e871fe76e14d3380ad98',
               'format':'json'})
    else:
            params = urllib.urlencode({'method' : 'artist.getInfo',
               'artist' : artist,
               'api_key' : '2a59114aa8b3e871fe76e14d3380ad98',
               'autocorrect':'1',
               'format':'json'})
    
    json_response = connection (params)
    if 'artist' in json_response:
        artist_dict_temp = json_response['artist']
        if 'bio' in artist_dict_temp:
            artist_dict_temp.update(artist_dict_temp.pop('bio'))
            artist_dict_temp.pop('links')
            if 'content' in artist_dict_temp:
                artist_dict_temp['bio'] = artist_dict_temp.pop('content')
                artist_dict_temp['bio_published'] = artist_dict_temp.pop('published')
        artist_dict_temp.pop('image')
        artist_dict_temp.update(artist_dict_temp.pop('stats'))
        if 'tags' in artist_dict_temp:
            tag_list = []
            for tag_dicts in artist_dict_temp.pop('tags')['tag']:
                tag_list.append(tag_dicts['name'])
            artist_dict_temp['tags'] = ";".join(tag_list)
        if 'similar' in artist_dict_temp:
            similar_list = []
            for artist_dicts in artist_dict_temp.pop('similar')['artist']:
                similar_list.append(artist_dicts['name'])
            artist_dict_temp['similar'] = ";".join(similar_list)
        birthday = get_birthday(artist_dict_temp['summary'])
        artist_dict_temp['birthday'] = birthday
        return artist_dict_temp





def get_birthday(text):
    year_text = re.search('\d\d\d\d', text)
    if year_text:
        tokens = re.split('(\W+)', text[0:(year_text.end())])
        text = ''.join(tokens[-5:]) #assuming the birthday will be the first to have these formats
        return text
#        try:
#            date = dateutil.parser.parse(text, fuzzy = False)
#            return date
#        except ValueError:
#            pass

                
                
artist = 'rihanna'
name = 'umbrella'
album = 'Good Girl Gone Bad'
number_of_items = '100'
artist_mbid = 'db36a76f-4cdf-43ac-8cd0-5e48092d2bae'
#a = get_song(artist,name)
#b = get_similar_song(artist, name, number_of_items)
#c = get_album(artist, album)
#d = get_artist (artist)
