import sys

from error import InputError
from parse_flatfile import parse_flatfile

if __name__ == '__main__':
	if len(sys.argv) != 3:
		raise InputError("Wrong number of arguments provided")

	datafilename = sys.argv[1]
	specfilename = sys.argv[2]
	output = parse_flatfile(datafilename, specfilename)
	print(output)
