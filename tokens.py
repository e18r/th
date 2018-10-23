#! /usr/bin/env python

from twython import Twython
import sys

if len(sys.argv) == 3:
    APP_KEY = sys.argv[1]
    APP_SECRET = sys.argv[2]
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    print('APP_KEY: ' + APP_KEY)
    print('APP_SECRET: ' + APP_SECRET)
    print('oauth_token: ' + auth['oauth_token'])
    print('oauth_token_secret: ' + auth['oauth_token_secret'])
    print('auth_url: ' + auth['auth_url'])


elif len(sys.argv) == 6:
    APP_KEY = sys.argv[1]
    APP_SECRET = sys.argv[2]
    oauth_token = sys.argv[3]
    oauth_token_secret = sys.argv[4]
    oauth_verifier = sys.argv[5]
    twitter = Twython(APP_KEY, APP_SECRET, oauth_token, oauth_token_secret)
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    data = twitter.show_user(screen_name='silvaEmil')
    print("APP_KEY = '" + APP_KEY + "'")
    print("APP_SECRET = '" + APP_SECRET + "'")
    print("OAUTH_TOKEN = '" + OAUTH_TOKEN + "'")
    print("OAUTH_TOKEN_SECRET = '" + OAUTH_TOKEN_SECRET + "'")
