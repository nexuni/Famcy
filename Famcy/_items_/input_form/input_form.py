import Famcy

class input_form(Famcy.FamcyCard):
	def __init__(self):
		self.configs["method"] = "post"

	def render_inner(self):
		content_render = self.layout.render()
		return """<form id="%s" method="%s" action="%s" onsubmit="return false;">%s</form>
        """ % (self.id, self.configs["method"], self.action, content_render)