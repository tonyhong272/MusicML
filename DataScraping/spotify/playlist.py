import urllib.request
import urllib.parse
import json

def find_key_in_json(data, key):

    if isinstance(data, dict):
        for _k in data:
            if _k == key:
                return data[key]
            else:
                ret = find_key_in_json(data[_k], key)
                if ret:
                    return ret
        return None

    elif isinstance(data, list):
        for _k in data:
            ret = find_key_in_json(_k, key)
            if ret:
                return ret


    return None


def get_popular_playlists(headers, limit=2,
                          offset=0, country='US', timestamp='2014-10-23T09:00:00'):

    timestamp = timestamp.encode('utf-8')

    query = {'country' : country, 'timestamp' : timestamp, 'offset' : offset, 'limit' : limit}

    url = 'https://api.spotify.com/v1/browse/featured-playlists?' + urllib.parse.urlencode(query)

    try:
        req = urllib.request.Request(url, None, headers)
        with urllib.request.urlopen(req) as response:
            result = response.read()
    except:
        raise Exception('fetching artist name failed. check your internet connection')

    result = json.loads(result.decode('utf-8'))

    return result


def get_tracks(playlist):

    assert isinstance(playlist, dict), 'playlist is not an appropriate type of json'

    tracks = find_key_in_json(playlist, 'tracks')

    return find_key_in_json(tracks, 'href')


def get_tracks_from_popular_playlists(headers, playlist_limit=2, playlist_offset=0,
                                      country='US', timestamp='2014-10-23T09:00:00'):

    playlists = get_popular_playlists(headers, playlist_limit, playlist_offset, country, timestamp)

    playlists = find_key_in_json(playlists, 'playlists')

    playlists = find_key_in_json(playlists, 'items')

    assert isinstance(playlists, list), 'playlists are not properly formated as lists'

    all_playlists = []

    for playlist in playlists:

        playlist_name = playlist['name']
        playlist_id = playlist['id']
        playlist_owner = playlist['owner']
        playlist_url = playlist['href']
        owner_id = playlist_owner['id']
        owner_uri = playlist_owner['uri']

        all_tracks = []

        url = get_tracks(playlist)

        try:
            req = urllib.request.Request(url, None, headers)
            with urllib.request.urlopen(req) as response:
                result = response.read()
        except:
            raise Exception('fetching artist name failed. check your internet connection')

        tracks = json.loads(result.decode('utf-8'))

        tracks = find_key_in_json(tracks, 'items')

        assert isinstance(tracks, list), 'tracks are not properly formated as lists'

        for each in tracks:
            track = find_key_in_json(each, 'track')
            artists = find_key_in_json(track, 'artists')
            names = []
            for artist in artists:
                names.append(artist['name'])
            track_name = track['name']
            popularity = track['popularity']
            album = track['album']
            album_name = album['name']
            album_url = album['external_urls']['spotify']
            album_uri = album['uri']
            track_url = track['external_urls']['spotify']
            track_uri = track['uri']

            all_tracks.append({'artists': names,
                               'track_name': track_name,
                               'album_name': album_name,
                               'popularity': popularity,
                               'track_url': track_url,
                               'track_uri': track_uri,
                               'album_url': album_url,
                               'album_uri': album_uri})

        ret_data = {'playlist_name' : playlist_name, 'playlist_id' : playlist_id,
                    'owner_id' : owner_id, 'owner_uri' : owner_uri,
                    'playlist_url': playlist_url,
                    'tracks_data' : all_tracks.copy()}
        all_playlists.append(ret_data.copy())


    return all_playlists



