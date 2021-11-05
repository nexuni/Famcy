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
	"title": ["Nexuni 圓餅圖", "Nexuni 圓餅圖"],
	"size": ["inner_section", "inner_section"],
	"type": ["table", ["display", "input_form"]]
}

table_content = Famcy.table_block.generate_template_content()

display_light_block = Famcy.display.generate_values_content("displayLight")

list_form_content1 = Famcy.input_form.generate_values_content("inputList")
list_form_content1.update({
		"value": ["1", "2", "3"]
	})
list_form_content2 = Famcy.input_form.generate_values_content("inputList")
list_form_content2.update({
		"value": ["5", "6", "7"]
	})

input_form_content = Famcy.input_form.generate_template_content([list_form_content1, list_form_content2])
input_form_content.update({
		"main_button_name": ["送出"], # btn name in same section must not be same
		"action_after_post": "save",                    # (clean / save)
	})

PAGE_CONTENT = [table_content, [Famcy.display.generate_template_content([display_light_block]), input_form_content]]

def after_submit(submission_list, **configs):
	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[0].context["submit_type"])

	table_content.update({
		"data": [
				{
					"col_title1": "row_content11",
					"col_title2": "row_content12",
					"col_title3": "row_content13"
				},
				{
					"col_title1": "row_content21",
					"col_title2": "row_content22",
					"col_title3": "row_content23"
				},
				{
					"col_title1": "row_content31",
					"col_title2": "row_content32",
					"col_title3": "row_content33"
				},
				{
					"col_title1": "row_content11",
					"col_title2": "row_content12",
					"col_title3": "row_content13"
				},
				{
					"col_title1": "row_content21",
					"col_title2": "row_content22",
					"col_title3": "row_content23"
				},
				{
					"col_title1": "row_content31",
					"col_title2": "row_content32",
					"col_title3": "row_content33"
				}
			]
		})

	PAGE_CONTENT_OBJECT[0].update_page_context(table_content)

	content = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[0])
	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")

def after_submit_2(submission_list, **configs):
	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[1][1].context["submit_type"])

	if submission_list[0][0] == "1":
		display_light_block.update({
			"status": {"red": "", "yellow": "bulb_yellow", "green": ""},
	    })
	elif submission_list[0][0] == "2":
		display_light_block.update({
			"status": {"red": "", "yellow": "", "green": "bulb_green"},
	    })
	elif submission_list[0][0] == "3":
		display_light_block.update({
		    "status": {"red": "bulb_red", "yellow": "", "green": ""},
	    })

	PAGE_CONTENT_OBJECT[1][0].update_page_context({
			"values": [display_light_block]
		})


	content = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[1])
	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")


PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [after_submit, [None, after_submit_2]])