import requests
import json
from keys_tokens import auth
from friends_listfier import add_to_list
import sqlite3

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

donor_list = 'nflcomnflnetwork'
receiver_list = 'nfl'
cur.execute('SELECT list_id FROM lists WHERE list_name = \'' + receiver_list + '\'')
receiver_list_id = str(cur.fetchone()[0])

cur.execute('SELECT * from {0} where user_id not in (select user_id from {1})'.format(donor_list, receiver_list))
donor_members = cur.fetchall()

for member in donor_members:
    member_id = str(member[1])
    member_handle = member[2]
    add_to_list(receiver_list_id, member_id)

print("members transferred")
