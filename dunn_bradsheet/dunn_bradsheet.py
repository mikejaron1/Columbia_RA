import os
import pandas as pd
import re
import csv

## look into fuzzywuzzy for string matching

def clean_files_and_detect_bad_files(file1, year):
    new_dict = {}
    
    for i in file1:
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
                    new_dict[field] = temp[len(test)+1:]
                    company_name = temp[len(test)+1:]
                    broken_file = file_name
                except:
                    new_dict[field] = temp
                    company_name = temp
                    broken_file = 'na'
                
                ## stop looping through all of the variables and stop at business name
                break
            
#             else:
#                 new_dict[field] = temp

        with open('company_names.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([company_name, year])
            

    return new_dict, broken_file


def main(directory, text_layot):
	broken_files = []
	# master_dict = {}
	for file_name in os.listdir(directory):
	    if '.TXT' in file_name:
	        year = file_name[file_name.find('DMI.')+4:file_name.find('.TXT')]
	        file1 = open(directory+file_name)
	        new_dict, broken_file = clean_files_and_detect_bad_files(file1, year)
	        if broken_file != 'na':
	            broken_files.append(broken_file)
	#         master_dict[year] = new_dict
	        df = pd.DataFrame({'broken_files': broken_files})
	        df.to_csv('broken_files.csv', index = False) 




if __name__ == '__main__':
	directory = '/home/research/datasets/dun-bradstreet/'
	text_layot = pd.read_excel(directory+'HISTORICAL Layout 560.xls', skiprows=1)
	
	## initiate file
	with open('company_names.csv', 'w') as f:
    	writer = csv.writer(f)
    	writer.writerow(['company_name', 'year'])

	main(directory, text_layot)


