import requests
from keys_tokens import auth
from easygui import *
import sqlite3
import do_all
import random

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

def randomly(seq):
    shuffled = [x for x in seq]
    #shuffled = seq
    random.shuffle(shuffled)
    return iter(shuffled)

def add_to_list(list_id, member_id):
    url = 'https://api.twitter.com/1.1/lists/members/create.json?'
    url += 'list_id='+ str(list_id) +'&'
    url += 'user_id='+ str(member_id)
    headers = {
    'Cookie': 'guest_id=v1%3A160805601485553252; personalization_id="v1_avHrOzKaJeJMXf77gpv/ig=="; lang=en'
    }
    try:
        response = requests.request("POST", url, headers=headers, auth=auth)
    except:
        print('error adding to list')

def ask_user(lists_list, member, users_left):
    # message to be displayed
    text = member[1] + ' ( ' + member[2] + ' )' + '\n' + member[3]
    # window title
    title = 'total users remaining: ' + str(users_left)
    # item choices
    choices = lists_list
    # creating a multi choice box
    return multchoicebox(text, title, choices, preselect=None)

def user_continue():
    msg = "Do you want to continue?"
    title = "Continue?"
    return ccbox(msg, title)

# get list of lists (name + id)
cur.execute('SELECT * from lists ORDER BY list_name')
lists_list = cur.fetchall()
lists = [item[1] for item in lists_list]
lst_dic = dict([(y,x) for (x,y,z) in lists_list])

# get list of friends without lists (name + id)
query = 'SELECT * from friends where '
for list in lists_list[:-2]:
    query += 'user_id not in (select user_id from ' + list[1] + ') AND '
query += 'user_id not in (select user_id from ' + lists_list[-1][1] + ')'
cur.execute(query)
friends_no_list = cur.fetchall()

should_continue = True
counter = 1
while should_continue:
    for i in randomly(range(len(friends_no_list))):
        if counter % 20 == 0:
            should_continue = user_continue()
            if not should_continue:
                break
        counter += 1
        selection = ask_user(lists, friends_no_list[i], len(friends_no_list)-counter)
        if selection != None:
            for lst in selection:
                add_to_list(lst_dic[lst], friends_no_list[i][0])

print('end')