import pandas as pd 
import os
import re


def store_numbers(main_df):
	new_df = pd.DataFrame()
	temp_df = pd.DataFrame()
	store_num_list = []
	text_list = []
	for count, i in enumerate(main_df['text']):
		# i = '477.56'
		try:
			# store_num = [num for num in re.findall(r'[-+]?\d+[\.]?\d*[eE]?[-+]?\d*', i) if 3 <= len(num) <= 4]
			store_num = [num for num in re.findall(r'\b\d+\b', i) if 3 <= len(num) <= 4]
		except:
			continue
		# print store_num
		if len(store_num) > 0:
			for digit in store_num:
				a = i.find(digit)
				c = list(i[a-2:a+8])
				if a == 1:
					c = list(i[a-1:a+8])
				elif a == 0:
					c = list(i[a:a+8])
				# print c, 'heresadf'
				if '%' not in c and '$' not in c and '-' not in c and digit[:3] != '000' and \
								digit[:3] != '200' and digit[:3] != '201' and digit[:3] != '199'\
								and '.00' not in i[a:len(digit)+2]:
					i_ = i.replace('\r', '').replace('\n','')
					main_df['text'].ix[count] = i_
					temp_df = temp_df.append(main_df.ix[count])
					# print digit, "made it ******"

					if len(new_df) > 0:
						if main_df['user_name'][count] not in list(new_df['user_name']):
							new_df = new_df.append(main_df.ix[count])
							store_num_list.append(digit)
					else:
						new_df = new_df.append(main_df.ix[count])
						store_num_list.append(digit)

	
	print len(temp_df)
	print len(new_df)
	new_df['user_store_number'] = store_num_list
	temp_df.to_csv('temp.csv')
	new_df.to_csv('main.csv')
	
	print "finished store numbers"
	return new_df

def first_comment(main_df, new_df):
	first_comment = []
	num_comments = []
	for ids in new_df['user_ID']:
		temp = list(main_df['created_time'][main_df['user_ID'] == ids].copy())
		temp1 = pd.to_datetime(temp)
		temp2 = temp1.order()
		first_comment.append(temp2[0])
		num_comments.append(len(temp))

	new_df['user_num_of_posts'] = num_comments
	new_df['user_first_post'] = first_comment

	new_df = new_df.drop('Unnamed: 0', 1)
	cols = ['page_id', 'created_time', 'user_ID', 'user_name', 'user_store_number',\
	'user_num_of_posts', 'user_first_post', 'likes', 'message_ID', 'parent',  \
	 'type', 'photo_link', 'text']
	new_df = new_df[cols]
	new_df.to_csv('user_stores.csv', index=False)



def main():
	main_df = pd.read_csv('./results/Walmart_group_data.csv')
	# print len(main_df)
	# print 3695./len(main_df)
	# print len(set(main_df['user_name']))
	# print 3695./len(set(main_df['user_name']))

	new_df = store_numbers(main_df)
	first_comment(main_df, new_df)

if __name__ == "__main__":
	main()


