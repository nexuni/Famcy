import Famcy

class UpdateTabHtml(Famcy.FamcyResponse):
	"""
	This is the response to update the entire page (Tab)
	Make sure self.target is a fpage
	"""
	def __init__(self, target=None):
		super(UpdateTabHtml, self).__init__(target=target)

	def response(self, sijax_response):
		sijax_response.html('#content_section', self.target.render_inner())
		sijax_response.script(self.finish_loading_script)