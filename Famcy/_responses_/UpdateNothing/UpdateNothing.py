import Famcy

class UpdateNothing(Famcy.FamcyResponse):
	def __init__(self):
		super(UpdateNothing, self).__init__(self)

	def response(self, sijax_response):
		pass