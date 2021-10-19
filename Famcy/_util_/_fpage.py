import abc

class FamcyPage:
	"""
	This page represents each of the page 
	on Famcy. It handles rendering, layout, 
	submission, etc... providing an overview
	of everything that happens in the page. 

	Routing of the page is defined by the folder
	/ subfolders file structure. 

	Abstraction:
		AF(style) = FamcyPage of css / js style of style
	
	Rep:
		* layout: FamcyLayout. Represent the layout
		of Famcy cards of the page. 
		* permission: FamcyPermissions. Represent
		the allowed access of the user to this page. 

	Interface:
		* render()
		* preload()
		* postload()
	"""	
	layout = abc.abstractproperty()
	permission = abc.abstractproperty()

	def __init__(self, style):
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
		pass

	# Functions that can be overwritten
	# ---------------------------------
	def render_inner(self):
		"""
		Hidden render function that
		calls all layout
		"""
		pass

	def preload(self):
		pass

	def postload(self):
		pass



