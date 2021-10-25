import Famcy

class UpdateAlert(Famcy.FamcyResponse):
	def __init__(self, target=None):
		super(UpdateAlert, self).__init__(target=target)

		self.alert_type = ""
		self.alert_message = ""
		self.alert_position = "append"

	def generate_alert():
		self.alert_type = self.info_dict["alert_type"] if "alert_type" in self.info_dict.keys() else self.alert_type
		self.alert_message = self.info_dict["alert_message"] if "alert_message" in self.info_dict.keys() else self.alert_message

		inner_text = '''
		<div class="alert %s" id="alert_msg_%s" role="alert">
			%s
		</div>
		''' % (self.alert_type, self.target.id, self.alert_message)

		extra_script = '''
		$("#alert_msg_%s").fadeTo(2000, 500).slideUp(500, function(){
			$("#alert_msg_%s").slideUp(500);
			$("#alert_msg_%s").remove();
		});
		''' % (self.target.id, self.target.id, self.target.id)

		return inner_text, extra_script

	def response(self, sijax_response):
		inner_text, extra_script = self.generate_alert()

		self.alert_position = self.info_dict["alert_position"] if "alert_position" in self.info_dict.keys() else self.alert_position
		
		if self.alert_position == "append":
			sijax_response.html_append('#'+self.target.id, inner_text)
		else:
			sijax_response.html_prepend('#'+self.target.id, inner_text)

		sijax_response.script(self.target.header_script)
		sijax_response.script(self.finish_loading_script)