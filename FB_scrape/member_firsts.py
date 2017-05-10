"""
Get member info.

Author: Michael Jaron
Date: 2/19/17
"""
import pandas as pd 
import psycopg2 
from sqlalchemy import create_engine

from sql_url_setup import send_to_postgres, url_creator, graph_api
from config import page_id, auth


def create_table():
	"""
	Create table and get connection and curser.

	INPUT:
		None
	OUTPUT:
		None
	"""
	con = psycopg2.connect(database='facebook')
	cur = con.cursor() 
	cur.execute('DROP TABLE IF EXISTS users')
	cur.execute("""CREATE TABLE users (
	            user_id BIGINT,
	            user_name TEXT,
	            -- joined TIMESTAMP,
	            first_comment TIMESTAMP
	            );""")
	con.commit()


def get_all_members():
	"""
	Use the API to find all members of the group.
	"""
	pagination = True

	fields = 'members.limit(1500)'
	url = url_creator(auth, fields, page_id)
	page = graph_api(url)
	
	page_posts = page["members"]["data"]

	member_parse_send(page_posts)

	# extract next page
	try:
		next_page = page["members"]["paging"]["next"]
	except:
		pagination = False

	while pagination:
		print("starting feed pagination")
		page = graph_api(next_page)
		try:
			next_page = page["paging"]["next"]
		except:
			pagination = False

		page_posts = page["data"]

		member_parse_send(page_posts)


def member_parse_send(page_posts):
	"""
	Collect user id, names, and first comment then send to postgres.
	"""
	user_names = []
	user_ids = []
	for user in page_posts:
		user_ids.append(user['id'])
		user_names.append(user['name'])

	df = pd.DataFrame()
	df['user_id'] = user_ids
	df['user_name'] = user_names

	print(len(df))
	df = first_comment(df)
	# send all data from current page to postgres
	send_to_postgres(df, table='users')


def first_comment(df):
	"""
	Find when a user makes their first comment on the page.
	"""
	engine = create_engine('postgresql://mjaron@localhost:5432/facebook')
	first_comment = []
	for id_ in df['user_id']:
		temp_df = pd.read_sql("""SELECT min(created_time) FROM feed 
								WHERE user_id = %s """ % id_, engine)
		first_comment.append(temp_df['min'][0])

	df['first_comment'] = first_comment

	return df


def first_joined():
	"""
	Web scraper to get users and when they first joined.
	"""
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	import os

	chromedriver = "/home/mjaron/FB_work/code/v2.1/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	# driver = webdriver.Chrome("/home/mjaron/FB_work/code/v2.1/chromedriver")
	# driver = webdriver.Firefox("./geckodriver.log")
	url = 'https://www.facebook.com/groups/156622701063707/members/'
	driver.get("http://www.python.org")
	assert "Python" in driver.title
	print(driver.title)
	elem = driver.find_element_by_name("q")
	elem.clear()
	elem.send_keys("pycon")
	elem.send_keys(Keys.RETURN)
	assert "No results found." not in driver.page_source
	driver.close()
	# driver.quit()


def main():
	"""
	Combine all functions.
	"""
	print('start gathering members')
	create_table()
	get_all_members()
	# first_joined()
	print("finished getting members")

if __name__ == '__main__':
	main()

