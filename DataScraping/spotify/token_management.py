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
    return result['access_token'], result['expires_in']

def init_token():

    OAuthCode, expire_sec = get_token()
    headers = {}
    headers['Authorization'] = 'Bearer ' + OAuthCode
    headers['Accept'] = 'application/json'

    print('Access Token Obtained:', OAuthCode)

    return headers.copy(), expire_sec