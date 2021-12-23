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

# send_dict = {
# 	"service": "member",
# 	"operation": "get_item_info"
# }
# res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
# res_ind = json.loads(res_str)["indicator"]
# res_msg = json.loads(res_str)["message"]

# print(res_str)

# pick_up_datetime = []
# avail_store_name = []
# avail_type = []

# if res_ind:
# 	pick_up_datetime = res_msg["pick_up_datetime"]
# 	avail_store_name = res_msg["avail_store_name"]
# 	avail_type = res_msg["avail_type"]

# def find_total_price(unit):
# 	total = 0
# 	for item in PAGE_CONTENT_OBJECT[0].context["cart_item"]:
# 		print(unit, int(item[unit]))
# 		total += int(item[unit])

# 	return str(total)

# def change_total_price(submission_list, **configs):
# 	print("submission_list", submission_list)
# 	submission_dict_handler = Famcy.SijaxSubmit("update_block_html")
# 	if submission_list == "現金":
# 		PAGE_CONTENT_OBJECT[1][0].context["values"][0]["content"] = "NT$ " + find_total_price("price")
		
# 	elif submission_list == "點數":
# 		PAGE_CONTENT_OBJECT[1][0].context["values"][0]["content"] = find_total_price("point") + " 點"
	
# 	msg = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[1])
# 	return submission_dict_handler.return_submit_info(msg=msg)


# PAGE_HEADER = {
# 	"title": ["購物車", "", "DoDay 商店"],
# 	"size": ["half_inner_section", "half_inner_section", "inner_section"],
# 	"type": ["doday_shopping_cart", ["display", "input_form"], "doday_shop"],
# }

# doday_cart_section = Famcy.doday_shopping_cart.generate_template_content()


# store_list = Famcy.input_form.generate_values_content("inputList")
# store_list.update({
# 		"title": "選擇取貨店家",
# 		"mandatory": True,
# 		"value": avail_store_name
# 	})

# date_list = Famcy.input_form.generate_values_content("inputList")
# date_list.update({
# 		"title": "選擇取貨日期",
# 		"mandatory": True,
# 		"value": pick_up_datetime
# 	})

# payment_list = Famcy.input_form.generate_values_content("inputList")
# payment_list.update({
# 		"title": "選擇付款方式",
# 		"mandatory": True,
# 		"value": ["現金", "點數"],
# 		"list_selected_action": [change_total_price, change_total_price]
# 	})

# name_input = Famcy.input_form.generate_values_content("pureInput")
# name_input.update({
# 		"title": "取貨人姓名",
# 		"input_type": "text",
# 		"placeholder": "",
# 		"mandatory": True,
# 	})

# doday_cart_submit_section = Famcy.input_form.generate_template_content([name_input, store_list, date_list, payment_list])
# doday_cart_submit_section.update({
# 		"main_desc": "",
# 		"submit_type": "update_alert",
# 		"main_button_name": ["送出購物車"],
# 		"action_after_post": "save"
# 	})

# price_label = Famcy.display.generate_values_content("displayTag")
# price_label.update({
# 		"title": "總價: ",
#         "content": "NT$ 0 / 0 點"
# 	})

# display_section = Famcy.display.generate_template_content([price_label])

# doday_shop_section = Famcy.doday_shop.generate_template_content()
# doday_shop_section.update({
# 		"shop_item": avail_type,
# 		"submit_type": "update_tab_html",
# 	})


# def find_item(item_name, cart_item_list):
# 	for cart_item in cart_item_list:
# 		if cart_item["title"] == item_name:
# 			cart_item["amount"] += 1
# 			return True

# 	for item in avail_type:
# 		if item["title"] == item_name:
# 			item["amount"] = 1
# 			cart_item_list.append(item)
# 			return True

# 	return False

# def del_item(item_name, cart_item_list):
# 	for i in range(len(cart_item_list)):
# 		print("cart_item_list: ", cart_item_list)
# 		if cart_item_list[i]["title"] == item_name:
# 			if cart_item_list[i]["amount"] > 1:
# 				cart_item_list[i]["amount"] -= 1
# 				return True
# 			else:
# 				del cart_item_list[i]
# 				print("cart_item_list after: ", cart_item_list)
# 				return True
# 	return False

# def find_store(store_name):
# 	if store_name == "辛亥店":
# 		return "DDB"
# 	elif store_name == "木柵店":
# 		return "DDA"
# 	return None

# def submit_item(item_list):
# 	temp = []
# 	for item in item_list:
# 		if item["amount"] != 1:
# 			for i in range(item["amount"]):
# 				temp.append(item)
# 		else:
# 			adict.pop("amount")
# 			temp.append(item)
# 		return temp
# 	return None

# def shop_item_submission(submission_list, **configs):
# 	flag = find_item(submission_list[0][0], PAGE_CONTENT_OBJECT[0].context["cart_item"])

# 	if flag:
# 		PAGE_CONTENT_OBJECT[1][0].context["values"][0]["content"] = "NT$ " + find_total_price("price") + " / " + find_total_price("point") + " 點"
# 		submission_dict_handler = Famcy.SijaxSubmit("update_tab_html")
# 		msg = submission_dict_handler.generate_tab_html("shop")
# 	else:
# 		submission_dict_handler = Famcy.SijaxSubmit("update_alert")
# 		msg = "商品未成功加入購物車，請重新再試"
# 	return submission_dict_handler.return_submit_info(msg=msg)

# def del_shop_item_submission(submission_list, **configs):
# 	flag = del_item(submission_list[0][0], PAGE_CONTENT_OBJECT[0].context["cart_item"])

# 	if flag:
# 		PAGE_CONTENT_OBJECT[1][0].context["values"][0]["content"] = "NT$ " + find_total_price("price") + " / " + find_total_price("point") + " 點"
# 		submission_dict_handler = Famcy.SijaxSubmit("update_tab_html")
# 		msg = submission_dict_handler.generate_tab_html("shop")
# 	else:
# 		submission_dict_handler = Famcy.SijaxSubmit("update_alert")
# 		msg = "商品未成功刪除，請重新再試"
# 	return submission_dict_handler.return_submit_info(msg=msg)

# def cart_submission(submission_list, **configs):
# 	store = find_store(submission_list[1][0])
# 	item = submit_item(PAGE_CONTENT_OBJECT[0].context["cart_item"])

# 	msg = "未成功送出訂單，請重新再試"

# 	if store:
# 		submit_data = {
# 			"operation":"add_to_member_cart",
# 			"service":"order",
# 			"store_id":store,
# 			"item":item,
# 			"user_phone":"0983030465",
# 			"name":"test",
# 			"datetime":submission_list[2][0]
# 		}

# 		post_str = Famcy.FManager.http_client.client_post("member_http_url", submit_data, gauth=True)
# 		post_ind = json.loads(post_str)["indicator"]
# 		post_msg = json.loads(post_str)["message"]

# 		if post_ind:
# 			msg = "成功送出訂單"
			
# 	submission_dict_handler = Famcy.SijaxSubmit("update_alert")
# 	return submission_dict_handler.return_submit_info(msg=msg)

# PAGE_CONTENT = [doday_cart_section, [display_section, doday_cart_submit_section], doday_shop_section]

# PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [del_shop_item_submission, [None, cart_submission], shop_item_submission])