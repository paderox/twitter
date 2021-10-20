import requests
import json
from keys_tokens import auth
import sqlite3

conn = sqlite3.connect("twitter.sqlite")
cur = conn.cursor()

cur.execute("SELECT * from lists")
lists = cur.fetchall()

for list in lists:
    list_id = str(list[0])
    list_name = list[1].lower().strip().replace(' ','').replace('-','').replace('.','').replace('/','')
    cursor = "-1"
    while cursor != '0':
        url = "https://api.twitter.com/1.1/lists/members.json?"
        url += "list_id=" + list_id + "&"
        url += "count=200&"
        url += "cursor=" + cursor + "&"
        url += "include_entities=false&"
        url += "skip_status=true"
        headers = {
        'Cookie': 'guest_id=v1%3A160805601485553252;personalization_id="v1_avHrOzKaJeJMXf77gpv/ig=="; lang=en'
        }
        response = requests.request("GET", url, headers=headers, auth=auth)
        data = json.loads(response.text)

        try:
            cursor = data["next_cursor_str"]
        except:
            print(data["errors"][0]["message"])
            break
        for user in data["users"]:
            member_name = user["name"]
            handle = user["screen_name"]
            user_id = user["id"]
            cur.execute(
                'INSERT OR REPLACE INTO ' + list_name + '(member_name, user_id, handle) VALUES ( ?, ?, ? )',
                (member_name, user_id, handle),
            )
        conn.commit()
conn.close()

print("members listed")