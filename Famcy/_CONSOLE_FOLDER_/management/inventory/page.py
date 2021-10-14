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

PAGE_HEADER = {
	"title": ["Nexuni 表單", "Nexuni 上傳檔案"],
	"size": ["half_inner_section", "half_inner_section"],
	"type": ["input_form", "upload_form"]
}

list_form_content1 = Famcy.input_form.generate_values_content("inputList")
list_form_content1.update({
		"value": ["list1", "list2", "list3"]
	})
list_form_content2 = Famcy.input_form.generate_values_content("inputList")
list_form_content2.update({
		"value": ["list1", "list2", "list3"]
	})

input_form_content = Famcy.input_form.generate_template_content([list_form_content1, list_form_content2])
input_form_content.update({
		"submit_type": "update_tab_html",
		"main_button_name": ["送出"], # btn name in same section must not be same
		"action_after_post": "save",                    # (clean / save)
	})

upload_form_detail = Famcy.upload_form.generate_values_content("uploadFile")
upload_form_detail.update({
		"title": "庫存照",
		"accept_type": ["png", "jpg", "heic", "txt"],
		"file_path": './__submissions__'
	})

upload_form_content = Famcy.upload_form.generate_template_content([upload_form_detail])
upload_form_content.update({
		"submit_type": "update_alert",
		"main_button_name": ["更新庫存照"]
	})

PAGE_CONTENT = [input_form_content, upload_form_content]

def file_submission(submission_list, **configs):
	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[1].context["submit_type"])
	img_data = submission_dict_handler.generate_image_data(submission_list[0][0])

	index = int(submission_list[0][2])
	with open(PAGE_CONTENT_OBJECT[1].context["values"][index]["file_path"] + "/" + submission_list[0][1], "wb") as fh:
		fh.write(img_data)
		
	return submission_dict_handler.return_submit_info(msg="succeed")

def input_form_submission(submission_list, **configs):
	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[0].context["submit_type"])
	content = submission_dict_handler.generate_tab_html("management-inventory")
	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")
	
PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [input_form_submission, file_submission])