import abc
import Famcy

class FamcyPage:
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
	layout = abc.abstractproperty()
	permission = abc.abstractproperty()

	def __init__(self, route, style):
		self.route = route
		self.style = style
		self._check_rep()

	def _check_rep(self):
		"""
		Check rep invariant:
			- Famcy layout in bound
			- Permission is not empty, able to 
				access in some way. 
		"""
		pass

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
		pass

	def register(self):
		"""
		This is the function to register 
		the page to the flask route system. 
		"""
		route_func = lambda: self.render
		route_func.__name__ = id(self)

		# Register the page render to the main blueprint
		Famcy.MainBlueprint.route(self.route)(route_func)

	# Functions that can be overwritten
	# ---------------------------------
	def render_inner(self):
		"""
		This is the customizable inner render
		function for famcy page. 
		"""
		pass

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

