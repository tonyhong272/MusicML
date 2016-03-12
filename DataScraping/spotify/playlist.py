import urllib.request
import urllib.parse
import json
import base64

# currently useless
client_id = '2da9e3d6414047ccb45cda8a9b359f59'
client_secret = 'fe5f334a1cf24ad897944dff46b8a3e6'

"""
get_name: artist name is the english name for the artist
country_code has to obey with Spotify standards and currently not implemented
, i.e. using the default value
"""

"""
return OAuth token and expiration time in seconds.
"""

def get_code():

    query = {'client_id': client_id, 'response_type': 'code', 'redirect_uri': 'http://google.com'}
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query)
    code_headers = {'Accept' : 'application/json'}

    try:
        req = urllib.request.Request(url, None, code_headers)
        with urllib.request.urlopen(req) as response:
            result = response.read()
    except:
        raise Exception('fetching artist name failed. check your internet connection')

    result = json.loads(result.decode('utf-8'))

    return result


def get_token():

    url = 'https://accounts.spotify.com/api/token'
    data = {'grant_type':'client_credentials'}
    data = urllib.parse.urlencode(data)
    login = client_id + ':' + client_secret
    encoded_login = base64.b64encode(login.encode('ascii'))
    encoded_login = encoded_login.decode('utf-8')
    ##
    headers = {'Authorization': 'Basic ' + encoded_login}
    try:
        req = urllib.request.Request(url, data.encode('ascii'), headers)
        with urllib.request.urlopen(req) as response:
            result = response.read()
    except:
        raise Exception('fetching artist name failed. check your internet connection')    ## to be fixed or ask Spotify Customer Service to fix. Can not find solution (400 Bad Request)

    result = json.loads(result.decode('utf-8'))
    return result['access_token']

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


def get_popular_playlists(limit=2, offset=0, country='US', timestamp='2014-10-23T09:00:00'):

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

def get_tracks_from_popular_playlists(playlist_limit=2, playlist_offset=0, country='US', timestamp='2014-10-23T09:00:00'):

    playlists = get_popular_playlists(playlist_limit, playlist_offset, country, timestamp)

    playlists = find_key_in_json(playlists, 'playlists')

    playlists = find_key_in_json(playlists, 'items')


    assert isinstance(playlists, list), 'playlists are not properly formated as lists'

    all_tracks = []

    for playlist in playlists:

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

            all_tracks.append({'artists': names, 'track_name': track_name, 'album_name': album_name, 'popularity': popularity})

    return all_tracks


OAuthCode = get_token()

headers = { 'Authorization' : 'Bearer ' + OAuthCode, 'Accept' : 'application/json'}

print('Access Token Obtained:', OAuthCode)

print(get_tracks_from_popular_playlists())


