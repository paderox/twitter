import requests
import json
from keys_tokens import auth, main_account
import sqlite3
from datetime import datetime

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS "friends" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"handle"	TEXT,
	"description"	TEXT,
	"last_tweet"	TEXT,
	PRIMARY KEY("user_id")
)
''')
conn.commit()

cur.execute('DELETE from friends')
conn.commit()

cursor = '-1'
while cursor != '0':
    url = 'https://api.twitter.com/1.1/friends/list.json?'
    url += 'screen_name='+ main_account +'&'
    url += 'cursor='+cursor+'&'
    url += 'count=200&'
    url += 'skip_status=false&'
    url += 'include_user_entities=false'
    response = requests.request("GET", url, auth=auth)
    data = json.loads(response.text)

    try:
        cursor = data['next_cursor_str']
    except:
        print(data['errors'][0]['message'])
        conn.commit()
        conn.close()
        exit()

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