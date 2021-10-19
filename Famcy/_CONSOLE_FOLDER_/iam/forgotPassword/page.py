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