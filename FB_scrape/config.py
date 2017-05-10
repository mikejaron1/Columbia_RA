"""
This page is meant as just the configuration set up.
"""
import os
import sys
import datetime
# appending where site packages are, cron was having a hard time finding packages
sys.path.append("/opt/anaconda3/lib/python3.5/site-packages/")

from sqlalchemy import create_engine
import pandas as pd


# get long term auth lasts about 2 months
f = open(os.path.join(sys.path[0], "auth_info.txt"), "r")
auth = f.read()

# id to walmart employee closed group
page_id = '156622701063707'

email = 'mikejaron@gmail.com'

# how far back do you want to search?, I beleive group was created on 
# March 28, 2011, so if you want all just add in 100 years, 36500 days
days = 36500


stop = datetime.timedelta(days=days)
today = datetime.date.today()
time_stop = today - stop
time_stop = time_stop.strftime("%Y-%m-%dT%H:%M:%S+0000")

# the higher the numbers are below the faster it will run but the greater
# likelihood it will fail due to requesting to much data. I have played around
# with it to find what I think is the optimal amount.
# comments to feed is roughly 14/1 and reply to feed is roughly 6/1
limit1 = 20  # feed limit
limit2 = 90  # comments and reply limit
limit3 = 150  # reaction limit

# activate this after first time to just update the database
cont = True
if cont:
	engine = create_engine('postgresql://mjaron@localhost:5432/facebook')
	df = pd.read_sql("SELECT max(created_time) FROM feed;", engine) 
	time_stop = df['max'][0].strftime("%Y-%m-%dT%H:%M:%S+0000")

