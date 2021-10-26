import Famcy

style = Famcy.LoginStyle()

class CustomLoginManager(Famcy.FamcyLogin):
	def __init__(self, always_remember=True):
		super(CustomLoginManager, self).__init__(always_remember=always_remember)

	def login(self, info_list):
		"""
		This is the main login function
		to process user input and login
		user to famcy and return login status
		"""
		self.prelogin(user)
		# info_dict = Famcy.FManager.http_client.
		# Authenticate
		self.postlogin(self, user, info_dict)

	def load_famcy_user(self, user_id):
		# info_dict = Famcy.FManager.http_client.
		# self.postlogin(Famcy.FamcyUser(), info_dict)
		pass

	def prelogin(self, user):
		pass

	def postlogin(self, user, user_info_dict):
		user.id = user_info_dict["user_id"]
		user.level = user_info_dict["membership_level"]
		user.phone_num = user_info_dict["user_phone"]
		user.name = user_info_dict["username"] if user_info_dict["username"] != "" else Famcy.FManager.get("default_name", "")
		user.profile_pic_url = user_info_dict["profile_pic_url"] if user_info_dict["profile_pic_url"] != "" else Famcy.FManager.get("default_profile_pic_url", "")

class LoginPage(Famcy.FamcyPage):
	def __init__(self):
		super(LoginPage, self).__init__("/iam/login", style)
		self.main_form = self.login_form()
		self.layout.addWidget(self.main_form, 0, 0)

	def login_form(self):
		login_input_form = Famcy.input_form()
		login_input_form.loader = True

		phone_content = Famcy.pureInput()
		phone_content.update({
		        "type": "pureInput",
		        "title": "帳號(電話號碼)",
		        "desc": "",
		        "input_type": "number",
		        "placeholder": "0900123456",
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

		login_input_form.layout.addWidget(phone_content, 0, 0)
		login_input_form.layout.addWidget(password_content, 1, 0)
		login_input_form.layout.addWidget(save_info_content, 2, 0)
		login_input_form.layout.addWidget(url_btn_content, 3, 0)
		login_input_form.layout.addWidget(submission_btn, 4, 0)

		return login_input_form

	def login_submit(self, submission_obj, info_list):
		if Famcy.FamcyLoginManger.login(info_list):
			response = Famcy.RedirectPage()
			response.info_dict = {"redirect_url": "/"}
		else:
			response = Famcy.UpdateAlert()
			response.info_dict = {"alert_type":"alert-warning", "alert_message":"登入驗證失敗", "alert_position":"prepend"}
		return response

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



"""
This is the page definition file for Famcy. 
There are two variables very important, which
defines the page content: PAGE_HEADER and PAGE_CONTENT. 

PAGE_HEADER:
	* title: a list of titles of the sections on the page. It is usually put
		at the top of the section as a header. 
	* size: a list. defines section size. Options include half_inner_section
		and inner_section -> half means share two sections on one page
	* type: list of fblock type of the sections on the page. This should match the
		defined fblock name. 

PAGE_CONTENT:
	* a list of dictionary that defines the fblock sections on the page.  

example:
	PAGE_HEADER = {
	"title": ["Nexuni 員工後台"],
	"size": ["inner_section"],
	"type": ["display"]
}

PAGE_CONTENT = [
	{
		"values": [{
			"type": "displayParagraph",
			"title": "",
			"content": '''
**Nexuni 会社ウェブサイトの案内** 

	1. 希望能讓來到Nexuni的新朋友都能夠快速地學習並瞭解我們工作時會使用到的軟體、程式語言、工具等等。
	2. 作為能力考核的依據
	3. 整合所有公司內部的管理工具，如發票上傳、PO申請、報帳工具、打卡記錄等

快速入門:

	* 點擊總覽 -> 訓練網介紹（可以看到本網頁的所有的內容簡介
	* 點擊相關訓練內容 -> 開始練習
	* 點擊總覽 -> 學習進度裡面的進度報告（可以看到練習的成果）

（網頁內容的版權皆為Nexuni Co. 擁有）
''',
		},{
			"type": "displayTag",
			"title": "測試不知道這是用來幹嘛的Layout",
			"content": "到底Display Tag有什麼不一樣？",
		},
		{
			"type": "displayImage",
			"title": "下面這個解析度也太糟糕了吧",
			"img_name": "test.jpg", # This is gathered from static folder or _images_ user folder
		}]
	}
]
"""
# import Famcy
# import json
# # from flask import url_for


# PAGE_HEADER = {
#     "title": ["Famcy 登入"],
#     "size": ["login_section"],
#     "type": ["input_form"]
# }

# phone_content = Famcy.input_form.generate_values_content("pureInput")
# phone_content.update({
#         "type": "pureInput",
#         "title": "帳號(電話號碼)",
#         "desc": "",
#         "input_type": "number",                               # text / number
#         "placeholder": "0900123456",
#         "mandatory": True
#     })
# password_content = Famcy.input_form.generate_values_content("inputPassword")
# password_content.update({
#         "type": "inputPassword",
#         "title": "密碼",
#         "desc": "",
#         "mandatory": True
#     })
# save_info_content = Famcy.input_form.generate_values_content("singleChoiceRadioInput")
# save_info_content.update({
#         "type": "singleChoiceRadioInput",
#         "title": "是否記住帳號密碼？",
#         "desc": "",
#         "mandatory": True,
#         "value": ["是", "否"]
#     })

# url_btn_content = Famcy.input_form.generate_values_content("urlBtn")
# url_btn_content.update({
#         "title": "是否記住帳號密碼？",
#         "desc": "",
#         "url": "/iam/forgotPassword",
#         "button_name": "簡訊傳送密碼",
#         "style": "link_style",
#         "desc": "忘記密碼?"

#     })

# input_form_content = Famcy.input_form.generate_template_content([phone_content, password_content, save_info_content, url_btn_content])
# input_form_content.update({
#         "main_button_name": ["登入"], # btn name in same section must not be same
#         "action_after_post": "save",                    # (clean / save)
#         "main_desc": "",
#         "loader": True
#     })


# def login_submission(submission_list, **configs):
#     phone_num = submission_list[0][0]
#     password = submission_list[1][0]
#     remember = True if submission_list[2][0] == "是" else False

#     login_user = Famcy.user()
#     login_user.id = phone_num                                                     # need a generate id function
#     Famcy.LOGIN_API.update({"user_phone": phone_num})

#     Famcy.login(login_user, remember=remember)

#     submission_dict_handler = Famcy.SijaxSubmit("redirect_page")
#     return submission_dict_handler.return_submit_info(msg='main.home')


# PAGE_CONTENT = [input_form_content]

# PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [login_submission])
