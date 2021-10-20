import requests
from keys_tokens import auth
from easygui import *
import sqlite3
#import do_all
import random

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()

def unfollow(friend_id):
    url = 'https://api.twitter.com/1.1/friendships/destroy.json?'
    url += 'user_id='+ str(friend_id)
    try:
        response = requests.request("POST", url, auth=auth) #, headers=headers
    except:
        print('error unfollowing')

def keep_following(friend):
    msg = 'Keep following ' + friend[1] + ' ( ' + friend[2] + ' )?' + '\n' + '\n' + friend[3] + '\n' + '\n' + 'last tweet: ' + str(friend[4])
    title = 'Should keep following ' + str(friend[1]) + '?'
    return ynbox(msg, title, choices=("[<F1>]Keep Following", "[<F2>]Unfollow"))

def user_continue():
    msg = "Do you want to continue?"
    title = "Continue?"
    return ccbox(msg, title, choices=("Continue", "Stop"))

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