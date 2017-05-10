import pandas as pd
from sqlalchemy import create_engine    
import datetime  
import os


def years(year, engine, output_dir):
# First spreadsheet:
# [dun id, parent dun id, state, first SIC, employment, sales]

# Second spreadsheet:
# [dun id, business name]
	while year >= 1969:
		print(year)
		df = pd.read_sql("""SELECT duns, dpardun, dstateco, dprimsi, demplher, dsalesvo FROM main 
					WHERE year = '%s'
       				""" %year, engine)       

		df.to_csv(output_dir+'/emp_sales_%s.csv' %year, index=False)


		df = pd.read_sql("""SELECT duns, dcomp FROM main 
					WHERE year = '%s'
       				""" %year, engine)       

		df.to_csv(output_dir+'comp_names_%s.csv' %year, index=False)
	
		year = year - 1



def sums_means_sql(year, engine, output_dir):
	'''
	attempted this method with more sql
	'''
	df = pd.read_sql("""SELECT DISTINCT dstateco FROM main 
   				""", engine) 
	df = df.dropna()
	state_codes = df['dstateco']
	df.to_csv(output_dir+'state_codes.csv', index = False)


	df = pd.read_sql("""SELECT DISTINCT dprimsi FROM main 
	   				""", engine) 
	df = df.dropna()
	sic_codes = df['dprimsi']
	df.to_csv(output_dir+'sic_codes.csv', index = False)


	df_main = pd.DataFrame()

	while year >= 1969:
		print(year)
		for stateco in state_codes:
			print(stateco)
			for sicco in sic_codes:
				df = pd.read_sql("""SELECT SUM(demplher) as sum_emp, SUM(dsalesvo) as sum_sale,
									 AVG(demplher) as avg_emp, AVG(dsalesvo) as avg_sale FROM main 
									WHERE dstateco = '%s' AND year = '%s' AND dprimsi = '%s' """ 
									%(stateco, year, int(sicco)), engine) 

				df['year'] = year
				df['dstateco'] = stateco
				df['dprimsi'] = sicco
				df_main = df_main.append(df)

		year = year -1

	df_main.to_csv(output_dir+'stateco_sic_year_means.csv', index = False)





def sums_means(year, engine, output_dir):
	'''
	Attempted this method with more python, not sure which one is faster
	'''
	# df = pd.read_sql("""SELECT MIN(dstateco), MAX(dstateco) FROM main 
 #       				""", engine) 

	# min_stateco = int(df['min'][0])
	# max_stateco = int(df['max'][0])
	# print("min and max state code")
	# print(min_stateco, max_stateco)

	df = pd.read_csv(output_dir+'state_codes.csv')
	state_codes = df['dstateco']

	total_rows_saved = 0
	while year >= 1969:
		print(year)
		for stateco in state_codes:
			print(stateco)
		# stateco = max_stateco+1
		# while stateco > min_stateco:
			# stateco = stateco - 1
			df = pd.read_sql("""SELECT dprimsi, demplher, dsalesvo FROM main 
				WHERE dstateco = '%s' AND year = '%s' """ %(stateco, year), engine) 

			if len(df) == 0:
				continue

			df0 = df.groupby(['dprimsi'])['demplher', 'dsalesvo'].mean()
			df0 = df0.reset_index()
			df_main = df0.rename(columns={"demplher": "demplher_mean", "dsalesvo": "dsalesvo_mean"})

			df1 = df.groupby(['dprimsi'])['demplher', 'dsalesvo'].sum()
			df1 = df1.reset_index()
			df_main['demplher_sum'] = df1['demplher']
			df_main['dsalesvo_sum'] = df1['dsalesvo']
			df_main['year'] = [year]*len(df_main)
			df_main['dstateco'] = [stateco]*len(df_main)

			total_rows_saved += len(df_main)
			df_main.to_csv(output_dir+'%s_%s.csv' %(year, stateco), index=False)

		year = year - 1

	print('total rows saved '+total_rows_saved)
	print('done with search, now combine all files')
	
	## combine all files to 1 big one
	df_main = pd.DataFrame()

	for file in os.listdir(output_dir):
		if '.DS_store' not in file and '.csv' in file:
			df = pd.read_csv(d+file)
			df_main = df_main.append(df, ignore_index=True)

	## reorder columns
	df_main = df_main[['year', 'dstateco', 'dprimsi', 'demplher_mean', 'dsalesvo_mean', 'demplher_sum', 'dsalesvo_sum']] 
	df_main.to_csv(output_dir+'stateco_sic_year_means.csv', index=False)





def sums_means_python(output_dir):
	'''
	above versions using sql were taking forever, and I realized I already have the data
	so I will use the existing data and parse it all in python
	'''
	input_dir = '/home/research/projects/dunn-bradstreet/sql_output/'
	df_master = pd.DataFrame()
	total_rows_saved = 0

	for file in os.listdir(input_dir):
		if 'emp_sales' not in file:
			continue

		df = pd.read_csv(input_dir+file)
		year = file[10:14]
		print(file, len(df))

		if len(df) == 0:
			continue

		df = df[['dstateco', 'dprimsi', 'demplher', 'dsalesvo']]
		df = df.fillna(0)

		df0 = df.groupby(['dstateco', 'dprimsi'])['demplher', 'dsalesvo'].mean()
		df0 = df0.reset_index()
		df_main = df0.rename(columns={"demplher": "demplher_mean", "dsalesvo": "dsalesvo_mean"})

		df1 = df.groupby(['dstateco', 'dprimsi'])['demplher', 'dsalesvo'].sum()
		df1 = df1.reset_index()

		df_main['demplher_sum'] = df1['demplher']
		df_main['dsalesvo_sum'] = df1['dsalesvo']
		df_main['year'] = [int(year)]*len(df_main)

		total_rows_saved += len(df_main)
		print('total rows saved %s' %total_rows_saved)

		df_master = df_master.append(df_main)


	df_master = df_master[['year', 'dstateco', 'dprimsi', 'demplher_mean', 'dsalesvo_mean',
							'demplher_sum', 'dsalesvo_sum']] 
	df_master.to_csv(output_dir+'sums_means_all.csv', index = False)



if __name__ == '__main__':
	### only need below for using sql
	# year = datetime.datetime.today().year
	# year = year - 2 ## start in 2015
	# engine = create_engine('postgresql://mjaron@localhost:5432/dun_bradstreet')
	output_dir = './sql_output/sums_means/'

	print('starting')
	sums_means_python(output_dir)
	# sums_means(year, engine, output_dir)
	# sums_means_sql(year, engine, output_dir)
	print('done with sums and means')
	# years(year, engine, output_dir)
	print('done with everything')
