from Famcy._util_._fwidget import FamcyWidget
from Famcy._util_._flayout import *
from Famcy._util_._fsubmission import *
from Famcy._util_._fpermissions import *
from Famcy._util_._fthread import *
from flask import g, Response, request
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
			background_thread=False, background_freq=0.5):

		super(FPage, self).__init__()
		self.route = route
		self.style = style
		self.layout = FamcyLayout(self, layout_mode)
		self.permission = FPermissions(permission_level)
		self.background_thread_flag = background_thread
		self.background_freq = background_freq

		self.init_page()

		if self.background_thread_flag:
			self.sijax_response = None
			
			# Check loop correctness
			assert getattr(self, "background_thread_inner", None), "Must implement background_thread_inner"
			self.bthread = FamcyThread(target=self.background_thread_loop, daemon=True)
			self.bthread.start()

		self._check_rep()

	def init_page(self):
		self.body = Famcy.ELEMENT()

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

		if self.background_thread_flag:
			bg_func = lambda: self.background_generator_loop()
			bg_func.__name__ = "bgloop_" + self.id

			if self.permission.required_login():
				# Register the page render to the main blueprint
				Famcy.FManager["MainBlueprint"].route(self.route+"/bgloop")(login_required(bg_func))
			else:
				Famcy.FManager["MainBlueprint"].route(self.route+"/bgloop")(bg_func)
		

	def render(self, *args, **kwargs):
		"""
		This is the main render function, i.e.
		the flask route function top level. 
		"""
		# First setup the submission handler

		form_init_js = ''
		end_script = ''
		upload_list = self.find_class(self, "upload_form")
		for _item in upload_list:
			form_init_js += g.sijax.register_upload_callback(_item.id, FSubmissionSijaxHandler.upload_form_handler)

		if g.sijax.is_sijax_request:
			g.sijax.register_object(FSubmissionSijaxHandler)

			return g.sijax.process_request()

		if not self.permission.verify(Famcy.FManager["CurrentUser"]):
			content_data = "<h1>You are not authorized to view this page!</h1>"
		else:
			# Render all content
			self.body = super(FPage, self).render()
			content_data = self.body.render_inner()
			end_script = self.body.render_script()
			for temp, _ in self.layout.staticContent:
				end_script += temp.body.render_script()

		# Apply style at the end
		return self.style.render(self.header_script, content_data, background_flag=self.background_thread_flag, route=self.route, time=int(1/self.background_freq)*1000, form_init_js=form_init_js, end_script=end_script)

	def background_generator_loop(self):
		def generate():
			try:
				baction = Famcy.FamcyBackgroundQueue.pop()
				yield json.dumps({"indicator": True, "message": baction.tojson()})

			except Exception as e:
				yield json.dumps({"indicator": False, "message": str(e)})

		return Response(generate(), mimetype='text/plain')

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

	# Functions that can be overwritten
	# ---------------------------------
	def render_inner(self):
		"""
		This is the function to 
		render the layout. 
		"""
		header_script, self.body = self.layout.render()

		if header_script not in self.header_script:
			self.header_script += header_script
		
		return self.body

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

