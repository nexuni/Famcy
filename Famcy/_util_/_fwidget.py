import abc
import json
import Famcy
from Famcy._util_._fthread import *
from Famcy._util_._fsubmission import *

class FamcyWidget(metaclass=abc.ABCMeta):
	"""
	This represents the widget interface for
	all Famcy visual objects to follow. 

	Rep:
		* id, name, etc.

	Interface:
		* render(): render the page
		* register(): register the page to the Famcy env
		* preload(): action before the rendering
		* postload(): actions after the rendering
	"""	
	def __init__(self):
		self.id = "famcy"+str(id(self))
		self.name = "famcy_name"+str(id(self))
		self.action = ""
		self.loader = False
		self.parent = None
		self.clickable = False
		self.configs = {}

		# Header script
		self.header_script = ""
		self.js_after_func_dict = {} # post js script input
		self.js_after_func_name = "" # post js script function name

		# Submission related
		self.submission_obj = FSubmission(self)
		self.post_submission_js = ""

	def render(self):
		"""
		The main render flow is as
		follow. 
		1. Check permission
		2. preload function
		3. render inner
		4. start post load thread
		5. return render inner stuffs
		"""
		self.preload()
		render_data = self.render_inner()
		render_data += '<script>' + self.js_after_func_name + '("' + self.id + '", ' + json.dumps(self.js_after_func_dict) + ')</script>'

		# Set daemon to true to ensure thread dies when main thread dies
		post_thread = FamcyThread(target=self.postload, daemon=True)
		post_thread.start()
		return render_data

	def connect(self, submission_func, target=None):
		"""
		This is the function to setup the
		submission object type. 
		"""
		self.clickable = True
		self.submission_obj.func = submission_func
		self.submission_obj.origin = self
		self.submission_obj.target = target if target else self

	def disconnect(self):
		self.clickable = False
		self.submission_obj.func = lambda *a, **k: None
		self.submission_obj.origin = self
		self.submission_obj.target = self

	@abc.abstractmethod
	def render_inner(self):
		"""
		This is the customizable inner render
		function for famcy page. 
		"""
		pass
		
	@abc.abstractmethod
	def preload(self):
		"""
		This is the preload function
		that should be executed before 
		the inner render function. 
		"""
		pass

	@abc.abstractmethod
	def postload(self):
		"""
		After the page is rendered, 
		apply async post load function. 
		"""
		pass