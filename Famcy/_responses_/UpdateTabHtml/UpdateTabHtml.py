import Famcy

class UpdateTabHtml(Famcy.FamcyResponse):
	"""
	This is the response to update the entire page (Tab)
	Make sure self.target is a fpage
	"""
	def __init__(self, extra_script=None, target=None):
		super(UpdateTabHtml, self).__init__(target=target)
		self.extra_script = extra_script

	def response(self, sijax_response):
		if self.target:
			# update body html
			_ = self.target.render_inner()
			
			sijax_response.html('#content_section', self.target.body.render_inner())
			self.target.layout.setSijaxLayout(sijax_response)
			sijax_response.script(self.extra_script)
			sijax_response.script(self.finish_loading_script)