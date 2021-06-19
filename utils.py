import sys

from typing import T
from models import Spec

'''
@param string: the string from data line to evaluate
@param type: the type of value to evaluate to
@return converted string to value
'''
def convert_string_to_type(string: str, type: str) -> T:
	if type == "str":
		return string.strip()
	elif type == "bool":
		return string == "1"
	elif type == "int":
		return int(string)
	
	return string

'''
A valid spec needs to have:
- width > 0
- value is of type "bool", "int", or "str"
'''
def is_valid_spec(spec: Spec) -> bool:
	type = spec.get_type()

	if not (type == "bool" or type == "int" or type == "str"):
		return False
	return True

'''
@param filepointer points to spec file
@returns list of specs parsed from spec file
'''
def get_spec_list(filepointer) -> list: 
	spec_list = []
	spec_order = []
	for i, spec_line in enumerate(filepointer):
		spec_fields = spec_line.strip().split(",")
		if len(spec_fields) != 3:
			#TODO: print error saying spec file improperly formatted
			print("Incorrectly formatted specification file")
			sys.exit()

		if i == 0:
			spec_order = spec_fields
			for i in range(len(spec_order)):
				spec_order[i] = spec_order[i].strip()
		else:
			column_name_index = spec_order.index('"column name"')
			width_index = spec_order.index("width")
			datatype_index = spec_order.index("datatype")
			this_spec = Spec(spec_fields[column_name_index].strip(), int(spec_fields[width_index].strip()), spec_fields[datatype_index].strip())
			if is_valid_spec(this_spec):
				spec_list.append(this_spec)
			else:
				print("Invalid type in line {} in specifications file".format(i + 1))
	return spec_list