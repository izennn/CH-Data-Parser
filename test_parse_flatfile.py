import unittest
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
					"filename": "./specs/zerowidthformat.csv"
				},
				"expected": [
					Spec("name", 10, "str"),
					Spec("empty", 0, "str"),
					Spec("valid", 1, "bool")
				]
			},
			{
				"input": {
					"filename": "./specs/fileformat1.csv"
				},
				"expected": [
					Spec("name", 10, "str"),
					Spec("valid", 1, "bool"),
					Spec("count", 3, "int")
				]
			}
		]

		for test in tests:
			ff = open(test["input"]["filename"])
			result = get_spec_list(ff)
			ff.close()
			self.assertEqual(result, test["expected"])

class TestParseFile(unittest.TestCase):
	def test_normal_parse_file(self):
		tests = [
			{
				"input": {
					"datafile": "./data/zerowidthformat_2021-06-18.txt",
					"specfile": "./specs/zerowidthformat.csv"
				},
				"expected": [{'name': 'Foonyor', 'empty': '', 'valid': True}, {'name': 'Barzane', 'empty': '', 'valid': False}, {'name': 'Quuxitude', 'empty': '', 'valid': True}]
			},
			{
				"input": {
					"datafile": "./data/fileformat1_2007-10-15.txt",
					"specfile": "./specs/fileformat1.csv"
				},
				"expected": [{'name': 'Foonyor', 'valid': True, 'count': 1}, {'name': 'Barzane', 'valid': False, 'count': -12}, {'name': 'Quuxitude', 'valid': True, 'count': 103}]
			}
		]

		for test in tests:
			datafilename = test["input"]["datafile"]
			specfilename = test["input"]["specfile"]
			result = parse_flatfile(datafilename, specfilename)
			self.assertEqual(result, test["expected"])

	def test_parse_file_width_invalid_dataline(self):
		tests = [
			{
				"input": {
					"datafile": "./data/wronglengthdataformat_2021-06-18.txt",
					"specfile": "./specs/wronglengthdataformat.csv"
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
			datafilename = test["input"]["datafile"]
			specfilename = test["input"]["specfile"]
			result = parse_flatfile(datafilename, specfilename)
			self.assertEqual(result, test["expected"])

if __name__ == '__main__':
	unittest.main()