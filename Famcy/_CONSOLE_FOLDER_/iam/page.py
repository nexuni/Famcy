import Famcy

style = Famcy.LoginStyle()

class CustomLoginManager(Famcy.FamcyLogin):
	def __init__(self, always_remember=True):
		super(CustomLoginManager, self).__init__(always_remember=always_remember)

	def login(self, user):
		self.prelogin(user)
		# info_dict = Famcy.FManager.http_client.
		# Authenticate
		self.postlogin(self, user, info_dict):

	def load_famcy_user(self, user_id):
		# info_dict = Famcy.FManager.http_client.
		self.postlogin(Famcy.FamcyUser(), info_dict)

	def prelogin(self, user):
		pass

	def postlogin(self, user, user_info_dict):
		user.id = user_info_dict["user_id"]
		user.phone_num = user_info_dict["user_phone"]
		user.name = user_info_dict["username"] if user_info_dict["username"] != "" else Famcy.FManager.get("default_name", "")
		user.profile_pic_url = user_info_dict["profile_pic_url"] if user_info_dict["profile_pic_url"] != "" else Famcy.FManager.get("default_profile_pic_url", "")

class LoginPage(Famcy.FamcyPage):
	def __init__(self):
		super(LoginPage, self).__init__("/iam/login", style)
		self.main_form = self.login_form()

	def login_form(self):
		pass

CustomLoginManager().register()
login = LoginPage()
login.register()

# -------- Logout Part Below -------------
#
class LogoutPage(Famcy.FamcyPage):
	def __init__(self):
		super(LogoutPage, self).__init__("/logout", style)
	def render(self):
		logout_user()
		return redirect(url_for('main.'+login.id))

LogoutPage().register()
