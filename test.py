import urllib.request
import urllib.parse
import json

key = 'AIzaSyCr6xs0NlPg2hIynXQJWY3o230n6iQyDl0'
cx = '017146964052550031681:wnjobi1fzcm'

if __name__ == '__main__':
    q = 'flex-direction'
    url = 'https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}'.format(key, cx, q)
    f = urllib.request.urlopen(url)
    s = f.read().decode('utf-8')
    j = json.loads(s)
    print(j['items'][0])
