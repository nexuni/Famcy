import Famcy

class UpdateJSAlert(Famcy.FamcyResponse):
	def __init__(self, alert_type="alert-primary", alert_message="", alert_position="prepend", extra_script=None, target=None):
		super(UpdateJSAlert, self).__init__(target=target)

		self.alert_type = alert_type		# ("alert-primary" / "alert-secondary" / "alert-success" / "alert-danger" / "alert-warning" / "alert-info" / "alert-light" / "alert-dark")
		self.alert_message = alert_message
		self.alert_position = alert_position
		self.extra_script = extra_script

	def response(self, sijax_response):
		sijax_response.script("alert('"+self.alert_message+"');")
		sijax_response.script(self.extra_script)
		sijax_response.script(self.finish_loading_script)