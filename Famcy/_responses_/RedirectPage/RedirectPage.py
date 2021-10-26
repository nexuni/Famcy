import Famcy

class RedirectPage(Famcy.FamcyResponse):
	def __init__(self, target=None):
		super(RedirectPage, self).__init__(target=target)

		self.redirect_url = ""

	def response(self, sijax_response):
		if "redirect_url" in self.info_dict.keys():
			self.redirect_url = self.info_dict["redirect_url"]
			sijax_response.redirect(self.redirect_url)