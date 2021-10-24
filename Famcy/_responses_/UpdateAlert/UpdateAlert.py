import Famcy

class UpdateAlert(Famcy.FamcyResponse):
	def __init__(self):
		super(UpdateAlert, self).__init__(self)

	def generate_alert(info_dict, form_id):
		inner_text = '''
		<div class="alert %s" id="alert_msg_%s" role="alert">
			%s
		</div>
		''' % (info_dict["alert_type"], form_id, info_dict["alert_message"])

		extra_script = '''
		$("#alert_msg_%s").fadeTo(2000, 500).slideUp(500, function(){
			$("#alert_msg_%s").slideUp(500);
			$("#alert_msg_%s").remove();
		});
		''' % (form_id, form_id, form_id)

		return inner_text, extra_script, info_dict["target_alert"]

	def response(self, sijax_response):
		inner_text, extra_script, target_alert = generate_alert(info_dict, form_id)

		block_id = target_alert if target_alert else block_id

		if info_dict["alert_position"] == "append":
			sijax_response.html_append('#'+block_id, inner_text)
		else:
			sijax_response.html_prepend('#'+block_id, inner_text)

		sijax_response.script(extra_script)
		sijax_response.script("$('#loading_holder').css('display','none');")