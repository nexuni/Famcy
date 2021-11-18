import abc
import json
import Famcy

class FElement(metaclass=abc.ABCMeta):
	def __init__(self):
		self.style = {}
		self.classList = []
		self.attributes = {}

		self.innerHTML = ""
		self.html = ""
		self.parentElement = None
		self.children = []

	def __setitem__(self, key, value):
		if key == "className":
			if value not in self.classList:
				self.classList.append(value)
		else:
			self.attributes[key] = value

	def __getitem__(self, key):
		return self.attributes[key]

	def __delitem__(self, item):
		if item in self.attributes.keys():
			del self.attributes[item]

	def addElement(self, child):
		if child not in self.children:
			self.children.append(child)

	def setAttrTag(self):
		"""
		All input should be string
		"""
		return_attr = ""

		_ = ""
		for key, val in self.style.items():
			_ += key + ': ' + val + ';'
		return_attr += ' style="' + _ + '"' if _ != "" else ""

		_ = ""
		for _class in self.classList:
			_ += _class + " "
		return_attr += ' class="' + _[:-1] + '"' if self.classList != [] else ""

		for key, val in self.attributes.items():
			return_attr += ' ' + key + '="' + val + '"'

		return return_attr

	@abc.abstractmethod
	def render_inner(self):
		"""
		This is the customizable inner render
		function for famcy page. 
		"""
		pass