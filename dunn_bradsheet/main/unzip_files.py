import zipfile
import os

def unzip(input_directory, output_directory):
	##directory = '/home/research/datasets/dun-bradstreet/'
	for file_name in os.listdir(input_directory):
		if '.zip' in file_name:
			print(file_name)
			zip_ref = zipfile.ZipFile(input_directory+file_name, 'r')
			zip_ref.extractall(output_directory)
			zip_ref.close()


if __name__ == "__main__":
	input_directory = '/home/research/projects/dunn-bradstreet/'
	output_directory = '/home/mjaron/dunn_bradsheet/'
	unzip(input_directory, output_directory)
