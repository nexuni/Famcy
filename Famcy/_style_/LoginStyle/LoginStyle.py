import Famcy
from flask import render_template

class LoginStyle(Famcy.FamcyStyle):
	def __init__(self):
		super(LoginStyle, self).__init__()

		# set default value
		self.title = ""
		self.desc = ""

		self.loader = Famcy.FamcyStyleLoader()
		self.color_theme = Famcy.FamcyColorTheme()

	def setHeadScript(self, title=None, desc=None):
		if title:
			self.title = title
		if desc:
			self.desc = desc

	def render(self, extra_script, content, background_flag=False, route="", time=5000):

		html_header = self.setDashboardHTMLHeader()
		end_js = self.setDashboardJavaScript()
		color_theme = self.color_theme.render()
		load_spinner = self.loader.render()

		body_on_load = "background_loop('" + self.main_url + str(route) + "/bgloop" + "', '" + str(route) + "', " + str(time) + ");console.log('start!')" if background_flag else ""
		return render_template("login.html", load_spinner=load_spinner, color_theme=color_theme, html_header=html_header, content=content, extra_script=extra_script, end_js=end_js, body_on_load=body_on_load)
