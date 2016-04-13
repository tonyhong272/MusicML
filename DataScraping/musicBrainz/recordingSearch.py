#!/usr/bin/env python
"""A simple script that searches for a release in the MusicBrainz
database and prints out a few details about the first 5 matching release.

    $ ./recordingSearch.py "the beatles" revolver
    Revolver, by The Beatles
    Released 1966-08-08 (Official)
    MusicBrainz ID: b4b04cbf-118a-3944-9545-38a0a88ff1a2
"""
import musicbrainzngs
import sys

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

musicbrainzngs.set_hostname("localhost:5000")


def fetch_recording(artist, title, **kwarg):
    """fetch recording from musicBrainz
    """
    result = musicbrainzngs.search_recordings(query='', limit=5, offset=None, strict=False, artist = artist, release = title)
    recording = {};
    for i in range(0,5):
        if (not 'disambiguation' in result['recording-list'][i]) or \
        (result['recording-list'][i]['disambiguation'] != 'music video'):
            if 'length' in result['recording-list'][0]:
                recording['recording_length'] = result['recording-list'][0]['length']
            else:
                recording['recording_length'] = -1
            recording['recording_mbid'] = result['recording-list'][0]['id']
            recording['artist_mbid'] = result['recording-list'][0]['artist-credit'][0]['artist']['id']
            recording['release_date'] = result['recording-list'][0]['release-list'][0]['date']
            recording['release_mbid'] = result['recording-list'][0]['release-list'][0]['id']
            return recording

def fetch_artist(artist_mbid, **kwarg):
    """fetch artist info from musicBrainz
    """
    result = musicbrainzngs.search_artists(query='', limit=1, offset=None, strict=False, arid = artist_mbid)
    artist_info = {};
    if 'artist-list' in result:
        artist_info['artist_type'] = result['artist-list'][0]['type']
        if 'gender' in result['artist-list'][0]:
            artist_info['artist_gender'] = result['artist-list'][0]['gender']
        else:
            artist_info['artist_gender'] = ''
        if 'begin-area' in result['artist-list'][0]:
            artist_info['artist_begin_area'] = result['artist-list'][0]['begin-area']['name']
        else:
            artist_info['artist_begin_area-area'] = ''
        if 'country' in result['artist-list'][0]:
            artist_info['artist_country'] = result['artist-list'][0]['country']
        else:
            artist_info['artist_country'] = ''
        if 'life-span' in result['artist-list'][0]:
            artist_info['artist_begin_date'] = result['artist-list'][0]['life-span']['begin']
        else:
            artist_info['artist_begin_date-date'] = ''
        if 'tag-list' in result['artist-list'][0]:
            tag_list = result['artist-list'][0]['tag-list']
            artist_info['artist_tags'] = ';'.join([tag['name'] for tag in tag_list])
        else:
            artist_info['artist_tags'] = ''
    return artist_info

if __name__ == '__main__':
    args = ['Rihanna', 'Work']
    print(args)
    if len(args) != 2:
        sys.exit("usage: {} ARTIST ALBUM".format(sys.argv[0]))
    artist, title = args

    recording = fetch_recording(artist, title)
    artist = fetch_artist(recording['artist_mbid'])
    print recording, artist 


