import abc
import json
import Famcy
import time
from flask import session
from Famcy._util_._fthread import *
from Famcy._util_._fsubmission import *
from Famcy._util_._fpermissions import *

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
	id_iter = 0

	def __init__(self, **kwargs):
		# update next id number
		FamcyWidget.next_id()
		self.id = "famcy"+str(FamcyWidget.get_id())
		self.name = "famcy_name"+str(FamcyWidget.get_id())
		self.action = ""
		self.loader = Famcy.FManager["ConsoleConfig"]["DEFAULT_LOADER"]
		self.page_parent = kwargs["page_parent"] if "page_parent" in kwargs.keys() else None
		self.parent = kwargs["parent"] if "parent" in kwargs.keys() else None
		self.body = None
		self.clickable = False
		self.configs = {}
		self.attributes = {}
		self.permission = FPermissions(kwargs["permission"]) if "permission" in kwargs else FPermissions(0)

		# Header script
		self.header_script = ""
		self.js_after_func_dict = {} # post js script input
		self.js_after_func_name = "" # post js script function name

		# Style related
		self.css_style_dict = {}

		# Layout related
		self._layout_loading_flag = False
		self._layout_loading_parent = None

		# Submission related
		self.submission_obj = FSubmission(self)
		self.submission_obj_key = self.id
		self.post_submission_js = ""
		self.submit_value_name = self.name

	@classmethod
	def reset_id(cls):
		cls.id_iter = 0

	@classmethod
	def get_id(cls):
		return cls.id_iter

	@classmethod
	def next_id(cls):
		cls.id_iter += 1

	def __setitem__(self, key, value):
		self.attributes[key] = value

	def __getitem__(self, key):
		return self.attributes[key]

	def __delitem__(self, item):
		if item in self.attributes.keys():
			del self.attributes[item]

	def set_cookie(self, key, value):
		session[key] = value

	def get_cookie(self, key):
		return session.get(key)

	def setGeometry(self, x, y, w, h):
		if self.parent:
			if hasattr(self.parent, "layout"):
				self.parent.body.style["position"] = "relative !important"
				self.parent.layout.addFixedWidget(self, position="absolute", top=str(y)+"px" if isinstance(y, int) else _, left=str(x)+"px" if isinstance(x, int) else _, width=str(w)+"px" if isinstance(w, int) else _, height=str(h)+"px" if isinstance(h, int) else _)
			else:
				print("Widget should be put under a class which contains the attribute FLayout such as FPage or FCard")
		else:
			print("Widget should inherit a parent object")

	def setFixedSize(self, w, h):
		if self.body:
			self.body.style["width"] = str(w)+"px" if isinstance(w, int) else _ + " !important"
			self.body.style["height"] = str(h)+"px" if isinstance(h, int) else _ + " !important"
		else:
			print("Error: self.body is None")

	def find_page_parent(self, item):
		if item.parent:
			return self.find_page_parent(item.parent)
		else:
			return item

	def find_parent(self, item, className, include_self=False):
		if include_self and type(item).__name__ == className:
			return item
		if not type(item.parent).__name__ == className:
			if item.parent:
				return self.find_parent(item.parent, className)
			else:
				return item.parent
		else:
			return item.parent

	def find_class(self, item, className):
		return_list = []
		if hasattr(item, "layout"):
			for _item, _, _, _, _ in item.layout.content:
				if type(_item).__name__ == className:
					return_list.append(_item)
				return_list.extend(self.find_class(_item, className))

			for _item, _ in item.layout.staticContent:
				if type(_item).__name__ == className:
					return_list.append(_item)
				return_list.extend(self.find_class(_item, className))
		return return_list

	def find_all_widget(self, item):
		return_list = []
		if hasattr(item, "layout"):
			for _item, _, _, _, _ in item.layout.content:
				return_list.append(_item)
				return_list.extend(self.find_all_widget(_item))

			for _item, _ in item.layout.staticContent:
				return_list.append(_item)
				return_list.extend(self.find_all_widget(_item))
		return return_list

	def find_obj_by_id(self, item, obj_id):
		if hasattr(item, "layout"):
			for _item, _, _, _, _ in item.layout.content:
				if _item.submission_obj_key == obj_id:
					return _item.submission_obj
				_children = self.find_obj_by_id(_item, obj_id)
				if _children:
					return _children

			for _item, _ in item.layout.staticContent:
				if _item.submission_obj_key == obj_id:
					return _item.submission_obj
				_children = self.find_obj_by_id(_item, obj_id)
				if _children:
					return _children
		return None
		
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

		self.body = self.render_inner()
		if self.js_after_func_name != "" and self.js_after_func_name:
			script = Famcy.script()
			script.innerHTML = self.js_after_func_name + '("' + self.id + '", ' + json.dumps(self.js_after_func_dict) + ')'
			self.body.addElement(script)
		
		# Set daemon to true to ensure thread dies when main thread dies
		post_thread = FamcyThread(target=self.postload, daemon=True)
		post_thread.start()
		return self.body

	def set_submit_value_name(self, key_name):
		self.submit_value_name = key_name

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
		self.submission_obj.func = None
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