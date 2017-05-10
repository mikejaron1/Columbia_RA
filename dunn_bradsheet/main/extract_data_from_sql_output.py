
import pandas as pd
import os


# tennessee, 2000-2015.
# Tennessee	Tenn.	TN, code = 83
# dstateco  = text = STATE ABBREVIATION
# dstateab = text	= DUN AND BRADSTREET STATE CODE *indexed

def main():
	directory = '/home/mjaron/dunn_bradsheet/sql_output/'
	output_dir = '/home/mjaron/dunn_bradsheet/sql_output/subsets/TN/'
	
	# for i in os.listdir(directory):
	# 	if '.csv' in i and 'emp' in i and '20' in i:
	# 		year = i[10:14]
	# 		df = pd.read_csv(directory + i)
	# 		df_new = df[df['dstateco'] == 83]
	# 		df_new.to_csv(output_dir + 'TN_emp_sales_' + year + '.csv', index=False)
	# 		print('finished', i)

	# df = pd.read_csv(directory + 'sums_means_all.csv')
	# df_new = df[df['dstateco'] == 83]
	# df_new = df_new[df_new['year'] >= 2000]
	# df_new.to_csv(output_dir + 'TN_sums_means_2000_2015.csv', index=False)
	# print('finished sums and means')

	# df = pd.read_csv(directory + 'sql_export_all_years.csv')
	# df_new = df[df['dstateco'] == 83]
	# df_new = df_new[df_new['year'] >= 2000]
	# df_new.to_csv(output_dir + 'TN_all_2000_2015.csv', index=False)
	# print('finished everything')


if __name__ == '__main__':
	main()
