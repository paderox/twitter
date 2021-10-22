# import do_all
import requests
import sqlite3
from functions import unfollow, randomly, add_to_list, ask_user, user_continue

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

# get list of lists (name + id)
cur.execute('SELECT * from lists ORDER BY list_name')
lists_list = cur.fetchall()
lists = [item[1] for item in lists_list]
lists.append('Unfollow')
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
        if selection == ['Unfollow']:
                unfollow(friends_no_list[i][0])
        elif selection != None:
            for lst in selection:
                if lst != 'Unfollow':
                    add_to_list(lst_dic[lst], friends_no_list[i][0])

print('no more unlisted friends')