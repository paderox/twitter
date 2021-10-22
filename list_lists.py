import requests
import json
from keys_tokens import auth, main_account
import sqlite3

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS "lists" (
	"list_id"	INTEGER NOT NULL UNIQUE,
	"list_name"	TEXT NOT NULL,
	"list_slug"	TEXT,
	PRIMARY KEY("list_id")
)
''')
conn.commit()

cur.execute('DELETE from lists')
conn.commit()

url = 'https://api.twitter.com/1.1/lists/list.json?screen_name=' + main_account
response = requests.request("GET", url, auth=auth)
lists = json.loads(response.text)

for list in lists:
    if list['user']['screen_name'] == main_account:
        list_id = list['id']
        list_name = list['name'].lower().strip().replace(' ','').replace('-','').replace('.','').replace('/','')
        list_slug = list['slug']

        cur.execute('INSERT OR REPLACE INTO lists (list_id, list_name, list_slug) VALUES ( ?, ?, ? )', (list_id, list_name, list_slug) )

        cur.execute('CREATE TABLE IF NOT EXISTS ' + list_name + '( "member_name" TEXT NOT NULL, "user_id" INTEGER NOT NULL UNIQUE, "handle" TEXT NOT NULL, PRIMARY KEY("user_id") )')

conn.commit()

conn.close()

print('lists listed')