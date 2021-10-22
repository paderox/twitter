import requests
import json
from functions import add_to_list, ask_list
import sqlite3

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

# get list of lists (name + id)
cur.execute('SELECT * from lists ORDER BY list_name')
lists_list = cur.fetchall()
lst_dic = dict([(y,x) for (x,y,z) in lists_list])

donor_list = ask_list(list(lst_dic.keys()), 'donor')[0]
receiver_list = ask_list(list(lst_dic.keys()), 'receiver')[0]

cur.execute('SELECT list_id FROM lists WHERE list_name = \'' + receiver_list + '\'')
receiver_list_id = str(cur.fetchone()[0])

cur.execute('SELECT * from {0} where user_id not in (select user_id from {1})'.format(donor_list, receiver_list))
donor_members = cur.fetchall()

for member in donor_members:
    member_id = str(member[1])
    member_handle = member[2]
    add_to_list(receiver_list_id, member_id)

print("members transferred")
