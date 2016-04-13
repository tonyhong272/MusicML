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
import difflib

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

musicbrainzngs.set_hostname("localhost:5000")

def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()

def fetch_recording(artist, title, **kwarg):
    """fetch recording from musicBrainz
    """
    result = musicbrainzngs.search_recordings(query='', limit=10, offset=None, strict=False, artist = artist, release = title)
    seq2 =' '.join([title, artist])
    high_score = 0
    idx = 0
    for i in range(0,10):
        seq1 = ' '.join([result['recording-list'][i]['title'], result['recording-list'][i]['artist-credit-phrase']])
        similarity_score = similar(seq1,seq2)
        if similarity_score > high_score and 'instrumental' not in seq1 and (not 'disambiguation' in result['recording-list'][i] or \
        (result['recording-list'][i]['disambiguation'] != 'music video')):
            high_score = similarity_score
            idx = i
            '''print similarity_score
            print seq1
            print seq2'''
    #print idx
    recording = {}
    recording['match_score'] = high_score
    if 'length' in result['recording-list'][idx]:
        recording['recording_length'] = result['recording-list'][idx]['length']
    else:
        recording['recording_length'] = -1
    recording['recording_mbid'] = result['recording-list'][idx]['id']
    recording['artist_mbid'] = result['recording-list'][idx]['artist-credit'][0]['artist']['id']
    recording['release_date'] = result['recording-list'][idx]['release-list'][0]['date']
    recording['release_mbid'] = result['recording-list'][idx]['release-list'][0]['id']
    if 'artist-credit-phrase' in result['recording-list'][idx]:
        recording['mb_artist'] = result['recording-list'][idx]['artist-credit-phrase']
    else:
        recording['mb_artist'] = ''
    recording['mb_title'] = result['recording-list'][idx]['title']
    #print result['recording-list']
    return recording

def fetch_artist(artist_mbid, **kwarg):
    """fetch artist info from musicBrainz
    """
    result = musicbrainzngs.search_artists(query='', limit=1, offset=None, strict=False, arid = artist_mbid)
    artist_info = {};
    if 'artist-list' in result:
        if 'type' in result['artist-list'][0]:
            artist_info['artist_type'] = result['artist-list'][0]['type']
        else:
            artist_info['artist_type'] = ''
        if 'gender' in result['artist-list'][0]:
            artist_info['artist_gender'] = result['artist-list'][0]['gender']
        else:
            artist_info['artist_gender'] = ''
        if 'begin-area' in result['artist-list'][0]:
            artist_info['artist_begin_area'] = result['artist-list'][0]['begin-area']['name']
        else:
            artist_info['artist_begin_area'] = ''
        if 'country' in result['artist-list'][0]:
            artist_info['artist_country'] = result['artist-list'][0]['country']
        else:
            artist_info['artist_country'] = ''
        if 'life-span' in result['artist-list'][0] and 'begin' in result['artist-list'][0]['life-span']:
            artist_info['artist_begin_date'] = result['artist-list'][0]['life-span']['begin']
        else:
            artist_info['artist_begin_date'] = ''
        if 'tag-list' in result['artist-list'][0]:
            tag_list = result['artist-list'][0]['tag-list']
            artist_info['artist_tags'] = ';'.join([tag['name'] for tag in tag_list])
        else:
            artist_info['artist_tags'] = ''
    return artist_info

if __name__ == '__main__':
    args = ['Rihanna', 'umbrella']
    print(args)
    if len(args) != 2:
        sys.exit("usage: {} ARTIST ALBUM".format(sys.argv[0]))
    artist, title = args

    recording = fetch_recording(artist, title)
    artist = fetch_artist(recording['artist_mbid'])
    print recording, artist


