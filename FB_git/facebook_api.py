# import urllib2
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import requests
import json
import pandas as pd 
import datetime
import os
import csv
import time
import pickle


from config import *

def url_creator(auth, pageID, fields):
	'''
	Takes in arguments and returns the search url needed
	'''
	base_url =  "https://graph.facebook.com/v2.8/"
	access = "&access_token="+auth
	fields = "?fields="+fields
	main_url = base_url+str(pageID)+fields+access

	return main_url


def new_auth_cont_url_creater(url):
	'''
	since auth changes every hour this is just in case it takes longer
	this will just ask for the new auth then use it to continue paginataion
	'''
# https://graph.facebook.com/v2.8/156622701063707/feed?fields=message,created_time,from,comments.limit%285%29%7Blikes.limit%280%29,message,created_time,from,id,parent%7D,likes.limit%280%29,full_picture&access_token=EAACEdEose0cBAEvkvaysdNJAG8pM37zUAJlAgvTfSXZA5SnIB9vMxpssyT0QR0lYOKU05BAnZADFOgOWYE8FaLEByLCHrcrXMvO68cvrBWrZBIrrY5rffIEZCXkoIsIlziyRjbnQzb45NNs1FLEOwL8ZA73urVprbg4AAajyTRQZDZD&limit=25&until=1479831833&__paging_token=enc_AdDZBncJaufmuuk0FX4HgrEACyiOiyp4KS3kFXlAI1yzLo2lEWtbN9XecGefgTkOe2550pMxzhAZAOK3PHO5s2ZBZBT9NF30iUgVwK3x2WkqMWDCHwZDZD
	auth_old = auth
	global auth
	auth = raw_input("new auth= ")
	url = url.replace(auth_old, auth)
	# s = url.find('access_token=')
	# e = url.find('&until=')
	# start = url[:s+13]
	# end = url[e:]
	# url = start+auth+end

	return url


def graph_api(url):
	'''
	takes in complete URL, calls the api and returns the page
	'''
	test = urlopen(url)
	page = json.loads(test.read())
	# data = page['data']

	return page

def parse_data(output, field, paginataion, first, ID):

	type_list = []
	text_list = []
	ID_list = []
	created_times = []
	store_list = []
	og_id = []
	like_count = []
	if_photo = []
	from_user_name = []
	from_user_id = []
	total_likes = []

	for i_ in output:

		try:
			text_list.append(i_['message'])
		except:
			try:
				text_list.append(i_['story'])
			except:
				continue
		try:
			link = i_['full_picture']
			if_photo.append(link)
		except:
			if_photo.append('na')
		
		type_list.append(field)
		store_list.append(store)
		ID_list.append(i_['id'])
		created_times.append(i_['created_time'])
		og_id.append(ID)
		try:
			from_user_name.append(i_['from']['name'])
			from_user_id.append(str(i_['from']['id']))
		except:
			# print(i_)
			from_user_name.append('na')
			from_user_id.append('na')

		total_likes.append(i_['likes']['summary']['total_count'])

		if i_['created_time'] < time_stop and field == 'feed':
			paginataion = False
			print("time stopped")
			break
	
		## every 30 seconds print the data it is at
		if round((time.time()-start_time),0) % 30 == 0:
			print(i_['created_time'], type(i_['created_time']))
			time.sleep(5)
			# print i_
			# raw_input('any key')
	if field == 'comments':
		url, paginataion = pagination_fun(output, first, field, paginataion)
	else:
		url = 'na'

	write_to_csv(field,type_list, ID_list, store_list, text_list, created_times, og_id, if_photo, \
					from_user_name, from_user_id, total_likes)
	
	return paginataion, url

	# return type_list, ID_list, store_list, text_list, created_times, og_id, if_photo, \
	# 		 from_user_name, from_user_id, total_likes, paginataion, url, i['id']


def feed_comment_search(url_, field, store, ID):
	'''
	THis
	'''

	# type_list = []
	# text_list = []
	# ID_list = []
	# created_times = []
	# store_list = []
	# og_id = []
	# like_count = []
	# if_photo = []
	# from_user_name = []
	# from_user_id = []
	# total_likes = []

	# temp_id_list = []

	paginataion = True
	first = True
	page_count = 0
	while paginataion:
		print("starting page feed search")
		field = 'feed'
		output, url_, paginataion = get_data(url_, field, first, paginataion)
		paginataion, url_na = parse_data(output, field, paginataion, first, ID='na')
		print("done page feed search")
		# # if paginataion:
		# for i in output:
		# 	try:
		# 		text_list.append(i['message'])
		# 	except:
		# 		try:
		# 			text_list.append(i['story'])
		# 		except:
		# 			continue
		# 	try:
		# 		link = i['full_picture']
		# 		if_photo.append(link)
		# 	except:
		# 		if_photo.append('na')
			
		# 	type_list.append(field)
		# 	store_list.append(store)
		# 	ID_list.append(i['id'])
		# 	created_times.append(i['created_time'])
		# 	og_id.append(ID)
		# 	from_user_name.append(i['from']['name'])
		# 	from_user_id.append(i['from']['id'])
		# 	total_likes.append(i['likes']['summary']['total_count'])
		
		# while comment_pagination:
		for comment_data in output:
			ID = str(comment_data['id'])
			try:
				comment_data = comment_data['comments']
			except:
				continue
			# temp_id_list.append(ID)
			field = 'comments'
			first = False
			comment_pagination = True
			comment_pagination, url = parse_data(comment_data, field, comment_pagination, first, ID)
			# if comment_pagination and url != 'na':
			while comment_pagination and url != 'na':
				print("starting comment pagination")
				# print url
				# first = False
				comment_data, url_na, comment_pagination = get_data(url, field, first, comment_pagination)
				comment_pagination, url = parse_data(comment_data, field, comment_pagination, first, ID)
			# if i['created_time'] < time_stop and field == 'feed':
			# 	paginataion = False
			# 	print "time stopped"
			# 	break
		
		page_count += 1
		first = False

	# temp_df = pd.DataFrame({'id': temp_id_list})
	# temp_df.to_csv('./resutls/comment_id_list.csv')

	print(page_count, 'total feed pages viewed')
	# return type_list, ID_list, store_list, text_list, created_times, og_id, if_photo, \
	# 		 from_user_name, from_user_id, total_likes



def write_to_csv(field,type_list, ID_list, store_list, text_list, created_times, og_id, if_photo, \
					from_user_name, from_user_id, total_likes):
	## after loop is done, assuming that is all for the page write it all to the csv
	if len(ID_list) > 0:
		new_df = pd.DataFrame()
		new_df['page_ID'] = store_list
		new_df['type'] = type_list
		new_df['user_name'] = from_user_name
		new_df['user_ID'] = from_user_id
		new_df['parent'] = og_id
		new_df['message_ID'] = ID_list
		new_df['created_time'] = created_times
		new_df['likes'] = total_likes
		new_df['photo_link'] = if_photo
		new_df['text'] = text_list


		filename = os.getcwd()+'/results/'+store+'.csv'
		# if not os.path.isfile(filename) or field == 'feed':
		if not os.path.isfile(filename):
			new_df.to_csv(filename, encoding='utf-8', index=False)
		else: # else it exists so append without writing the header
			new_df.to_csv(filename, mode = 'a', header=False, encoding='utf-8', index=False)
	



def like_counter(url, field="likes"):
	'''
	each like is outputed so this just counts up the total amount of likes from output
	'''

	paginataion = True
	first = True
	total = 0

	while paginataion:
		output, url, paginataion = get_data(url, field, first, paginataion)
		# if paginataion:
		total += len(output)
		first = False

	like_count = total

	return like_count


def get_data(url, field, first, paginataion):
	'''
	Main function that gets the data and gives the necessary output
	'''

	try:
		## since auth changes every hour this is just in case it takes longer
		## if the error occurs not within pagination then thats another problem
		try:
			main_output = graph_api(url)
		except:
			url = new_auth_cont_url_creater(url)
			main_output = graph_api(url)
			print("new auth worked")

		if first:
			output = main_output[field]['data']
		else:
			output = main_output['data']
	except:
		paginataion = False



	if paginataion and field != 'comments':
		url, paginataion = pagination_fun(main_output, first, field, paginataion)
	# 	if first:
	# 		try: 
	# 			url = main_output[field]['paging']['next']
	# 		except:
	# 			paginataion = False
	# 	else:
	# 		try:
	# 			url = main_output['paging']['next']
	# 		except:
	# 			paginataion = False

	if 'output' not in locals():
		output = 'na'

	return output, url, paginataion

def pagination_fun(main_output, first, field, paginataion):
	# print main_output
	# print field
	# print '\n'
	if first:
		try: 
			url = main_output[field]['paging']['next']
		except:
			paginataion = False
			url = 'na'
	else:
		try:
			url = main_output['paging']['next']
			if field == 'comments':
				## this then should only work for the first one and not needed after
				try:
					## 25 is default
					url = url.replace("limit=25", "limit=100")
				except:
					pass
		except:
			paginataion = False
			url = 'na'

	return url, paginataion



def get_all_members(url, field, store):
	'''
	written to get all members of a page, sefl contained gets the members and writes to csv
	'''
	print("starting get all members")
	paginataion = True
	first = True
	total = 0

	administrator = []
	member_ids = []
	names = []

	while paginataion:
		output, url, paginataion = get_data(url, field, first, paginataion)
		for i in output:
			names.append(i['name'])
			member_ids.append(i['id'])
			administrator.append(i['administrator'])
		first = False

			
	df = pd.DataFrame()
	df['name'] = names
	df['id'] = member_ids
	df['administrator'] = administrator
	df.to_csv('./results/'+store+'_members.csv', index=False, encoding='utf-8')

	print("finished getting all members")


# def batch_request_parse_data(url, field, store, ID):
# 	'''
# 	THis
# 	'''

# 	type_list = []
# 	text_list = []
# 	ID_list = []
# 	created_times = []
# 	store_list = []
# 	og_id = []
# 	like_count = []
# 	if_photo = []

# 	paginataion = True
# 	first = True
# 	page_count = 0
# 	while paginataion:
# 		output, url, paginataion = get_data(url, field, first, paginataion)
# 		# if paginataion:

# 		for i in output:
# 			try:
# 				text_list.append(i['message'])
# 			except:
# 				try:
# 					text_list.append(i['story'])
# 				except:
# 					continue
# 			try:
# 				if_photo.append(i['full_picture'])
# 			except:
# 				if_photo.append('na')
			
# 			type_list.append('feed')
# 			ID_list.append(i['id'])
# 			created_times.append(i['created_time'])
# 			og_id.append(ID)

# 			if i['created_time'] < time_stop and field == 'feed':
# 				paginataion = False
# 				print "time stopped"
# 				break
		
# 		page_count += 1
# 		first = False

# 	return type_list, ID_lis


def main(store):
	s_time = time.time()
	if FB_member_search:
		field = 'members'
		url = url_creator(auth, store, field)
		get_all_members(url, field, store)
	
	if comment_cont:
		ID_list = diff_ids
		# print(len(done_ids), " done IDs"
		# print len(all_ids), " all IDs"
		# print len(diff_ids), " difference"
	else:
		with open('./results/'+store+'.csv', 'w') as f:
			writer = csv.writer(f)
			writer.writerow(['page_ID', 'type', 'user_name','user_ID', 'parent','message_ID',\
    			'created_time', 'likes', 'photo_link', 'text'])

		field = 'feed.limit(100){full_picture,message,created_time,from,comments{likes.limit(0).summary(true),message,created_time,from,id},likes.limit(0).summary(true)}'
		# field = 'feed{full_picture,message,created_time,from,comments{likes.limit(0).summary(true),message,created_time,from,id},likes.limit(0).summary(true)}&limit=100'
		# field = 'feed{full_picture,id,created_time,message}'
		# field = 'feed{created_time,message,id}'
		url = url_creator(auth, store, field)
		field = 'feed'
		api_calls = 0
		feed_comment_search(url, field, store, ID='na')
		# type_list, ID_list, store_list, text_list, created_times, og_id, if_photo = \
		# 					feed_comment_search(url, field, store, ID='na')

		# write_to_csv(field, type_list, ID_list, store_list, text_list, \
		# 				created_times, og_id, if_photo)
	
		print("done")

		print("starting csv organizing")
		## organize by feed and comments and each by date
		df = pd.read_csv('./results/'+store+'.csv')
		print(len(df), "total rows")
		df_feed = df[df['type'] == 'feed']
		df_comments = df[df['type'] == 'comments']
		df_feed.sort_values('created_time', ascending=False, inplace=True)
		df_comments.sort_values('created_time', ascending=False, inplace=True)
		final_df = df_feed.append(df_comments)
		final_df.to_csv('./results/'+store+'.csv', index=False)
		print("done organizing")
	# print "starting comment seach for %s ids" % len(ID_list)
	# print '\n'
	
	# if len(ID_list) <= 0:
	# 	print "there is nothing in feed"
	# else:
	# 	# temp_flag = False
	# 	feed_ids = ID_list


		# feed_ids_df = pd.DataFrame({'all_ids': feed_ids})
		# feed_ids_df.to_csv('./results/all_ids.csv', index=False, encoding='utf-8')


		# comments_df = pd.DataFrame({'ID': []})
		# comments_df.to_csv('./results/comment_ids.csv', index=False, encoding='utf-8')
		# ## initiate done file
		# done_ids_df = pd.DataFrame({'done_ids': []})
		# done_ids_df.to_csv('./results/done_ids.csv', index=False, encoding='utf-8')
		
		# if comment_cont == False:
		# 	## initiate like count file
		# 	likes_df = pd.DataFrame({'ID': [], 'likes':[]})
		# 	likes_df.to_csv('./results/id_likes.csv', index=False, encoding='utf-8')

		# 	feed_ids_df.to_csv('./results/all_ids_from_feed.csv', index=False, encoding='utf-8')


		# per_done_0 = 0
		# new_dict = {}
		# new_id_list = []
		# like_count_list = []
		# new_feed_ids = []
		# for id_count, ID in enumerate(feed_ids): 
		# 	## prompt me for new auth every 55 min, use until i fugure out better solution
		# 	# if round(time.time()-s_time,0) == 3300.0:
		# 	# 	auth = raw_input('add new auth= ')
		# 	if '0' in str(id_count)[len(str(id_count))-1]:
		# 		# temp_flag = True
		# 		per_done = round((id_count/float(len(feed_ids)))*100,2)
		# 		if per_done_0 != per_done:
		# 			per_done_0 = per_done
		# 			print per_done, ' percent done'
		# 			time.sleep(.2)
		# 			print id_count
		# 		# print url
			
		# 	field = 'comments'
		# 	url = url_creator(auth, ID, field)
		# 	type_list, ID_list, store_list, text_list, created_times, og_id, if_photo = \
		# 	feed_comment_search(url, field, store, ID)

		# 	### continue to search for children as deep as possible
		# 	### AKA find comments of comments of comments .....
		# 	# feed_ids.extend(ID_list)

		# 	# new_feed_ids.extend(new_feed_ids)
		# 	comments_df = pd.DataFrame({'ID': ID_list})
		# 	comments_df.to_csv('./results/comment_ids.csv', mode='a', heading=False, index=False, encoding='utf-8')
		# 	## add to the all id list for reference
		# 	feed_ids_df = pd.DataFrame({'all_ids': ID_list})
		# 	feed_ids_df.to_csv('./results/all_ids.csv', mode='a',heading=False, encoding='utf-8', index=False)
			
		# 	field2 = "likes"
		# 	url = url_creator(auth, ID, field2)
		# 	like_count = like_counter(url)
		# 	# new_dict[ID] = like_count
		# 	likes_df = pd.DataFrame({'ID': [ID], 'likes':[like_count]})
		# 	likes_df.to_csv('./results/id_likes.csv', mode ='a', header=False, encoding='utf-8', index=False)


		# 	write_to_csv(field, type_list, ID_list, store_list, text_list, \
		# 				created_times, og_id, if_photo)

		# 	## when finished with ID save it to done file
		# 	done_ids_df = pd.DataFrame({'done_ids': [ID]})
		# 	done_ids_df.to_csv('./results/done_ids.csv', mode ='a', header=False, encoding='utf-8', index=False)

		# og_df = pd.read_csv('./results/'+store+'.csv')
		# likes_df = pd.read_csv('./results/id_likes.csv')
		# og_df = og_df.merge(likes_df, on='ID', how='left')
		## temp_like_list = [new_dict[i] for i in og_df['ID']]
		## og_df['like_count'] = temp_like_list
		## change up the column order
		# og_df = og_df[['store', 'type', 'OG_feed_id', 'ID', 'created_time', 'likes','text', 'photo_link']]
		# og_df.to_csv('./results/'+store+'.csv', index=False)

	

 # https://graph.facebook.com/v2.8/156622701063707/?fields=feed%7Bmessage%2Ccreated_time%2Cfrom%2Ccomments%7Blikes.limit(0).summary(true)%2Cmessage%2Ccreated_time%2Cfrom%2Cid%7D%2Clikes.limit(0).summary(true)%7D&access_token=EAACEdEose0cBAEdBHFs00cr0e6rF1F7OLOBoyYrsvxglAwiPKzdX9DwFbnaxO23PZCdmVBFex5NwjlAm0vVpQZCIZAFioosUxmiszbHrZBZCuXZA57u8v2g0ljL6YUlteiZCuBZCAQcZBQ1Bbuqcj427cgIRfEvsr7mSvO27yJ0HtIQZDZD

if __name__ == '__main__':
	
	## auth test
	# url = url_creator(auth, 'me', fields)
	# main_output = graph_api(url)

	## what files are you using
	if test:
		page_ids = [test_store]
		difference = page_ids
	else:
		if supercenter_file == False:
			## for new dataset with FB users
			df = pd.read_csv(file_name)
			page_ids = df['FacebookId']
			page_ids = page_ids.dropna()
			page_ids = [int(page) for page in page_ids]  #change it from float
		else:
			# for original dataset
			df = pd.read_csv(file_name)
			page_ids = df['fblink']
			page_ids = [page[page.find('com/')+4:] for page in page_ids]

		## find what has already been done
		difference = list(set(page_ids) - set(done_files) - set(does_not_exist))

	## add on most recent file to be done again, in case it stopped b4 it was 100% done
	## just needs to be uncommented if stops b4 100% done
	# difference.insert(0,max_file[:max_file.find('.csv')])

	store_count = 0
	for store in difference:
		start_time = time.time()
		# if 'Walmart' in store:
		# if int(store) > 0:
		print(store)
		main(str(store))

		total_time = time.time()-start_time
		print(total_time, "took this long")
		# time.sleep(60)
		store_count += 1
		print(store_count, "store index")
	
### this is just to run an api call for each id that didn't come back with comments but should have
	if missing_comment_search:
		start_time = time.time()
		store = test_store

		df1 = pd.read_csv('./results/'+store+'.csv')
		df1_feed_id = df1[df1['type'] == 'feed']['message_ID']
		df1_comments_id = df1[df1['type'] == 'comments']['parent']
		no_comment_ids = list(set(df1_feed_id) - set(df1_comments_id))

		print len(no_comment_ids), "making this many calls"
		for id_count, ID in enumerate(no_comment_ids):
			
			if '0' in str(id_count)[len(str(id_count))-1]:
				print id_count/float(len(no_comment_ids))

			comment_pagination = True
			first = True
			field = 'comments.limit(100){message,id,from,created_time,likes.limit(0).summary(true)}'
			url = url_creator(auth, ID, field)
			field = 'comments'
			comment_data, url_na, comment_pagination = get_data(url, field, first, comment_pagination)
			if comment_data == 'na':
				continue
			comment_pagination, url = parse_data(comment_data, field, comment_pagination, first, ID)
			while comment_pagination and url != 'na':
				print "starting paginataion"
				first = False
				comment_data, url_na, comment_pagination = get_data(url, field, first, comment_pagination)
				comment_pagination, url = parse_data(comment_data, field, comment_pagination, first, ID)


		df1 = pd.read_csv('./results/'+store+'.csv')
		df1 = df1.drop_duplicates()
		df1.to_csv('./results/'+store+'.csv')
		total_time = time.time()-start_time
		print(total_time, "took this long")





	# writing this for a temp fix of ids counts, as lengths will be diff
	# store = test_store
	# og_df = pd.read_csv('./results/'+store+'.csv')
	# likes_df = pd.read_csv('./results/id_likes.csv')
	# print len(og_df['ID']), len(set(og_df['ID']))
	# print len(likes_df['ID']), len(set(likes_df['ID']))
	# if len(likes_df['ID']) != len(set(likes_df['ID'])) and len(og_df['ID']) != len(set(og_df['ID'])):
	# 	a = raw_input('any key to continue')
	
	# like_id_diff = list(set(og_df['ID']) - set(likes_df['ID']))
	# print len(like_id_diff), " difference"
	# per_done_0 = 0
	# for id_count, ID in enumerate(like_id_diff):
	# 	if '0' in str(id_count)[len(str(id_count))-1]:
	# 		per_done = round((id_count/float(len(like_id_diff)))*100,2)
	# 		if per_done_0 != per_done:
	# 			per_done_0 = per_done
	# 			print per_done, ' percent done'
	# 			time.sleep(.2)
	# 	url = url_creator(auth, ID, fields='likes')
	# 	like_count = like_counter(url)
	# 	likes_df = pd.DataFrame({'ID': [ID], 'likes':[like_count]})
	# 	likes_df.to_csv('./results/id_likes.csv', mode ='a', header=False, encoding='utf-8', index=False)

	# og_df = pd.read_csv('./results/'+store+'.csv')
	# likes_df = pd.read_csv('./results/id_likes.csv')
	
	# print len(og_df['ID'])
	# print len(likes_df['ID'])
	# if len(likes_df['ID']) != len(og_df['ID']):
	# 	a = raw_input('any key to continue')

	# og_df = og_df.merge(likes_df, on='ID', how='left')
	# # change up the column order
	# og_df = og_df[['store', 'type', 'OG_feed_id', 'ID', 'created_time', 'likes','text', 'photo_link']]
	# og_df.to_csv('./results/'+store+'.csv', index=False)	




	