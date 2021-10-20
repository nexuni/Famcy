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
import json

send_dict = {
	"service": "member",
	"operation": "get_item_info",
	"include": json.dumps(["會員純享6. 有糖家庭號豆漿","會員純享6. 無糖家庭號豆漿","會員純享6. 有糖瓶裝豆漿","會員純享6. 無糖瓶裝豆漿"])
}
res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
res_ind = json.loads(res_str)["indicator"]
res_msg = json.loads(res_str)["message"]

print(res_str)

pick_up_datetime = []
avail_store_name = []
avail_type = []

if res_ind:
	pick_up_datetime = res_msg["pick_up_datetime"]
	avail_store_name = res_msg["avail_store_name"]
	item_name = []
	for item in res_msg["avail_type"]:
		item_name.append(item["title"])
	avail_type = res_msg["avail_type"]

PAGE_HEADER = {
	"title": ["doday豆漿預約", "豆日子歷史訂單"],
	"size": ["inner_section", "inner_section"],
	"type": ["input_form", "table"]
}

store_list = Famcy.input_form.generate_values_content("inputList")
store_list.update({
        "title": "選擇取貨店家",
        "mandatory": True,
        "value": avail_store_name
	})

date_list = Famcy.input_form.generate_values_content("inputList")
date_list.update({
		"title": "選擇取貨日期",
        "mandatory": True,
        "value": pick_up_datetime
	})

size_list = Famcy.input_form.generate_values_content("inputList")
size_list.update({
        "title": "選擇豆漿大小",
        "mandatory": True,
        "value": item_name
	})

amount_list = Famcy.input_form.generate_values_content("inputList")
amount_list.update({
		"title": "選擇瓶數",
        "mandatory": True,
        "value": ["1", "2"]
	})

doday_input_form = Famcy.input_form.generate_template_content([store_list, date_list, size_list, amount_list])
doday_input_form.update({
		"main_desc": "歡迎doday會員預約豆漿!",
		"submit_type": "update_alert",
		"main_button_name": ["送出"],
		"action_after_post": "clean"
	})




# send_dict = {
#     "service": "member",
#     "operation": "get_history_order",
#     "user_phone": Famcy.FManager["CurrentUser"].phone_num,
#     "member_order": "True"
# }
# res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
# res_ind = json.loads(res_str)["indicator"]
# res_msg = json.loads(res_str)["message"]

# table_info = []

# if res_ind:
#     table_info = res_msg

# table_content = Famcy.table.generate_template_content()
# table_content.update({
# 		"main_button_name": [],
# 		"input_button": "none",
#         "page_detail": False,
#         "page_detail_content": ["<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>"],
#         "page_footer": True,
#         "page_footer_detail": {
#             "page_size": 10,
#             "page_list": [10, 20, "all"]
#         },
#         "column": [[{
#                 "title": 'datetime',
#                 "field": 'datetime',
#                 "rowspan": 1,
#                 "align": 'center',
#                 "valign": 'middle',
#                 "sortable": True
#             },
#             {
#                 "title": 'order',
#                 "field": 'order',
#                 "rowspan": 1,
#                 "align": 'center',
#                 "valign": 'middle',
#                 "sortable": True
#             },
#             {
#                 "title": 'total_price',
#                 "field": 'total_price',
#                 "rowspan": 1,
#                 "align": 'center',
#                 "valign": 'middle',
#                 "sortable": True
#             },
#             {
#                 "title": 'used_point',
#                 "field": 'used_point',
#                 "rowspan": 1,
#                 "align": 'center',
#                 "valign": 'middle',
#                 "sortable": True
#             }
#         ]],
#         "data": table_info
# 	})










# PAGE_CONTENT = [doday_input_form, table_content]

# def find_item(item_name, amount):
# 	for item in avail_type:
# 		if item["title"] == item_name:
# 			temp = []
# 			for i in range(int(amount)):
# 				temp.append(item)
# 			return temp
# 	return None

# def find_store(store_name):
# 	if store_name == "辛亥店":
# 		return "DDB"
# 	elif store_name == "木柵店":
# 		return "DDA"
# 	return None

# def doday_input_form_submission(submission_list, **configs):
# 	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[0].context["submit_type"])
# 	item = find_item(submission_list[2][0])
# 	store = find_store(submission_list[0][0])

# 	msg = "未成功送出訂單，請重新再試"

# 	if item and store:
# 		submit_data = {
# 			"operation":"add_to_member_cart",
# 			"service":"order",
# 			"store_id":store,
# 			"item":item,
# 			"user_phone":"0983030465",
# 			"name":"test",
# 			"datetime":submission_list[1][0]
# 		}

# 		post_str = Famcy.CLIENT_SERVER.client_post("member_http_url", submit_data, gauth=True)
# 		post_ind = json.loads(post_str)["indicator"]
# 		post_msg = json.loads(post_str)["message"]

# 		if post_ind:
# 			msg = "成功送出訂單"

# 	return submission_dict_handler.return_submit_info(msg=msg)

# PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [doday_input_form_submission, None])