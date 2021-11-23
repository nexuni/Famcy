from Famcy._util_._fwidget import FamcyWidget
from Famcy._util_._flayout import *
from Famcy._util_._fsubmission import *
from Famcy._util_._fpermissions import *
from Famcy._util_._fthread import *
from flask import g
from flask_login import login_required
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
		* permission: FPermissions. Represent
		the allowed access of the user to this page. 

	Interface:
		* render(): render the page
		* register(): register the page to the Famcy env
		* preload(): action before the rendering
		* postload(): actions after the rendering
	""" 
	def __init__(self, route, style, permission_level=0, 
			layout_mode=FLayoutMode.recommend, 
			background_thread=False, background_freq=0.5, comet_update_freq=0.5):

		super(FPage, self).__init__()
		self.route = route
		self.style = style
		self.layout = FamcyLayout(self, layout_mode)
		self.permission = FPermissions(permission_level)
		self.background_thread_flag = background_thread
		# self.ws = None

		if self.background_thread_flag:
			# self.ws = FamcyWebsocketClient("127.0.0.1", "8000")
			self.comet_update_freq = comet_update_freq
			self.background_freq = background_freq
			self.background_queue = Famcy.FamcyBackgroundQueue
			self.sijax_response = None
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

		if self.permission.required_login():
			# Register the page render to the main blueprint
			Famcy.FManager["Sijax"].route(Famcy.MainBlueprint, self.route)(login_required(route_func))
		else:
			Famcy.FManager["Sijax"].route(Famcy.MainBlueprint, self.route)(route_func)

	def render(self, *args, **kwargs):
		"""
		This is the main render function, i.e.
		the flask route function top level. 
		"""
		# First setup the submission handler
		if g.sijax.is_sijax_request:
			g.sijax.register_object(FSubmissionSijaxHandler)

			# No more comet, not compatible with uwsgi
			if self.background_thread_flag:
			  g.sijax.register_comet_callback('background_work', self.background_main_comet_handler)

			return g.sijax.process_request()

		if not self.permission.verify(Famcy.FManager["CurrentUser"]):
			content_data = "<h1>You are not authorized to view this page!</h1>"
		else:
			# Render all content
			content_data = super(FPage, self).render()

		# Apply style at the end
		return self.style.render(self.header_script, content_data, page_id=self.id, background_flag=self.background_thread_flag)

	def background_thread_loop(self):
		"""
		This is the background thread 
		loop for fpage
		"""
		while True:
			time.sleep(int(1/self.background_freq))
			self.background_thread_inner()

	def background_thread_inner(self):
		"""
		This is the background thread
		inner content for fpage. 
		"""
		pass

	def background_main_comet_handler(self, obj_response, **kwargs):
		"""
		This is the main handler
		for sijax comet plugin
		"""
		while True:
			time.sleep(int(1/self.comet_update_freq))
			self.sijax_response = obj_response
			try:
				baction = self.background_queue.pop()
				responseObj = baction.func(baction, [])
				responseObj.target = responseObj.target if responseObj.target else baction.target
				responseObj.response(self.sijax_response)

			except Exception as e:
				continue

			yield self.sijax_response
			pass

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

