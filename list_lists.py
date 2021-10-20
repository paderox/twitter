import requests
import json
from keys_tokens import auth
import sqlite3

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

url = "https://api.twitter.com/1.1/lists/list.json?screen_name=paderox"

headers = {
'Cookie': 'guest_id=v1%3A160805601485553252;personalization_id="v1_avHrOzKaJeJMXf77gpv/ig=="; lang=en'
}
response = requests.request("GET", url, headers=headers, auth=auth)
lists = json.loads(response.text)

for list in lists:
    if list['user']['screen_name'] == 'paderox': #or list['user']['screen_name'] == 'ChrisWesseling':
        list_id = list['id']
        list_name = list['name'].lower().strip().replace(' ','').replace('-','').replace('.','').replace('/','')
        list_slug = list['slug']

        cur.execute('INSERT OR REPLACE INTO lists (list_id, list_name, list_slug) VALUES ( ?, ?, ? )', (list_id, list_name, list_slug) )

        cur.execute('CREATE TABLE IF NOT EXISTS ' + list_name + '( "member_name" TEXT NOT NULL, "user_id" INTEGER NOT NULL UNIQUE, "handle" TEXT NOT NULL, PRIMARY KEY("user_id") )')

conn.commit()

conn.close()

print('lists listed')