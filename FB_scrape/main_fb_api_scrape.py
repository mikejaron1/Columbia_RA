"""
This is to get all of the information needed from the Facebook graph API.

Author: Michael Jaron
Date: 2/19/17
"""
import time
import sys
# appending where site packages are, cron was having a hard time finding packages
# sys.path.append("/opt/anaconda3/lib/python3.5/site-packages/")

import psycopg2
# import sqlite3
# :x
# from sqlalchemy import create_engine

from config import time_stop, page_id, auth, limit1, limit2, limit3, email
from fb_data_parser import parse_data
from fb_data_frames import create_dict, dict_to_df
from sql_url_setup import send_to_postgres, url_creator, graph_api, \
	email_notify


def delete_duplicates_postgres():
	"""
	Delete any duplicate rows in the table after each session.
	
	This may happen because some older posts may be recentyly updated
	and if that happens it will pull them into the database.
	"""
	# con = sqlite3.connect(database='facebook')

	con = psycopg2.connect(database='facebook')
	cur = con.cursor() 
	print('here1')
	cur.execute("""DELETE FROM feed 
  						WHERE ctid = ANY(ARRAY(SELECT ctid 
                 		FROM (SELECT row_number() OVER (PARTITION BY 
                 		message_id), ctid 
                        FROM feed) x 
                 		WHERE x.row_number > 1));""")
	con.commit()
	print('here2')
	# now create an index on message and user ids
	cur.execute("""DROP INDEX IF EXISTS ids;""")
	con.commit()
	cur.execute("""CREATE INDEX ids ON feed 
									(message_id, user_id, created_time);""")
	con.commit()
	con.close()


def start_feed_crawl(url, dict_main):
	"""
	Main starting point.

	INPUT:
		url = string of main starting url
		dict_main = main dict to be updated
	OUTPUT:
		dict_main = updated dict to be passed around
	"""
	# always start off assuming True
	pagination = True

	# render URL to JSON
	page = graph_api(url)

	try:
		# grab all posts
		page_posts = page["feed"]["data"]
	except:
		if page['error']['code'] == 1:
			# may want to reduce data requested, sometimes waiting works
			print(page)
			print('waiting 2 min and trying again')
			time.sleep(120)
			page = graph_api(url)
			try:
				page_posts = page["feed"]["data"]
			except Exception as e:
				email_notify(email, e, page)
				sys.exit('problem in data %s' % e)

	# extract next page
	try:
		next_page = page["feed"]["paging"]["next"]
	except:
		pagination = False

	dict_main, pagination = parse_data(page_posts, dict_main, time_stop,
									parent_id='na', type_='post')

	# send all data from current page to postgres
	df = dict_to_df(dict_main)
	send_to_postgres(df, table='feed')

	# re-initialize dict
	dict_main = create_dict()

	while pagination:
		print("starting feed pagination")
		page = graph_api(next_page)
		try:
			next_page = page["paging"]["next"]
		except:
			pagination = False

		try:
			page_posts = page["data"]
		except Exception as e:
			print(page)
			print('problem with feed page')
			broken_entries.write('%s %s %s %s' % (str(e), '/ feed, pagination =', 
												pagination, page))
			continue

		dict_main, pagination = parse_data(page_posts, dict_main, time_stop,
								parent_id='na', type_='post')		

		# send all data from current page to postgres
		df = dict_to_df(dict_main)
		send_to_postgres(df, table='feed')

		# re-initialize dict
		dict_main = create_dict()


def main():
	"""
	Combine all functions.
	"""
	# initiate an empty log files to track errors
	global broken_entries
	broken_entries = open('errors.log', 'w')

	# create the empty dict
	dict_main = create_dict()

	# doing all of this at once greatly reduces the amount of api calls
	fields = "feed.limit(" + str(limit1) + "){message,created_time," + \
		"reactions.limit(" + str(limit3) + ")," + \
		"updated_time,attachments,story,story_tags,message_tags,from," + \
		"comments.limit(" + str(limit2) + "){created_time,from,message,id," + \
		"like_count,message_tags,attachment," + \
		"comments.limit(" + str(limit2) + "){created_time,from,message," + \
		"id,like_count,message_tags,attachment} } }"
	
	# start things off with first feed search and crawl
	url = url_creator(auth, fields, page_id)

	start_feed_crawl(url, dict_main)

	print('start deleting duplicates')
	delete_duplicates_postgres()

	print("finished everything")


if __name__ == '__main__':
	start = time.time()
	# if anything goes wrong then an email will me sent
	try:
		main()
	except Exception as e:
		email_notify(email, e, page='NA')
	# temperary to see if the chron job is working	
	email_notify(email, 'Finished api scrape', page='NA')
	print('total seconds it took ' + str(time.time() - start))
