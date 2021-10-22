# import do_all
import sqlite3
from functions import unfollow, keep_following, user_continue

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

# get list of friends ordered by last_tweet
cur.execute('SELECT * from friends order by last_tweet')
friends = cur.fetchall()

should_continue = True
counter = 1
while should_continue:
    for friend in friends:
        if counter % 5 == 0:
            should_continue = user_continue()
            if not should_continue:
                break
        selection = keep_following(friend)
        if selection == False:
            unfollow(friend[0])
        counter += 1

print('end')