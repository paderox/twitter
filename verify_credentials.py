import requests
from requests_oauthlib import OAuth1
from keys_tokens import consumer_key, consumer_secret, access_token, token_secret, bearer_token

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, token_secret)

test = requests.get(url, auth=auth)

print(test)
print('end')