import Famcy

class RedirectPage(Famcy.FamcyResponse):
	def __init__(self):
		super(RedirectPage, self).__init__(self)

		self.redirect_url = ""

	def response(self, sijax_response):
		if "redirect_url" in self.info_dict.keys():
			self.redirect_url = self.info_dict["redirect_url"]
			sijax_response.redirect(url_for(self.redirect_url))