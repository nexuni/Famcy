import Famcy

class UpdateTabHtml(Famcy.FamcyResponse):
	"""
	This is the response to update the entire page (Tab)
	Make sure self.target is a fpage
	"""
	def __init__(self):
		super(UpdateTabHtml, self).__init__(self)

	def response(self, sijax_response):
		sijax_response.html('#content_section', self.target.render_inner())
		sijax_response.script(self.target.header_script)
		sijax_response.script(self.finish_loading_script)