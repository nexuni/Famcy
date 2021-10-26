from Famcy._util_._fwidget import FamcyWidget
from Famcy._util_._flayout import *
from Famcy._util_._fsubmission import *
import Famcy

class FCard(FamcyWidget):
	"""
	This represents the card-like block
	that can be laid onto the Famcy console
	layout. 
	"""
	def __init__(self, layout_mode=FLayoutMode.recommend):
		super(FCard, self).__init__()

		self.title = ""
		self.layout = FamcyLayout(self, layout_mode)
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
		header_script, content = self.layout.render()
		if header_script not in self.header_script:
			self.header_script += header_script
		title = '<div class="title_holder"><h2 class="section_title">' + self.title + '</h2></div>' if self.title != "" else ""

		return """
		<div class="inner_section" id="{0}">
			{1}

			<div class="inner_section_content">
				{2}
			</div>
		</div>
		""".format(self.id, title, content)

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