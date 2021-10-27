import Famcy

class UpdateBlockHtml(Famcy.FamcyResponse):
	"""
	This is the response to update a specific
	part of the famcy widget
	"""
	def __init__(self, target=None):
		super(UpdateBlockHtml, self).__init__(target=target)

	def response(self, sijax_response):
		sijax_response.html('#'+self.target.id, self.target.render_inner())
		sijax_response.script(self.finish_loading_script)