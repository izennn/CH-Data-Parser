class Error(Exception):
	'''Base class for exceptions in this module'''
	pass

class InputError(Error):
	'''
	Exception raised for errors in the input.

	Attributes:
		message -- explanation of the error
	'''
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		return self.message

class FileFormatError(Error):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)
	
	def __str__(self):
		return self.message
