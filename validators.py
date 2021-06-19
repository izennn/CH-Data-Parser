from typing import Tuple
from datetime import datetime

def has_correct_file_type(filename: str, extension: str) -> bool:
	# given a relative path (filename), return whether
	word_fields = filename.split(".")
	file_extension = "." + word_fields[len(word_fields) - 1]
	return file_extension == extension

def has_matching_format(datafilename: str, specfilename: str) -> bool:
	true_format = specfilename.split(".")[0]
	data_file_name_without_extension = datafilename.split(".")[0]
	data_file_name_fields = data_file_name_without_extension.split("_")

	# Check for matching file formats
	if data_file_name_fields[0] != true_format:
		return False
	return True

'''
Given a data file name, return whether 
1. there is a date contained
2. is the date contained the correct format
e.g. fileformat1_2007-10-15.txt
'''
def has_correct_date_format(datafilename: str, date_format: str) -> Tuple[bool, str]:
	fields = datafilename.split("_")
	if (len(fields) != 2):
		return (False, "Incorrect formatting on data file name, should be filename_date.txt")
	date_string = fields[1]
	date_string = date_string.split(".")[0]

	try:
		datetime.strptime(date_string, date_format)
	except ValueError:
		return (False, "This is the incorrect date format, it should be {}".format(date_format))

	return (True, None)

'''
- Given data file name, and specs file name, make sure:
	1. datafilename has correct file type (.txt)
	2. specfilename has correct file type (.csv)
	3. both share the same format
	4. datafilename is format_date.txt
- Remember, the datafilename & specfilename are both relative paths
'''
def is_valid_input(datafilename: str, specfilename: str) -> Tuple[bool, str]:
	# make sure both files have proper extensions
	wordfields = datafilename.split("/")
	strict_datafile_name = wordfields[len(wordfields) - 1]
	if not has_correct_file_type(strict_datafile_name, ".txt"):
		return (False, f"Expected .txt file extension for {datafilename}")

	date_format = "%Y-%m-%d"
	ok, err = has_correct_date_format(strict_datafile_name, date_format)
	if not ok:
		return (False, err)

	wordfields = specfilename.split("/")
	strict_specfile_name = wordfields[len(wordfields) - 1]
	if not has_correct_file_type(strict_specfile_name, ".csv"):
		return (False, f"Expected .csv file extension for {specfilename}")

	# make sure both files have the same fileformat	
	if not has_matching_format(strict_datafile_name, strict_specfile_name):
		return (False, f"Mismatching file formats between {strict_datafile_name} and {strict_specfile_name}")

	return (True, None)
