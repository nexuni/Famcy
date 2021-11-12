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
		self.body = None
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


		self.body = Famcy.div()
		self.body["id"] = self.id
		self.body["className"] = "inner_section"

		if self.title != "":
			title = Famcy.div()
			title["className"] = "title_holder"

			h2_temp = Famcy.h2()
			h2_temp["className"] = "section_title"
			h2_temp.innerHTML = self.title

			title.addElement(h2_temp)
			self.body.addElement(title)

		inner_section = Famcy.div()
		inner_section["className"] = "inner_section_content"
		inner_section.innerHTML = content

		self.body.addElement(inner_section)

		return self.body.render_inner()

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