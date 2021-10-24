import abc
import json
import Famcy
from Famcy._util_._fthread import *

class FamcyWidget(metaclass=abc.ABCMeta):
	"""
	This represents the widget interface for
	all Famcy visual objects to follow. 

	Rep:
		* permission: FamcyPermissions. Represent
		the allowed access of the user to this page. 

	Interface:
		* render(): render the page
		* register(): register the page to the Famcy env
		* preload(): action before the rendering
		* postload(): actions after the rendering
	"""	
	def __init__(self, permission_level=0):
		self.id = str(id(self))
		self.name = ""
		self.action = ""
		self.parent = None
		self.children = []
		self.configs = {}

		# Header script
		self.header_script = ""
		self.js_after_func_dict = {} # post js script input
		self.js_after_func_name = "" # post js script function name

		self.permission = Famcy.FamcyPermissions(permission_level)

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
		# self.permission.verify(Famcy.FManager["CurrentUser"])
		self.preload()
		render_data = self.render_inner()
		render_data += '<script>' + self.js_after_func_name + '("' + self.id + '", ' + json.dumps(self.js_after_func_dict) + ')</script>'
		# Set daemon to true to ensure thread dies when main thread dies
		post_thread = FamcyThread(target=self.postload, daemon=True)
		post_thread.start()
		return render_data

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