import abc
import json
from flask import session
import Famcy
from Famcy._util_._fthread import *
from Famcy._util_._fsubmission import *
from multiprocessing import Process
from multiprocessing.process import AuthenticationString
import multiprocessing as mp

import pickle

class My_class(Process):
	def __init__(self, target=None, args=None):
		super(My_class, self).__init__(target=target, args=args)
		print("Object", self, "created.")

	def run(self):
		print("Object", self, "process started.")

	def __getstate__(self):
		"""called when pickling - this hack allows subprocesses to 
		   be spawned without the AuthenticationString raising an error"""
		state = self.__dict__.copy()
		conf = state['_config']
		if 'authkey' in conf: 
			#del conf['authkey']
			conf['authkey'] = bytes(conf['authkey'])
		return state

	def __setstate__(self, state):
		"""for unpickling"""
		state['_config']['authkey'] = AuthenticationString(state['_config']['authkey'])
		self.__dict__.update(state)

def add_to_table(key, obj):
	pass

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
		self.body = None
		self.clickable = False
		self.configs = {}
		self.attributes = {}

		# Header script
		self.header_script = ""
		self.js_after_func_dict = {} # post js script input
		self.js_after_func_name = "" # post js script function name

		# Style related
		self.css_style_dict = {}

		# Submission related
		self.submission_obj = FSubmission(self)
		self.submission_obj_key = self.id
		self.post_submission_js = ""

		Famcy.SubmissionObjectTable[self.submission_obj_key] = self.submission_obj
		# p = My_class(target=add_to_table, args=(Famcy.SubmissionObjectTable, self.submission_obj_key, self.submission_obj))
		# Famcy.SubmissionObjectProcess.append(p)
		# p.start()
		
		# p = mp.Pool()
		# p.apply_async(add_to_table, args=(self.submission_obj_key, self.submission_obj))
		# p.close()
		# p.join()

		# session["SubmissionObjectTable"][self.submission_obj_key] = self.submission_obj

	def __setitem__(self, key, value):
		self.attributes[key] = value

	def __getitem__(self, key):
		return self.attributes[key]

	def __delitem__(self, item):
		if item in self.attributes.keys():
			del self.attributes[item]

	def find_parent(self, item, className):
		if not type(item.parent).__name__ == className:
			if item.parent:
				return self.find_parent(item.parent, className)
			else:
				return item.parent
		else:
			return item.parent

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