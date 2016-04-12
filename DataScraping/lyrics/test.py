# test.py
# Johnny Dai 4/11/2016
# Test version script to scraping www.lyrics.com to grab lyrics of target song
# Ex:
# To grab lyrics of 'This Love'
# print find_lyrics(this love)

import urllib
from bs4 import BeautifulSoup

#Function is to get rid of <br> in html content
def text_with_newlines(elem):
    text = ''
    for e in elem.recursiveChildGenerator():
        if isinstance(e, basestring):
            text += e.strip()
        elif e.name == 'br':
            text += '\n'
    return text

#Function to get url of lyrics website of target song
def find_lyrics_url(song):
    serviceurl = 'http://www.lyrics.com/search.php?'
    url =  serviceurl + urllib.urlencode({'keyword':song,'what':'all'})
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    txt = soup.find("a", {"class": "lyrics_preview"})
    return txt.get('href')

#Main function
def find_lyrics(title, artist):
    url =  'http://www.lyrics.com/' + find_lyrics_url(title + ' ' + artist)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    txt = soup.find("div", {"class": "SCREENONLY"})
    lyrics = text_with_newlines(txt)
    return lyrics

#Ex:
#print find_lyrics('bubbly')
print find_lyrics( title = 'this love', artist = 'maroon 5')
#print find_lyrics('back at one')



#MISC, no use
#http://www.lyrics.com/search.php?keyword=fallin+for+you+lyrics&what=all
#url = "http://www.lyrics.com/search.php?"keyword=fallin+for+you+lyrics&what=all
