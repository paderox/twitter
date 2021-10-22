from keys_tokens import auth
import requests
from easygui import *
import random

def unfollow(friend_id):
    url = 'https://api.twitter.com/1.1/friendships/destroy.json?'
    url += 'user_id='+ str(friend_id)
    try:
        response = requests.request("POST", url, auth=auth)
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

def randomly(seq):
    shuffled = [x for x in seq]
    #shuffled = seq
    random.shuffle(shuffled)
    return iter(shuffled)

def add_to_list(list_id, member_id):
    url = 'https://api.twitter.com/1.1/lists/members/create.json?'
    url += 'list_id='+ str(list_id) +'&'
    url += 'user_id='+ str(member_id)
    try:
        response = requests.request("POST", url, auth=auth)
    except:
        print('error adding to list')

def ask_user(lists_list, member, users_left):
    msg = member[1] + ' ( ' + member[2] + ' )' + '\n' + member[3]
    title = 'total users remaining: ' + str(users_left)
    choices = lists_list
    return multchoicebox(msg, title, choices, preselect=None)

def user_continue():
    msg = "Do you want to continue?"
    title = "Continue?"
    return ccbox(msg, title, choices=("Continue", "Stop"))

def ask_list(lists, side):
    msg = 'select ' + side + ' list'
    title = 'select ' + side + ' list'
    choices = lists
    return multchoicebox(msg, title, choices, preselect=None)
