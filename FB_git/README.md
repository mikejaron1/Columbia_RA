This will take a list of Facebook pages and calls the API to get feed data, all comments and likes for each comment for each page and outputs that to a csv.

Edit the config file for all of the general changes listed below.

auth = [auth from facebook],
file_name = [name or directory plus name of file you want to load], 
supercenter_file = [True or False] # depends on file given above, 
days = [range of days to look back >= 1], 
test = [True or False] # if test is set to True then file_name does not matter, 
