import Famcy

class UpdateRemoveElement(Famcy.FamcyResponse):
	"""
	This is the response to update the entire page (Tab)
	Make sure self.target is a fpage
	"""
	def __init__(self, extra_script=None, target=None):
		super(UpdateRemoveElement, self).__init__(target=target)
		self.extra_script = extra_script

	def response(self, sijax_response):
		sijax_response.remove('#' + self.target.id)
		sijax_response.script(self.extra_script)
		sijax_response.script(self.finish_loading_script)