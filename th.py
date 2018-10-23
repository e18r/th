#! /usr/bin/env python

from twython import Twython, TwythonStreamer
from pymongo import MongoClient
import re

APP_KEY = '6NvNomgUFfICMCWVMSclz7DpR'
APP_SECRET = 'jNYnBRfDe73lSRnZzbqrrZTsZETcgjNtgrDdvuq9Ufx2wQtnWs'
OAUTH_TOKEN = '326997205-opAgyYEVk6OZhtoGZ8DYDhxJ67vpqzoSp9DxWplM'
OAUTH_TOKEN_SECRET = 'mwFUPc318RXOWgtuf4Ccvk2bjs8KFKG2FwerODXCPWWzt'

APP_KEY = '0tyaCY5ZOIUhQkFhdI1Q0zkpV'
APP_SECRET = 'tWwxTQJdT77kms0ZLZwLtexLb4qDB94RhShoorrBRZ837yYThi'
OAUTH_TOKEN = '326997205-QFJfjn5qL3yP7xXmw6Ue5GUmCIv66Is1CzHsPa8R'
OAUTH_TOKEN_SECRET = 'OEk0UDetnzE5KWXxWWhv41sPrp2BHus6SUvb7hX3YpfVD'


class Th(TwythonStreamer):
    def on_success(self, data):
        if not ('user' in data and 'id' in data['user']):
            return
        if data['user']['id'] not in ids:
            return
        tweet_collection.insert_one(data)
        date = ''
        if 'created_at' in data:
            date = data['created_at']
        screen_name = ''
        url = 'https://twitter.com/'
        if 'screen_name' in data['user']:
            screen_name = data['user']['screen_name']
            url += screen_name
        actual_tweet = data
        rt = ''
        if 'retweeted_status' in data:
            actual_tweet = data['retweeted_status']
            rt = ' RT {}'.format(actual_tweet['user']['screen_name'])
        if 'text' in actual_tweet:
            text = actual_tweet['text']
            if actual_tweet['truncated']:
                text = actual_tweet['extended_tweet']['full_text']
        text = re.sub(r'\s', ' ', text)
        if 'id_str' in data:
            url += '/status/' + data['id_str']
        print('\n{} - {}{}: {} {}'.format(date, screen_name, rt, text, url))

    def on_error(self, status_code, data):
        print()
        print(status_code)
        print(data)
        self.disconnect()

def get_ids(screen_names):
    ids = []
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    for screen_name in screen_names:
        data = twitter.show_user(screen_name=screen_name)
        id = data['id']
        ids.append(id)
    return ids

def follow(ids):
    stream = Th(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(follow=ids)

def get_screen_names():
    screen_names = []
    user_collection = db.users
    user_cursor = user_collection.find({})
    for user_object in user_cursor:
        screen_name = user_object['screen_name']
        screen_names.append(screen_name)
    return screen_names

client = MongoClient()
db = client.twitter
tweet_collection = db.tweets
screen_names = get_screen_names()
print(screen_names)
ids = get_ids(screen_names)
print(ids)
while True:
    try:
        follow(ids)
    except Exception as e:
        print(e)
