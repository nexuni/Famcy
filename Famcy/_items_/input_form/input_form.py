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
		self.init_block()

	def init_block(self):
		self.body = Famcy.form()
		self.body["id"] = self.id
		self.body["method"] = self.configs["method"]
		self.body["action"] = self.action
		self.body["onsubmit"] = "return false;"

	def render_inner(self):
			
		header_script, content_render = self.layout.render()
		if header_script not in self.header_script:
			self.header_script += header_script

		self.body.innerHTML = content_render

		script = Famcy.script()
		inner_html = ""
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
						if (pair[0] !== "btSelectAll") {
							if (!(pair[0] in response_dict)) {
								response_dict[pair[0]] = [pair[1]]
							}
							else {
								response_dict[pair[0]].push(pair[1])
							}
						}
					}

					var flag = checkform(form_element, %s)
					var token = document.head.querySelector("[name~=csrf-token][content]").content
					if (flag) {
						console.log('%s')
						Sijax.request('famcy_submission_handler', ['%s', response_dict], { data: { csrf_token: token } });
					}
				});""" % (widget.id, json.dumps(widget.loader), self.id, str(self.submission_obj_key), str(widget.submission_obj_key), str(widget.submission_obj_key))

		script.innerHTML = inner_html

		return self.body.render_inner() + script.render_inner()
		