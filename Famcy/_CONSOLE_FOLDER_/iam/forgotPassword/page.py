import Famcy
import json
# from flask import url_for


PAGE_HEADER = {
	"title": ["Famcy 修改密碼"],
	"size": ["login_section"],
	"type": ["input_form"]
}

phone_content = Famcy.input_form.generate_values_content("pureInput")
phone_content.update({
		"type": "pureInput",
		"title": "電話號碼",
		"desc": "",
		"input_type": "number",                               # text / number
		"placeholder": "0900123456",
		"mandatory": True
	})

url_btn_content = Famcy.input_form.generate_values_content("urlBtn")
url_btn_content.update({
		"title": "",
		"desc": "",
		"url": "/iam/login",
		"button_name": "返回登入頁面",
		"style": "link_style",
		"desc": "登入會員"

	})

input_form_content = Famcy.input_form.generate_template_content([phone_content, url_btn_content])
input_form_content.update({
		"main_button_name": ["傳送訊息"], # btn name in same section must not be same
		"action_after_post": "save",                    # (clean / save)
		"main_desc": "",
		"loader": False
	})


def msg_submission(submission_list, **configs):
	print("submission_list: ", submission_list)
	phone_num = submission_list[0][0]

	if phone_num != "":
		send_dict = {
		    "service": "member",
		    "operation": "forget_password", 
		    "user_phone": phone_num
		}

		post_str = Famcy.CLIENT_SERVER.client_post("member_http_url", send_dict, gauth=True)
		post_ind = json.loads(post_str)["indicator"]
		post_msg = json.loads(post_str)["message"]

		print("post_msg: ", post_msg)

		if post_ind:
			msg = "訊息已傳送，請稍待5-10分鐘後重新登入修改密碼"

		else:
			msg = "訊息傳送失敗，請重新再試"

	submission_dict_handler = Famcy.SijaxSubmit("update_alert")
	return submission_dict_handler.return_submit_info(msg=msg)


PAGE_CONTENT = [input_form_content]

PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [msg_submission])