import urllib.request as request
import json

"""
get_name: artist name is the english name for the artist
country_code has to obey with Spotify standards and currently not implemented
, i.e. using the default value
"""

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


def get_artist_data(artist_name, country_code):

    ## prepare to get the URL
    name_query = '+'.join(artist_name.split(' '))
    url = 'https://api.spotify.com/v1/search?q=' + name_query + '&type=artist&market=' + country_code
    try:
        result = request.urlopen(url)
    except:
        raise Exception('fetching artist name failed. check your internet connection')

    result = json.loads(result.read().decode(result.info().get_param('charset') or 'utf-8'))

    return result

def get_artist_properties(artist_name, keys, country_code = 'US'):

    data = get_artist_data(artist_name, country_code)

    ret = {}

    for key in keys:
        ret[key] = find_key_in_json(data, key)

    return ret


print(get_artist_properties('jay chou', ['name', 'id', 'popularity']))
