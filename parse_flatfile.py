import sys
from typing import List, T

from utils import convert_string_to_type, get_spec_list
from validators import is_valid_input

'''
@param dataline: line of data from data file
@param spec_list: list of Spec objects, describes how to parse dataline
@return object for this line of data
'''
def get_data_object(idx, dataline, spec_list):
	obj = {}
	dataline_idx = 0

	total_width = 0
	for spec in spec_list:
		total_width += spec.get_width()
	if len(dataline) != total_width:
		print("Improper formatting on line {} in data file".format(idx + 1))
		return None

	for spec in spec_list:
		data_width = spec.get_width()
		data_in_string = dataline[dataline_idx:dataline_idx + data_width]
		dataline_idx += data_width
		value = convert_string_to_type(data_in_string, spec.get_type())
		obj[spec.get_name()] = value
	return obj

def parse_flatfile(datafilename: str, formatfilename: str) -> List[T]:
	# instantiate return value
	output = []

	# try opening the files
	try:
		ff = open(formatfilename)
	except IOError as e:
		print("I/O error {}: {}".format(e.strerror, formatfilename))
		sys.exit()
	try:
		df = open(datafilename)
	except IOError as e:
		print("I/O error {}: {}".format(e.strerror, datafilename))
		sys.exit()

	
	# check inputs
	ok, err_msg = is_valid_input(datafilename, formatfilename)
	if not ok:
		print(err_msg)
		sys.exit()

	# get specs
	spec_list = get_spec_list(ff)
			
	# for each data line, extract data object
	for idx, data_line in enumerate(df):
		data_line = data_line.strip()
		data_obj = get_data_object(idx, data_line, spec_list)
		if data_obj != None:
			output.append(data_obj)

	ff.close()
	df.close()

	return output