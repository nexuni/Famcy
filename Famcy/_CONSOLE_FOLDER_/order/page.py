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

# send_dict = {
# 	"service": "member",
# 	"operation": "get_item_info",
# 	"include": json.dumps(["會員純享6. 有糖家庭號豆漿","會員純享6. 無糖家庭號豆漿","會員純享6. 有糖瓶裝豆漿","會員純享6. 無糖瓶裝豆漿"])
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
# 	item_name = []
# 	for item in res_msg["avail_type"]:
# 		item_name.append(item["title"])
# 	avail_type = res_msg["avail_type"]

# PAGE_HEADER = {
# 	"title": ["doday豆漿預約", "豆日子歷史訂單"],
# 	"size": ["inner_section", "inner_section"],
# 	"type": ["input_form", "table"]
# }

# store_list = Famcy.input_form.generate_values_content("inputList")
# store_list.update({
#         "title": "選擇取貨店家",
#         "mandatory": True,
#         "value": avail_store_name
# 	})

# date_list = Famcy.input_form.generate_values_content("inputList")
# date_list.update({
# 		"title": "選擇取貨日期",
#         "mandatory": True,
#         "value": pick_up_datetime
# 	})

# size_list = Famcy.input_form.generate_values_content("inputList")
# size_list.update({
#         "title": "選擇豆漿大小",
#         "mandatory": True,
#         "value": item_name
# 	})

# amount_list = Famcy.input_form.generate_values_content("inputList")
# amount_list.update({
# 		"title": "選擇瓶數",
#         "mandatory": True,
#         "value": ["1", "2"]
# 	})

# doday_input_form = Famcy.input_form.generate_template_content([store_list, date_list, size_list, amount_list])
# doday_input_form.update({
# 		"main_desc": "歡迎doday會員預約豆漿!",
# 		"submit_type": "update_alert",
# 		"main_button_name": ["送出"],
# 		"action_after_post": "clean"
# 	})


class OrderPage(Famcy.FamcyPage):
    def __init__(self):
        super(OrderPage, self).__init__("/order", Famcy.ClassicStyle(), background_thread=False)
        self.p_card = self.prompt_card()
        self.layout.addPromptWidget(self.p_card, 50)

        self.card_1 = self.card1()
        self.card_2 = self.card2()

        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 1, 0)

    def card1(self):
        card1 = Famcy.FamcyCard()

        input_form = Famcy.input_form(layout_mode=Famcy.FamcyLayoutMode.custom)

        pure_input = Famcy.pureInput()
        input_btn = Famcy.inputBtn()
        input_list = Famcy.inputList()
        input_paragraph = Famcy.inputParagraph()
        input_password = Famcy.inputPassword()
        multiple_choices = Famcy.multipleChoicesRadioInput()
        single_choices = Famcy.singleChoiceRadioInput()
        url_btn = Famcy.urlBtn()
        submit_btn = Famcy.submitBtn()

        pure_input.update({
                "mandatory": True,
                "action_after_post": "save"
            })

        input_btn.update({
                "mandatory": False,
                "action_after_post": "save"
            })

        input_paragraph.update({
                "mandatory": False,
                "action_after_post": "save"
            })

        input_password.update({
                "mandatory": True,
                "action_after_post": "save"
            })

        multiple_choices.update({
                "value": ["multiple_choices1", "multiple_choices2", "multiple_choices3"],
                "mandatory": False,
                "action_after_post": "save"
            })

        single_choices.update({
                "value": ["single_choices1", "single_choices2", "single_choices3"],
                "mandatory": True,
                "action_after_post": "save"
            })

        input_list.update({
                "value": ["input_list1", "input_list2", "input_list3"],
                "mandatory": True,
                "action_after_post": "save"
            })

        url_btn.update({
                "url": "https://www.google.com/"
            })

        submit_btn.connect(self.submit_input, target=self.p_card)

        card1.postload = lambda: print("parent_card: ", submit_btn.parent, submit_btn.find_parent(submit_btn, "FCard"))

        input_form.layout.addWidget(pure_input, 0, 0)
        input_form.layout.addWidget(input_btn, 0, 1)
        input_form.layout.addWidget(input_paragraph, 1, 0, 1, 2)
        input_form.layout.addWidget(input_list, 2, 0)
        input_form.layout.addWidget(input_password, 2, 1)
        input_form.layout.addWidget(url_btn, 3, 0, 1, 2)
        input_form.layout.addWidget(multiple_choices, 4, 0)
        input_form.layout.addWidget(single_choices, 4, 1)
        input_form.layout.addWidget(submit_btn, 5, 0, 1, 2)

        input_form.layout.addCusWidget(pure_input, 0, 0)
        input_form.layout.addCusWidget(input_btn, 1, 0)
        input_form.layout.addCusWidget(input_paragraph, 2, 0)
        input_form.layout.addCusWidget(input_list, 3, 0)
        input_form.layout.addCusWidget(url_btn, 4, 0)
        input_form.layout.addCusWidget(input_password, 5, 0)
        input_form.layout.addCusWidget(multiple_choices, 6, 0)
        input_form.layout.addCusWidget(single_choices, 7, 0)
        input_form.layout.addCusWidget(submit_btn, 8, 0)
        input_form.layout.updateCustomLayoutContent(_max="540px")

        upload_form = Famcy.upload_form()

        upload_file = Famcy.uploadFile()
        submit_file = Famcy.submitBtn()

        submit_file.connect(self.submit_pic, target=card1)

        upload_form.layout.addWidget(upload_file, 0, 0)
        upload_form.layout.addWidget(submit_file, 1, 0)

        card1.layout.addWidget(input_form, 0, 0)
        card1.layout.addWidget(upload_form, 1, 0)
        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()

        display_image = Famcy.displayImage()
        display_light = Famcy.displayLight()
        display_tag = Famcy.displayTag()
        display_paragraph = Famcy.displayParagraph()
        display_paragraph.body.children[0].style["font-size"] = "50px"

        display_step_loader = Famcy.displayStepLoader()

        card2.layout.addWidget(display_image, 0, 0)
        card2.layout.addWidget(display_light, 0, 1)
        card2.layout.addWidget(display_tag, 1, 0, 1, 2)
        card2.layout.addWidget(display_paragraph, 2, 0, 1, 2)
        card2.layout.addWidget(display_step_loader, 3, 0, 1, 2)
        return card2

    def prompt_card(self):
        pcard = Famcy.FamcyCard()

        input_form = Famcy.input_form()
        submit_btn = Famcy.submitBtn()
        submit_btn.connect(self.submit_remove, target=pcard)

        input_form.layout.addWidget(submit_btn, 0, 0)

        pcard.layout.addWidget(input_form, 0, 0)
        return pcard

    def submit_input(self, submission_obj, info_list):
        return Famcy.UpdatePrompt()
        # return Famcy.UpdateRemoveElement()
        # return Famcy.UpdateAlert(alert_message=str(info_list))

    def submit_remove(self, submission_obj, info_list):
        return Famcy.UpdateRemoveElement(prompt_flag=True)

    def submit_pic(self, submission_obj, info_list):
        return Famcy.UpdateAlert(alert_message=str(info_list))

page = OrderPage()
page.register()

