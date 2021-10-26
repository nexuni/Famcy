import Famcy

class CustomLoginManager(Famcy.FamcyLogin):
	def __init__(self, always_remember=True):
		super(CustomLoginManager, self).__init__(always_remember=always_remember)

class LoginPage(Famcy.FamcyPage):
	def __init__(self):
		super(LoginPage, self).__init__("/iam/login", style)

CustomLoginManager().register()
login = LoginPage()
login.register()

# ------------
class LogoutPage(Famcy.FamcyPage):
	def __init__(self):
		super(LogoutPage, self).__init__("/logout", style)
	def render(self):
		logout_user()
		return redirect(url_for('main.'+login.id))

class ForgotPasswordPage(Famcy.FamcyPage):
	def __init__(self):
		super(ForgotPasswordPage, self).__init__("/iam/fpw", style)

class ProfilePage(Famcy.FamcyPage):
	def __init__(self):
		super(ProfilePage, self).__init__("/iam/profile", style)

class SignupPage(Famcy.FamcyPage):
	def __init__(self):
		super(SignupPage, self).__init__("/iam/signup", style)



logout_user()
return redirect(url_for('main.home'))


SignupPage().register()
LogoutPage().register()
ForgotPasswordPage().register()
ProfilePage().register()
