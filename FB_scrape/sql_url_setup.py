"""
Connect to sql server, send data to postgres, create url and get data from api.
"""
import requests
import json
from sqlalchemy import create_engine
import time
import smtplib
import datetime
from config import email


def send_to_postgres(df, table):
	"""
	Send data frame to the postgres server.

	INPUT:
		df = pandas data frame that has the data for each page
	OUTPUT:
		None
	"""
	try:
		# just to see where we are at as it runs
		print('last date uploaded', df['created_time'][len(df) - 1])
	except:
		pass

	engine = create_engine('postgresql://mjaron@localhost:5432/facebook')
	df.to_sql(table, engine, if_exists='append', index=False)


def url_creator(auth, fields, page_id):
	"""
	Take in arguments and returns the search url needed.

	INPUT:
		auth = string authentication key
		fields = string of fields to search on
		page_id = string id of page to look at
	OUTPUT:
		main_url = string with complete combined url
	"""
	base_url = "https://graph.facebook.com/v2.8/"
	access = "&access_token=" + auth
	fields = "?fields=" + fields

	main_url = base_url + page_id + fields + access

	return main_url


def graph_api(url):
	"""
	Take in complete URL, calls the api and returns the page.

	INPUT:
		url = string of complete url to look for

	OUTPUT:
		page = json formatted string
	"""
	count = 0
	retry = True
	while retry:
		count += 1
		try:
			page = requests.get(url)
			page = json.loads(page.text)
			retry = False
			# check if auth has expired
			try:
				if page['error']['type'] == 'OAuthException':
					print(page)
					print('Auth expired, get new short term auth, to create long term one')
					error = page['error']['type']
					email_notify(email, error, page)
				elif page['error']['code'] == 1:
					print(page)
					print('the limits are set to high, may need to reduce')
			except:
				pass
		except:
			print('failed request, attempt %s, trying again' % count)
			
			# if it doesn't work, wait a 1 minute, try again, increasing wait time
			time.sleep(60 * count)
			# will retry up to 5 times
			if count >= 5:
				retry = False

	return page


def email_notify(email, error, page):
	"""
	Send an email if something goes wrong.
	"""
	time_error = str(datetime.datetime.now())
	msg = """The facebook api code to gather data error from the walmart
	page had an error at %s \n 
	The error is: 
	%s \n
	Most likely need to get a new long term token. To do that
	follow the instructions in the readme \n
	The page returned is as follows: \n
	%s""" % (time_error, error, page)
	
	# dummy account I created, gmail would not work
	username = 'columbiauniversity@yahoo.com'
	password = 'colum12345'

	server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
	server.starttls()
	server.login(username, password)
	server.sendmail(username, email, msg)
	server.quit()
