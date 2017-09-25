This is the complete readme on how to get data from a Walmart page.

SUMMARY:
This program uses the Facebook Graph API to gather data on a Facebook group. Current working version is v2.1, please use all files in this folder (/home/mjaron/FB_work/code/v2.1/).


HOW IT RUNS:
The cronjob runs the code every Sunday at 4am. It first finds any new posts and comments made since the last search and then updates the users table with any new members and their first comment. If the auth expires, which it will every 2 months, an email, to the address in the config.py file, should be sent letting you know that has happened. Once it has follow the instructions below to get a new long term auth token. If anything goes wrong an email should be sent to let you know.


HOW TO MANUALLY OPERATE:
1*. Run the 'fb_create_feed_table.py' code to create the table to populate. **Only do this the very first time!** If you do it after data has been put in, it will all be erased.
2. Then run 'main_fb_api_scrape.py', if after first time then just skip to this step.
3. Run members_firsts.py to update user table with all members and their first comment.

* main_run.sh is a shell scrip that runs 2 and 3 above (type into terminal "sh /home/mjaron/FB_work/code/v2.1/main_run.sh")



TO GET A NEW LONG TERM AUTH TOKEN:
First get short term token:
	1. go to developers.facebook.com/tools/explorer/
	2. log in with Angelas login
	3. click on the drop down, below "My Apps", and click on one that says 
		"Graph API Explorer", click on "Columbia_toy"
	4. click on the dropdown below, "Get Token"
	5. click "Get User Access Token"
    5a. Confirm all boxes are selected and press "Get Access Token"
	6. copy the user token in the box and paste it in the "input.txt" file, overwriting
		the token currently in the file
Get long term token:
	1. Run "get_long_lived_auth.py"
	2. all set, re-run program like usual
	2a. just run main_run.sh (type into terminal "sh /home/mjaron/FB_work/code/v2.1/main_run.sh")



to get everything in the sql server to csv
\copy feed to 'test.csv' csv header



NOTES:
for feed info
https://developers.facebook.com/docs/graph-api/reference/v2.8/post

expiration of tokens
https://developers.facebook.com/docs/facebook-login/access-tokens/expiration-and-extension

App creation
https://developers.facebook.com/tools/javascript-console/
https://github.com/ismaelc/MashapeFBSentimentExample
