from Famcy._util_._fwidget import FamcyWidget
from Famcy._util_._flayout import *
import Famcy

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
			layout_mode=FamcyLayoutMode.recommend):

		super(FPage, self).__init__(permission_level)
		self.route = route
		self.style = style

		self.layout = FamcyLayout(layout_mode)
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
		content_data = super(FPage, self).render()
		return self.style.render(self.header_script, content_data)

	# Functions that can be overwritten
	# ---------------------------------
	def render_inner(self):
		"""
		This is the function to 
		render the layout. 
		"""
		return self.layout.render()

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

