"""
This is to create the table with columns, only run this the the very FIRST time!

Author: Michael Jaron
Date: 2/12/17
"""

import psycopg2


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
	cur.execute('DROP TABLE IF EXISTS feed')
	cur.execute("""CREATE TABLE feed (
	            type TEXT, -- comment vs post vs reply
	            user_name TEXT, --name of user who posted
	            user_id BIGINT, --numerical id of each user
	            parent TEXT, -- id of parent only if comment or reply
	            message_id TEXT, --id of the message
	            created_time TIMESTAMP, --when message was created
	            like_count INT, -- total number of likes
	            love_count INT, -- if not comment or reply, total # of love
	            wow_count INT, -- if not comment or reply, total # of wow
	            haha_count INT, -- if not comment or reply, total # of haha
	            sad_count INT, -- if not comment or reply, total # of sad
	            angry_count INT, -- if not comment or reply, total # of angry
	            story TEXT, -- message of the story if it is one
	            story_tag_count INT, -- total number of story tags
	            story_tag_names TEXT, -- list story tag name
	            story_tag_ids TEXT, -- list of all story tag ids
	            message_tag_count INT, -- total number of message tags
	            message_tag_names TEXT, -- list message tag names
	            message_tag_ids TEXT, -- list message tag ids
	            attachment TEXT, --if message contains link, including photo or share
	            attachment_type TEXT, -- type of attachement, photo, share, etc
	            message TEXT --text of message
	            );""")
	con.commit()


if __name__ == '__main__':
	create_table()
	print('created empty table')
