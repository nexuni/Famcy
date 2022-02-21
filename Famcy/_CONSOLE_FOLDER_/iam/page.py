import Famcy
import json
import hashlib
from flask import redirect, url_for, request, session

class CustomLoginManager(Famcy.FamcyLogin):
	login_db = []
	def __init__(self, always_remember=True):
		super(CustomLoginManager, self).__init__(always_remember=always_remember)

	def init_login_db(self):
		# self.get_carpark_id() #get location position
		send_dict = {
			"operation": "pull_login_data",
			"area": "DDA"
			# "area": self.carpark_id
		}

		# headers = {
		# 	"walkthrough": "Julia"
		# }

		res = Famcy.FManager.http_client.client_post("login_http_url", send_dict, gauth=True)
		CustomLoginManager.login_db = json.loads(res)["message"]
		return json.loads(res)["indicator"]
		# return True

	def authenticate_user(self, user, password):
		"""
		This is the function to authenticate
		the user info. The input user should
		at least have the id attribute. 
		"""
		if isinstance(CustomLoginManager.login_db, list):
			for member in CustomLoginManager.login_db:
				sha_password = hashlib.sha256(password.encode()).hexdigest()
				if user.name == member["username"] and sha_password == member["password"]:
					return {"indicator": True, "message": member}
		return {"indicator": False, "message": None}

	def get_user_info(self, user):
		for member in CustomLoginManager.login_db:
			if user.name == member["username"]:
				self.load_user_info(user, member)
				return member
		return None

	def login(self, info_list):
		"""
		This is the main login function
		to process user input and login
		user to famcy and return login status
		"""
		user = Famcy.FamcyUser()
		user.id = info_list[0][0]
		user.name = info_list[0][0]
		user.password = info_list[1][0]
		res_dict = self.authenticate_user(user, user.password)
		if res_dict["indicator"]:
			self.load_user_info(user, res_dict["message"])
			return self.login_famcy_user(user)
		else:
			return False

	def load_famcy_user(self, user_id):
		user = Famcy.FamcyUser()
		user.id = user_id
		user.name = user_id
		info_dict = self.get_user_info(user)
		return user

	def load_user_info(self, user, user_info_dict):
		user.level = user_info_dict["permission"]
		user.name = user_info_dict["username"] if user_info_dict["username"] != "" else Famcy.FManager.get("default_name", "")
		user.profile_pic_url = ""

CustomLoginManager().register()

class LoginPage(Famcy.FamcyPage):
	def __init__(self):
		super(LoginPage, self).__init__()
		self.main_form = self.login_form()
		self.layout.addWidget(self.main_form, 0, 0)

	def login_form(self):
		login_input_form = Famcy.input_form()
		login_input_form.loader = True

		alert_content = Famcy.displayParagraph()
		if session.get('login_permission'):
			alert_content.update({
				"content": "",
				"title": session.get('login_permission')
			})
			session["login_permission"] = None

		else:
			alert_content.update({
				"title": "",
				"content": ""
			})

		phone_content = Famcy.pureInput()
		phone_content.update({
				"type": "pureInput",
				"title": "帳號",
				"desc": "",
				"placeholder": "Leo",
				"mandatory": True,
				"action_after_post": "save"
			})
		password_content = Famcy.inputPassword()
		password_content.update({
				"type": "inputPassword",
				"title": "密碼",
				"desc": "",
				"mandatory": True,
				"action_after_post": "save"
			})
		save_info_content = Famcy.singleChoiceRadioInput()
		save_info_content.update({
				"type": "singleChoiceRadioInput",
				"title": "是否記住帳號密碼？",
				"desc": "",
				"mandatory": True,
				"value": ["是", "否"],
				"action_after_post": "save"
			})

		url_btn_content = Famcy.urlBtn()
		url_btn_content.update({
				"title": "是否記住帳號密碼？",
				"desc": "",
				"url": "/iam/forgotPassword",
				"button_name": "簡訊傳送密碼",
				"style": "link_style",
				"desc": "忘記密碼?"
			})

		submission_btn = Famcy.submitBtn()
		submission_btn.update({
			"title": "登入"
		})

		submission_btn.connect(self.login_submit, target=login_input_form)

		login_input_form.layout.addWidget(alert_content, 0, 0)
		login_input_form.layout.addWidget(phone_content, 1, 0)
		login_input_form.layout.addWidget(password_content, 2, 0)
		login_input_form.layout.addWidget(save_info_content, 3, 0)
		login_input_form.layout.addWidget(url_btn_content, 4, 0)
		login_input_form.layout.addWidget(submission_btn, 5, 0)

		return login_input_form

	def login_submit(self, submission_obj, info_list):
		if Famcy.FamcyLoginManager.login(info_list):
			_url = request.args["next"] if "next" in request.args.keys() else "/"+Famcy.FManager["ConsoleConfig"]['main_page']
			response = Famcy.RedirectPage(redirect_url=_url)
		else:
			response = Famcy.UpdateAlert(alert_type="alert-warning", alert_message="登入驗證失敗")
		return response

LoginPage.register("/iam/login", Famcy.LoginStyle())

# -------- Logout Part Below -------------
#
class LogoutPage(Famcy.FamcyPage):
	def __init__(self):
		super(LogoutPage, self).__init__()

	@classmethod
	def render(cls, init_cls=None):
		Famcy.FamcyLoginManager.logout_famcy_user()
		return redirect(url_for("MainBlueprint.famcy_route_func_name_"+Famcy.FManager["ConsoleConfig"]['login_url'].replace("/", "_")))

LogoutPage.register("/logout", Famcy.LoginStyle())

