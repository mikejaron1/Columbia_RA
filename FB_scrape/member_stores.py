
'''
Auther: Michael Jaron
Date: 1/30/17
Purpose: This is to try to find all store numbers in the scraped facebook data.
'''

import pandas as pd 
import re


def store_numbers(main_df, directory, basic=True):
	"""
	Find all the store numbers that people write.

	Arguments:
		basic = 'True', finds any sentence with any integer in it.
				'False', tries to find actual store numbers by a bunch of
						 specific rules.

	INPUT:
		main_df = pandas data frame, which are all of the results of the scrape

	OUTPUT:
		new_df = pandas data frame, which are the results of this search including
				all original columns plus a few more
		*also auto saves pandas dataframe

	"""
	# make a copy to not screw anything up
	new_df = main_df
	# lists I will use
	store_num_list = []
	index_list = []
	text_list = []

	for count, i in enumerate(main_df['text']):

		if basic:
			try:
				# this regular expression finds any integer, even if there are no spaces
				store_num = [num for num in re.findall(r'\d+', i)]
			except:
				continue

			# just another check if there are acutally numbers in the list
			if len(store_num) > 0:
				store_num_list.append(store_num)
				# get rid of any line breaks
				text_list.append(i.replace('\r', '').replace('\n', ''))
				# saving index to keep
				index_list.append(count)

		else:
			try:
				# store_num = [num for num in re.findall(r'[-+]?\d+[\.]?\d*[eE]?[-+]?\d*', i) if 3 <= len(num) <= 4]
				# finds text with numbers if they are at 3 and 4 digits long and seperated by spaces
				store_num = [num for num in re.findall(r'\b\d+\b', i) if 3 <= len(num) <= 4]
			except:
				continue

			# just another check if there are acutally numbers in the list
			if len(store_num) > 0:
				# looks at each individual number in the list
				for digit in store_num:
					# looks at in in context of the entire sentence
					a = i.find(digit)
					# gets surronding characters based on position
					c = list(i[a - 2:a + 8])
					if a == 1:
						c = list(i[a - 1:a + 8])
					elif a == 0:
						c = list(i[a:a + 8])
					# random things i found that prob dont relate to store numbers
					# I am now looking at the surronding characters, not just the numbers
					if '%' not in c and '$' not in c and '-' not in c and digit[:3] != '000' and \
						digit[:3] != '200' and digit[:3] != '201' and digit[:3] != '199'\
						and '.00' not in i[a:len(digit) + 2]:
						
						store_num_list.append(digit)
						# get rid of any line breaks
						text_list.append(i.replace('\r', '').replace('\n', ''))
						# saving index to keep
						index_list.append(count)

						# finds if user already reported user name
						# not using for now, just going to report all
						# if deciding to use again the method of saving needs to be changed
						# i_ = i.replace('\r', '').replace('\n','')
						# main_df['text'].ix[count] = i_
						# if len(new_df) > 0:
						# 	if main_df['user_name'][count] not in list(new_df['user_name']):
						# 		new_df = new_df.append(main_df.ix[count])
						# 		store_num_list.append(digit)
						# else:
						# 	new_df = new_df.append(main_df.ix[count])
						# 	store_num_list.append(digit)

	# keep only rows with the potential store number
	new_df = new_df.ix[index_list]
	# drop the original text column
	new_df = new_df.drop('text', axis=1)
	# add in new text column with the line breaks removed
	new_df['text'] = text_list
	new_df['user_store_number'] = store_num_list

	# keep only columns needed and re-arrange them
	cols = ['page_id', 'created_time', 'user_ID', 'user_name', 'user_store_number',
		'likes', 'message_ID', 'parent', 'type', 'photo_link', 'text']
	new_df = new_df[cols]

	# save name based on search type
	if basic:
		new_df.to_csv(directory + 'store_numbers_basic_search.csv', 
			encoding='utf-8', index=False)
	else:
		new_df.to_csv(directory + 'store_numbers_complex_search.csv', 
			encoding='utf-8', index=False)

	print("found %s potential store numbers" % len(new_df))
	print("about %s percent of total comments" % (len(new_df) / float(len(main_df))))
	print("finished store numbers")

	return new_df


def main():
	directory = '/home/mjaron/FB_work/data/main_data/'
	main_df = pd.read_csv(directory + 'Walmart_group_data.csv', encoding="ISO-8859-1")
	print('read in csv')

	new_df = store_numbers(main_df, directory, basic=True)
	# do it here to get all users first comment if they also posted store ids
	# first_comment(main_df, new_df)

	# to get first comment of all members
	# main_all_members = pd.read_csv('./results/Walmart_group_members.csv')
	# first_comment(main_df, main_all_members)

if __name__ == "__main__":
	main()


