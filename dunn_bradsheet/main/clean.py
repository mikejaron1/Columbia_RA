# mainly to clean the data and output a csv with all variables
# simplified this to just get business name and year
import os
import pandas as pd
import re
import csv
import time
import codecs

def clean_files_and_detect_bad_files(file1, year):
	new_dict = {}
	for line_count, i in enumerate(file1):
		for count, field in enumerate(text_layot['FIELD DESCRIPTION']):
			temp = i[text_layot['START'][count]-1:text_layot['END'][count]]
            
            		## set this up to try to decipher which files are not in line with the excel sheet
            		## business name is the second field and should just be characters
            		## it seems the corrupt files have longer dun #'s that run into the name
            		## I am just checking the first line b/c all of the lines should be same
			if field == "BUSINESS NAME":
				r = re.compile("([0-9]+)")
				m = r.match(temp)
				try:
					test = m.group(1)
					temp = i[text_layot['START'][count]-1:text_layot['END'][count]+len(test)+1]
					new_dict[field] = temp[len(test)+1:]
					company_name = temp[len(test)+1:]
					broken_file = year
				except:
					new_dict[field] = temp
					company_name = temp
					broken_file = 'na'
                
                		## stop looping through all of the variables and stop at business name
				break
            
#          		else:
#                 		new_dict[field] = temp

		with open('company_names.csv', 'a') as f:
            		writer = csv.writer(f)
            		writer.writerow([company_name, year])
	
		#if line_count >= 5:
			#break    

	return new_dict, broken_file


def main(directory, text_layot):
	broken_files = []
	# master_dict = {}
	done_files = []
	for file_name in os.listdir('./dunn_data/'):
		if '.TXT' in file_name and '.zip' not in file_name:
			print(file_name)
			year = file_name[file_name.find('DMI.')+4:file_name.find('.TXT')]
			#file1 = open('./dunn_data/'+file_name, 'r', encoding='utf-8')
			file1 = codecs.open('./dunn_data/'+file_name,'r',  encoding='utf-8', errors='ignore')
			#file1 = file1.readlines()
			new_dict, broken_file = clean_files_and_detect_bad_files(file1, year)
			if broken_file != 'na':
				broken_files.append(broken_file)
	#         	master_dict[year] = new_dict
			df = pd.DataFrame({'broken_files': broken_files})
			df.to_csv('broken_files.csv', index = False) 
			done_files.append(file_name)
			done_df = pd.DataFrame({'done_files': done_files})
			done_df.to_csv('done_files.csv', index= False)

if __name__ == '__main__':
	print("Starting")
	start = time.time()

	directory = '/home/research/datasets/dun-bradstreet/'
	text_layot = pd.read_excel(directory+'HISTORICAL Layout 560.xls', skiprows=1)
	
	## initiate file
	with open('company_names.csv', 'w') as f:
    		writer = csv.writer(f)
    		writer.writerow(['company_name', 'year'])
	
	main(directory, text_layot)
	
	end = time.time()
	total = end-start
	print("took ", str(total), " seconds")
	print("Finished")


