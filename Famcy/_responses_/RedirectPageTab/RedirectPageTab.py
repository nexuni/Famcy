import Famcy

class RedirectPageTab(Famcy.FamcyResponse):
	def __init__(self):
		super(RedirectPageTab, self).__init__(self)

		self.redirect_tab = ""

	def response(self, sijax_response):
		if "redirect_tab" in self.info_dict.keys():
			self.redirect_tab = self.info_dict["redirect_tab"]
			sijax_response.redirect(url_for("main.generate_tab_page", tab=self.redirect_tab))