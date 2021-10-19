import enum
import Famcy

class FamcyLayoutType(enum.IntEnum):
	auto = 0
	fixed = 1

class FamcyLayout:
	"""
	This represents the layout scheme
	that the famcy console would need
	to obtain. 

	AF(layout_mode): Represent a layout with mode
	layout_mode

	Rep:
		* content: a list of list of [card, start row, 
			start col, height(num row), width(num col)]

	Method:
		* setMode(layout mode)
		* addCard(card, start row, start col, height(num row), width(num col))
		* render()
	"""
	def __init__(self, layout_mode):
		self.mode = layout_mode
		self.content = []
		self._check_rep()

	def _check_rep(self):
		"""
		Rep Invariant
		"""
		pass

	def setMode(layout_mode):
		"""
		This is the method to set the
		layout mode of the famcy layout. 
		"""
		self.mode = layout_mode



