from Famcy._util_._fwidget import FamcyWidget
from Famcy._util_._flayout import *
import Famcy

class FCard(FamcyWidget):
	"""
	This represents the card-like block
	that can be laid onto the Famcy console
	layout. 
	"""
	def __init__(self, permission_level=0, 
			layout_mode=FamcyLayoutMode.recommend):
		super(FCard, self).__init__(permission_level)

		self.layout = FamcyLayout(layout_mode)
		self._check_rep()

	def _check_rep(self):
		"""
		Check rep invariant:
			- Famcy layout in bound
		"""
		pass

	# Functions that can be overwritten
	# ---------------------------------
	def render_inner(self):
		"""
		This is the function to 
		render the layout and
		apply style. 
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