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
import os
# from werkzeug.utils import secure_filename


def test_function(context, **configs):
	print("test_function")


PAGE_HEADER = {
	"title": ["doday客服表單"],
	"size": ["inner_section"],
	"type": ["input_form"]
}

mail_title = Famcy.input_form.generate_values_content("pureInput")
mail_title.update({
        "title": "主旨",
        "input_type": "text",
        "placeholder": "",
        "mandatory": True,
	})

mail_content = Famcy.input_form.generate_values_content("inputParagraph")
mail_content.update({
		"title": "信件內容",
        "placeholder": "",
        "mandatory": False,
	})

doday_input_form = Famcy.input_form.generate_template_content([mail_title, mail_content])
doday_input_form.update({
		"main_desc": "歡迎doday會員寫信!",
		"submit_type": "update_alert",
		"main_button_name": ["送出"],
		"action_after_post": "save",
		"before_function": [test_function]
	})

PAGE_CONTENT = [doday_input_form]

def doday_input_form_submission(submission_list, **configs):
	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[0].context["submit_type"])
	return submission_dict_handler.return_submit_info(msg=str(submission_list))

PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [doday_input_form_submission])