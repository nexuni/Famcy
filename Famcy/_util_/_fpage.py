from Famcy._util_._fwidget import FamcyWidget
from Famcy._util_._flayout import *
from Famcy._util_._fsubmission import *
from flask import g
import Famcy
import time
import abc

class FPage(FamcyWidget):
	"""
	This page represents each of the page 
	on Famcy. It handles rendering, layout, 
	submission, etc... providing an overview
	of everything that happens in the page. 

	Routing of the page is defined by the folder
	/ subfolders file structure. 

	Abstraction:
		AF(route, style) = The page that is at url route and 
		apply css / js style of style
	
	Rep:
		* layout: FamcyLayout. Represent the layout
		of Famcy cards of the page. 
		* permission: FamcyPermissions. Represent
		the allowed access of the user to this page. 

	Interface:
		* render(): render the page
		* register(): register the page to the Famcy env
		* preload(): action before the rendering
		* postload(): actions after the rendering
	"""	
	def __init__(self, route, style, permission_level=0, 
			layout_mode=FamcyLayoutMode.recommend, 
			background_thread=False, background_freq=0.5, 
			comet_update_freq=0.25):

		super(FPage, self).__init__(permission_level)
		self.route = route
		self.style = style
		self.layout = FamcyLayout(self, layout_mode)
		self.background_thread_flag = background_thread

		if self.background_thread_flag:
			self.comet_update_freq = comet_update_freq
			self.background_freq = background_freq
			self.background_signal = FamcySignal()
			self.sijax_response = None
			# Necessary header script for comet
			self.header_script += '<script type="text/javascript" src="/static/js/sijax/sijax_comet.js"></script>'
			
			# Check loop correctness
			assert getattr(self, "background_thread_inner", None), "Must implement background_thread_inner"
			self.bthread = FamcyThread(target=self.background_thread_loop, daemon=True)
			self.bthread.start()

		self._check_rep()

	def _check_rep(self):
		"""
		Check rep invariant:
			- Famcy layout in bound
			- Permission is not empty, able to 
				access in some way. 
		"""
		pass

	def register(self):
		"""
		This is the function to register 
		the page to the flask route system. 
		"""
		route_func = lambda: self.render()
		route_func.__name__ = self.id

		# Register the page render to the main blueprint
		Famcy.MainBlueprint.route(self.route)(route_func)

	def render(self, *args, **kwargs):
		"""
		This is the main render function, i.e.
		the flask route function top level. 
		"""
		# First setup the submission handler
		if g.sijax.is_sijax_request:
			g.sijax.register_object(FSubmissionSijaxHandler)

			if self.background_thread_flag:
				g.sijax.register_comet_callback('background_work', self.background_main_comet_handler)

			return g.sijax.process_request()

		# Render all content
		content_data = super(FPage, self).render()

		# Apply style at the end
		return self.style.render(self.header_script, content_data, background_flag=self.background_thread_flag)

	def background_thread_loop(self):
		"""
		This is the background thread 
		loop for fpage
		"""
		while True:
			time.sleep(int(1/self.background_freq))

			if not self.sijax_response:
				continue

			self.background_thread_inner(self.sijax_response)
			

	def background_thread_inner(self, sijax_response):
		"""
		This is the background thread
		inner content for fpage. 
		* Input:
			sijax_response: the object that can
			help trigger sijax response
		"""
		pass

	def background_main_comet_handler(self, obj_response):
		"""
		This is the main handler
		for sijax comet plugin
		"""
		while True:
			self.sijax_response = obj_response
			self.background_signal.emit()

			yield self.sijax_response

			time.sleep(int(1/self.comet_update_freq))

	# Functions that can be overwritten
	# ---------------------------------
	def render_inner(self):
		"""
		This is the function to 
		render the layout. 
		"""
		header_script, content_data = self.layout.render()

		if header_script not in self.header_script:
			self.header_script += header_script
			
		for _card, _, _, _, _ in self.layout.content:
			self.header_script += _card.header_script
		
		return content_data

	def preload(self):
		"""
		This is the preload function
		that should be executed before 
		the inner render function. 
		"""
		pass

	def postload(self):
		"""
		After the page is rendered, 
		apply async post load function. 
		"""
		pass

