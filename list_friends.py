import requests
import json
from keys_tokens import auth
import sqlite3
from datetime import datetime

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

cursor = '-1'
while cursor != '0':
    url = 'https://api.twitter.com/1.1/friends/list.json?'
    url += 'screen_name=paderox&'
    url += 'cursor='+cursor+'&'
    url += 'count=200&'
    url += 'skip_status=false&'
    url += 'include_user_entities=false'
    headers = {
    'Cookie': 'guest_id=v1%3A160805601485553252;personalization_id="v1_avHrOzKaJeJMXf77gpv/ig=="; lang=en'
    }
    response = requests.request("GET", url, headers=headers, auth=auth)
    data = json.loads(response.text)

    try:
        cursor = data['next_cursor_str']
    except:
        print(data['errors'][0]['message'])
        break

    for user in data['users']:
        name = user['name']
        handle = user['screen_name']
        description = user['description']
        user_id = user['id']
        try:
            last_tweet = datetime.strptime(user['status']['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
        except:
            last_tweet = None

        cur.execute('INSERT OR REPLACE INTO friends (user_id, name, handle, description, last_tweet) VALUES ( ?, ?, ?, ?, ? )', (user_id, name, handle, description, last_tweet) )

    conn.commit()

conn.close()

print('friends listed')