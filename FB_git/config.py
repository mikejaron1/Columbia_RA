'''
This page is meant as just the configuration set up
'''

import datetime
import os
import pandas as pd

## auth expires about every hour
auth = "EAACEdEose0cBAGSjUP2pGYgX8iJvZBxqCMq270l9SknEKb9ZAB6L3zBGb1tw21L1frPCzj8hEyl7OMhKIIIRS5ZBIYIsRAg9pcqxuB8htDrtdZA9m4f0boEsrEVzAjWdFf44xP186iYa70ZBF15V6rTjSSWuU1Gnyr7voZA8ZCIZCQZDZD"

## name of file, add in location if not in working directory
## comment necessary code block for df on other file
# file_name = "FacebookUser.csv"
file_name = "supercenterinfo.csv"
supercenter_file = False

## how far back do you want to search?
days = 365*10
## run a test with a specific store
test = True
## want to get all the members from a page
FB_member_search = False

## walmart group created March 28, 2011
test_store = "156622701063707"
# test_store = "Walmart1207"

## if program stops in comment search and want to continue
comment_cont = False

## if continuation of walmart stores after program stops on certain store
cont_store = False

missing_comment_search = True

## any pages not found add here
does_not_exist = ['Walmart763']



###########################################################################
########## dont edit below here ###################
#############################################################



newpath = os.getcwd()+'/results/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

stop = datetime.timedelta(days=days)
today = datetime.date.today()
time_stop = today-stop
time_stop = time_stop.strftime("%Y-%m-%dT%H:%M:%S+0000")
created_time = today.strftime("%Y-%m-%dT%H:%M:%S+0000")

## find done page ids through the file names
if cont_store:
	done_files = os.listdir(newpath)
	done_files = [i[:i.find('.csv')]for i in done_files]

## if program stops in comment search and want to continue
if comment_cont:
	# all_df = pd.read_csv('./results/all_ids.csv')
	all_df = pd.read_csv('./results/all_ids_from_feed.csv')
	all_ids = all_df['all_ids']
	done_df = pd.read_csv('./results/done_ids.csv')
	done_ids = done_df['done_ids']
	diff_ids = list(set(all_ids) - set(done_ids))

## find the last file that has been done if
max_mtime = 0
for dirname,subdirs,files in os.walk(newpath):
    for fname in files:
        full_path = os.path.join(dirname, fname)
        mtime = os.stat(full_path).st_mtime
        if mtime > max_mtime:
            max_mtime = mtime
            max_file = fname

