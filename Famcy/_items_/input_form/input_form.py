import Famcy
import json

class input_form(Famcy.FamcyCard):
	"""
	This is a category of card
	that group all submittable
	blocks together. 
	"""
	def __init__(self, layout_mode=Famcy.FamcyLayoutMode.recommend):
		super(input_form, self).__init__(layout_mode=layout_mode)
		self.configs["method"] = "post"

	def render_inner(self):
		header_script, content_render = self.layout.render()
		if header_script not in self.header_script:
			self.header_script += header_script
		inner_html = """<form id="%s" method="%s" action="%s" onsubmit="return false;">%s</form>
		""" % (self.id, self.configs["method"], self.action, content_render)

		inner_html += """<script type="text/javascript">"""

		for widget, _, _, _, _ in self.layout.content:
			if widget.clickable:
				inner_html += """$('#%s').bind('click', (e) => {

					if (%s) {
						$('#loading_holder').css("display","flex");
					}

					var form_element = document.getElementById('%s')
					var formData = new FormData(form_element)
					var response_dict = {}
					for (var pair of formData.entries()) {
						if (!(pair[0] in response_dict)) {
							response_dict[pair[0]] = [pair[1]]
						}
						else {
							response_dict[pair[0]].push(pair[1])
						}
					}

					var flag = checkform(form_element)
					var token = document.head.querySelector("[name~=csrf-token][content]").content

					Sijax.request('famcy_submission_handler', ['%s', response_dict], { data: { csrf_token: token } });
				});""" % (widget.id, json.dumps(widget.loader), self.id, str(id(widget.submission_obj)))

		inner_html += """</script>"""

		return inner_html
		