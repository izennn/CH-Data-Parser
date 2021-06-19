from dataclasses import dataclass

@dataclass
class Spec:
	name: str
	width: int
	type: str

	def __init__(self, name: str, width: int, type: str):
		self.name = name
		self.width = width
		self.type = type

	def get_width(self):
		return self.width

	def get_name(self):
		return self.name

	def set_name(self, new_name: str):
		self.name = new_name

	def get_type(self):
		return self.type