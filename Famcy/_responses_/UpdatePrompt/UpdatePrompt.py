import Famcy

class UpdatePrompt(Famcy.FamcyResponse):
	"""
	This is the response to update the entire page (Tab)
	Make sure self.target is a fpage
	"""
	def __init__(self, extra_script=None, target=None):
		super(UpdatePrompt, self).__init__(target=target)
		self.extra_script = extra_script

	def response(self, sijax_response):
		if self.target:
			print("UpdatePrompt")
			# update body html
			_ = self.target.render_inner()
			
			# inner_html = self.run_all_script_tag(self.target.body.render_inner(), sijax_response)
			print("self.target.body.render_inner(): ", self.target.body.render_inner())
			sijax_response.html_append('#root', '<div id="prompt_holder">' + self.target.body.render_inner() + '</div>')
			sijax_response.script(self.extra_script)
			sijax_response.script(self.finish_loading_script)