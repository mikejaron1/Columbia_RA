'''
Author: Michael Jaron
Data: 2/6/17

Program based on info from:
https://developers.facebook.com/docs/facebook-login/access-tokens/expiration-and-extension
'''

import requests
import json


def long_term_token(short_term_auth):
	"""
	Create url and get long lived access token.
	"""
	# main app ids
	app_secret = 'f528ab12b56bbb7553d7f7e465718e6b'
	app_id = '447274108937606'
	
	base_url = "https://graph.facebook.com/v2.8/"
	a = 'oauth/access_token?'
	b = 'client_id=%s&' % app_id
	c = 'client_secret=%s&' % app_secret
	d = 'grant_type=fb_exchange_token&'
	e = 'fb_exchange_token=%s' % short_term_auth
	url = base_url + a + b + c + d + e

	page = requests.get(url)
	page = json.loads(page.text)

	long_term_access_token = page['access_token']

	# write to file
	auth_file = open('./auth_info.txt', 'w')
	auth_file.write(long_term_access_token)

	return long_term_access_token


def main():
	"""
	Create url and get long lived access token.
	"""	
	# read in short term auth
	f = open('./input.txt', 'r')
	short_term_auth = f.read()

	long_term_access_token = long_term_token(short_term_auth)
	print(long_term_access_token)
	print('run program like normal now')

if __name__ == '__main__':
	main()



