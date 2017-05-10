"""
All of the parsing functions.

AUTHOR: Mike Jaron
DATE: 2/12/17
"""
from sql_url_setup import graph_api


def parse_data(page, dict_main, time_stop, parent_id, type_):
	"""
	Parse all data.

	INPUT:
		page = list with json elements with each one being a post
		dict_main = main dict to update
		search_ids = list to be updated with new ids to search
		parent_id = string with id of parent if comment or reply
		type_ = string of type of message; post, comment, or reply
	OUTPUT:
		dict_main = updated main dictionary
		search_ids = updated list with ids to search on for reactions and comments
		pagination = boolean if False if time stopped
	"""
	pagination = True

	for post in page:
		# no need to time stop for comments
		# added in updated_time b/c that is how it is ordered and would stop
		# early if not
		if type_ == 'post' and post['updated_time'] < time_stop:
			pagination = False
			print("time stopped")
			break

		try:
			dict_main['user_name'].append(post['from']['name'])
		except:
			dict_main['user_name'].append(None)
		try:
			dict_main['user_id'].append(post['from']['id'])
		except:
			dict_main['user_id'].append(None)

		dict_main['message_id'].append(post['id'])
		dict_main['type'].append(type_)
		dict_main['created_time'].append(post['created_time'])

		# below are items that may or may not appear

		# trying to deal with different outputs of attachements based on if it is in
		# a feed or not or has subattachements, etc. Made function due to complexity
		dict_main = attachment_parse(post, dict_main, type_)
		
		# to deal with the lists created of the story and message tags
		dict_main = message_story_tag_parse(post, dict_main)

		try:
			# make sure to take off any break lines
			dict_main['message'].append(post['message'].replace('\r', ' ') 
													.replace('\n', ' '))
		except:
			dict_main['message'].append(None)

		try:
			# make sure to take off any break lines
			dict_main['story'].append(post['story'].replace('\r', ' ')
													.replace('\n', ' '))
		except:
			dict_main['story'].append(None)

		if type_ == 'comment' or type_ == 'reply':

			dict_main['parent'].append(parent_id)
			dict_main['like_count'].append(post['like_count'])
			dict_main['love_count'].append(0)
			dict_main['wow_count'].append(0)
			dict_main['haha_count'].append(0)
			dict_main['sad_count'].append(0)
			dict_main['angry_count'].append(0)

			dict_main = comments_parse_pagination(post, dict_main, time_stop, 
					parent_id=post['id'], type_='reply')

		else:
			dict_main['parent'].append('na')
			dict_main = reaction_crawl_parse(post, dict_main)
		
			dict_main = comments_parse_pagination(post, dict_main, time_stop, 
					parent_id=post['id'], type_='comment')
					
	return dict_main, pagination


def comments_parse_pagination(post, dict_main, time_stop, parent_id, type_):
	"""
	Deal with pagination of comments and replys.
	"""
	try:
		reply_page = post['comments']['data']
		comment_flag = True
	except:
		comment_flag = False

	if comment_flag:
		dict_main, temp1 = parse_data(reply_page, dict_main,
				time_stop, parent_id=parent_id, type_=type_)
		
		try:
			comment_page = graph_api(post['comments']['paging']['next'])
			page_flag = True
		except:
			page_flag = False
		
		# below here is for pagination
		while page_flag:
			print('paging %s \n' % type_)
			dict_main, temp1 = parse_data(comment_page['data'], dict_main,
				time_stop, parent_id=parent_id, type_=type_)
			try:
				comment_page = graph_api(comment_page['paging']['next'])
			except:
				page_flag = False

	return dict_main


def message_story_tag_parse(post, dict_main):
	"""
	Parse story and message tags.

	INPUT:
		post = dict of each message
		dict_main = main dict
	OUTPU:
		dict_main = updated main dict
	"""
	for tag in ['story', 'message']:
		try:
			tags = post[tag + '_tags']
			count = len(tags)
			if len(tags) > 1:
				# add the list as 1 element
				tags_list = []
				id_list = []
				for i in tags:
					tags_list.append(i['name'])
					id_list.append(i['id'])
				names = str(tags_list)
				ids = str(id_list)
			else:
				# if there is just 1 then add it in with out the list
				names = tags[0]['name']
				ids = tags[0]['id']
		except: 
			count = 0 
			names = None
			ids = None

		# set variables above so that way we don't append until it is all done
		dict_main[tag + '_tag_count'].append(count)
		dict_main[tag + '_tag_names'].append(names)
		dict_main[tag + '_tag_ids'].append(ids)

	return dict_main


def attachment_parse(post, dict_main, type_):
	"""
	Parse attachment info.

	INPUT:
		post = dict of each message
		dict_main = main dict
		type_ = string of type of search; comment, reply or post
	OUTPUT:
		dict_main = updated dictionary
	"""
	# if comment or reply, attachment is not plural and there can be only 1
	if type_ == 'comment' or type_ == 'reply':
		try:
			attachments = post['attachment']
			# depending on type depends on different locations for data
			if post['attachment']['type'] == 'photo':
				attach = attachments['media']['image']['src']
			else:
				attach = attachments['url']
			
			attach_type = attachments['type']
		except:
			attach = 'na'
			attach_type = 'na'

	else:
		try:
			# it is always first element
			attachments = post['attachments']['data'][0]
			try:
				# if multiple subattachments, get info in loop then add to dict as
				# 1 item list
				attachments = attachments['subattachments']['data']
				att_url = []
				att_type = []
				for i in attachments:
					if attachments['type'] == 'photo':
						att_url.append(i['media']['image']['src'])
					else:
						att_url.append(i['url'])
					att_type.append(i['type'])

				attach = str(att_url)
				attach_type = str(att_type)

			except:
				# depending on type depends on different locations for data
				if attachments['type'] == 'photo':
					attach = attachments['media']['image']['src']
				else:
					attach = attachments['url']
				attach_type = attachments['type']
		except:
			attach = None
			attach_type = None
	
	# set variables above so that way we don't append until it is all done
	dict_main['attachment'].append(attach)
	dict_main['attachment_type'].append(attach_type)

	return dict_main


def reaction_crawl_parse(page, dict_main):
	"""
	Get the reaction fromt he graph api and then parse, for posts only.

	INPUT:
		search_ids = list of ids to search on
		dict_main = main dict to be updated
	OUTPUT:
		dict_main = updated dict to be passed around
	"""
	pagination = True

	like_count = 0
	love_count = 0
	wow_count = 0
	haha_count = 0
	sad_count = 0
	angry_count = 0

	try:
		# first see if there are even any reactions
		page = page['reactions']
	except:
		pagination = False

	while pagination:
		try:
			next_page = page["paging"]["next"]
		except:
			pagination = False

		for post in page['data']:
			if post['type'] == 'LIKE':
				like_count += 1
			elif post['type'] == 'LOVE':
				love_count += 1
			elif post['type'] == 'WOW':
				wow_count += 1
			elif post['type'] == 'HAHA':
				haha_count += 1
			elif post['type'] == 'SAD':
				sad_count += 1
			else:
				angry_count += 1

		if pagination:
			page = graph_api(next_page)
			# print("starting reaction pagination \n")

	dict_main['like_count'].append(like_count)
	dict_main['love_count'].append(love_count)
	dict_main['wow_count'].append(wow_count)
	dict_main['haha_count'].append(haha_count)
	dict_main['sad_count'].append(sad_count)
	dict_main['angry_count'].append(angry_count)

	return dict_main
