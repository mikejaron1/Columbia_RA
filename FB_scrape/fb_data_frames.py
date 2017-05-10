"""
Create empty dataframe and also turn the dict to a dataframe.

Author: Michael Jaron
Date: 2/12/17
"""


import pandas as pd


def dict_to_df(dict_main):
	"""
	Turn dict into pandas data frame.

	INPUT:
		dict_main = complete dictionary
	OUTPUT:
		df = pandas dataframe
	"""
	df = pd.DataFrame()
	df['type'] = dict_main['type']
	df['user_name'] = dict_main['user_name']
	df['user_id'] = dict_main['user_id']
	df['parent'] = dict_main['parent']
	df['message_id'] = dict_main['message_id']
	df['created_time'] = dict_main['created_time']
	df['like_count'] = dict_main['like_count']
	df['love_count'] = dict_main['love_count']
	df['wow_count'] = dict_main['wow_count']
	df['haha_count'] = dict_main['haha_count']
	df['sad_count'] = dict_main['sad_count']
	df['angry_count'] = dict_main['angry_count']
	df['story_tag_count'] = dict_main['story_tag_count']
	df['story_tag_names'] = dict_main['story_tag_names']
	df['story_tag_ids'] = dict_main['story_tag_ids']
	df['message_tag_count'] = dict_main['message_tag_count']
	df['message_tag_names'] = dict_main['message_tag_names']
	df['message_tag_ids'] = dict_main['message_tag_ids']
	df['story'] = dict_main['story']
	df['attachment'] = dict_main['attachment']
	df['attachment_type'] = dict_main['attachment_type']
	df['message'] = dict_main['message']

	return df


def create_dict():
	"""
	Create main dictionary to be passed around the functions to save the data.

	INPUT:
		None
	OUTPUT:
		Dictionay with keys and lists as values
	"""
	dict_main = {
		'type': [],
		'user_name': [],
		'user_id': [],
		'parent': [],
		'message_id': [],
		'created_time': [],
		'like_count': [],
		'love_count': [],
		'wow_count': [],
		'haha_count': [],
		'sad_count': [],
		'angry_count': [],
		'story_tag_count': [],
		'story_tag_names': [],
		'story_tag_ids': [],
		'message_tag_count': [],
		'message_tag_names': [],
		'message_tag_ids': [],
		'story': [],
		'attachment': [],
		'attachment_type': [],
		'message': []
	}

	return dict_main
