import unittest
import os

from utils import get_spec_list
from models import Spec
from validators import has_correct_file_type, has_matching_format, has_correct_date_format
from parse_flatfile import parse_flatfile


class TestFilename(unittest.TestCase):

	def test_has_correct_file_type(self):
		tests = [
			{
				"input": {
					"filename": "samplefile.txt", 
					"filetype": ".txt"
				},
				"expected": True
			},
			{
				"input": {
					"filename": "samplefile.txt", 
					"filetype": ".csv"
				},
				"expected": False
			},
			{
				"input": {
					"filename": "sample.csv.txt",
					"filetype": ".txt"
				},
				"expected": True
			}
		]
		
		for test in tests:
			filename = test["input"]["filename"]
			filetype = test["input"]["filetype"]
			result = has_correct_file_type(filename, filetype)
			self.assertEqual(result, test["expected"])

	def test_has_matching_file_format(self):
		tests = [
			{
				"input": {
					"datafile": "testformat",
					"specfile": "testformat"
				},
				"expected": True
			},
			{
				"input": {
					"datafile": "testformat1.txt",
					"specfile": "testformat2.csv"
				},
				"expected": False
			},
			{
				"input": {
					"datafile": "testformat.csv",
					"specfile": "testformat.csv"
				},
				"expected": True
			},
			{
				"input": {
					"datafile": "",
					"specfile": ""
				},
				"expected": True
			},
			{
				"input": {
					"datafile": "_2021-06-20.txt",
					"specfile": ".csv"
				},
				"expected": True
			},
		]

		for test in tests:
			datafilename = test["input"]["datafile"]
			specfilename = test["input"]["specfile"]
			result = has_matching_format(datafilename, specfilename)
			self.assertEqual(result, test["expected"])

	def test_has_correct_date_format(self):
		tests = [
			{
				"input": {
					"datafilename": "withoutdate",
					"dateformat": "%Y-%m-%d",
				},
				"expected": False
			},
			{
				"input": {
					"datafilename": "withcorrectdate_2021-06-03.txt",
					"dateformat": "%Y-%m-%d",
				},
				"expected": True
			},
			{
				"input": {
					"datafilename": "with-improper-date_21-06-20",
					"dateformat": "%Y-%m-%d",
				},
				"expected": False
			},
			{
				"input": {
					"datafilename": "fileformat_20-06-2021.txt",
					"dateformat": "%Y-%m-%d",
				},
				"expected": False
			},
		]

		for test in tests:
			datafilename = test["input"]["datafilename"]
			dateformat = test["input"]["dateformat"]
			ok, _ = has_correct_date_format(datafilename, dateformat)
			self.assertEqual(ok, test["expected"])

			
class TestSpecFile(unittest.TestCase):

	def test_gets_correct_spec_list_from_spec_file(self):
		tests = [
			{
				"input": {
					"specfilename": "./specs/zerowidthformat.csv"
				},
				"expected": [
					Spec("name", 10, "str"),
					Spec("empty", 0, "str"),
					Spec("valid", 1, "bool")
				]
			},
			{
				"input": {
					"specfilename": "./specs/fileformat1.csv"
				},
				"expected": [
					Spec("name", 10, "str"),
					Spec("valid", 1, "bool"),
					Spec("count", 3, "int")
				]
			}
		]

		for test in tests:
			# get result
			fp = open(test["input"]["specfilename"])
			result = get_spec_list(fp)
			fp.close()
			# remove created files
			# os.remove(specfilename)
			# test result == expected
			self.assertEqual(result, test["expected"])

class TestParseFile(unittest.TestCase):
	
	def test_normal_parse_file(self):
		tests = [
			{
				"input": {
					"datafile": "Foonyor   1  1\nBarzane   0-12\nQuuxitude 1103",
					"specfile": '"column name", width, datatype\nname, 10, str\nvalid, 1, bool\ncount, 3, int'
				},
				"expected": [{'name': 'Foonyor', 'valid': True, 'count': 1}, {'name': 'Barzane', 'valid': False, 'count': -12}, {'name': 'Quuxitude', 'valid': True, 'count': 103}]
			},
			{
				"input": {
					"datafile": "Foonyor   1\nBarzane   0\nQuuxitude 1",
					"specfile": '"column name", width, datatype\nname, 10, str\nempty, 0, str\nvalid, 1, bool'
				},
				"expected": [{'name': 'Foonyor', 'empty': '', 'valid': True}, {'name': 'Barzane', 'empty': '', 'valid': False}, {'name': 'Quuxitude', 'empty': '', 'valid': True}]
			}
		]

		for test in tests:
			datafilename = "./sampleformat2_2021-06-20.txt"
			specfilename = "./sampleformat2.csv"
			# make data file
			datafilepointer = open(datafilename, "w+")
			datafilepointer.write(test["input"]["datafile"])
			datafilepointer.close()
			# make spec file
			specfilepointer = open(specfilename, "w+")
			specfilepointer.write(test["input"]["specfile"])
			specfilepointer.close()
			# run function
			result = parse_flatfile(datafilename, specfilename)
			# remove created files
			os.remove(datafilename)			
			os.remove(specfilename)

			self.assertEqual(result, test["expected"])

	def test_parse_file_width_invalid_dataline(self):
		tests = [
			{
				"input": {
					"datafile": "Foonyor   1  1\nBarzane   0 -12\nQuuxitude 1103\nIzen      0100",
					"specfile": '"column name", width, datatype\nname, 10, str\nvalid, 1, bool\ncount, 3, int'
				},
				"expected": [
					{'name': 'Foonyor', 'valid': True, 'count': 1}, 
					# {'name': 'Barzane', 'valid': False, 'count': -12}, 
					{'name': 'Quuxitude', 'valid': True, 'count': 103},
					{'name': 'Izen', 'valid': False, 'count': 100}
				]
			}	
		]

		for test in tests:
			datafilename = "./wronglengthdataformat_2021-06-18.txt"
			specfilename = "./wronglengthdataformat.csv"
			# make data file
			datafilepointer = open(datafilename, "w+")
			datafilepointer.write(test["input"]["datafile"])
			datafilepointer.close()
			# make spec file
			specfilepointer = open(specfilename, "w+")
			specfilepointer.write(test["input"]["specfile"])
			specfilepointer.close()
			# run function
			result = parse_flatfile(datafilename, specfilename)
			# remove created files
			os.remove(datafilename)			
			os.remove(specfilename)

			self.assertEqual(result, test["expected"])

if __name__ == '__main__':
	unittest.main()