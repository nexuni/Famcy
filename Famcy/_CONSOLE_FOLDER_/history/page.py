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


# send_dict = {
#     "service": "member",
#     "operation": "get_history_order",
#     "user_phone": Famcy._current_user.phone_num
# }
# res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
# res_ind = json.loads(res_str)["indicator"]
# res_msg = json.loads(res_str)["message"]

# table_info = []

# if res_ind:
#     table_info = res_msg


# PAGE_HEADER = {
# 	"title": ["豆日子歷史訂單"],
# 	"size": ["inner_section"],
# 	"type": ["table"]
# }

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

# PAGE_CONTENT = [table_content]

# PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT)

class HistoryPage(Famcy.FamcyPage):
    def __init__(self):
        super(HistoryPage, self).__init__("/history", Famcy.ClassicStyle(), background_thread=False)
        
        self.table_info = []

        self.card_1 = self.card1()
        self.layout.addWidget(self.card_1, 0, 0)

    def card1(self):
        card1 = Famcy.FamcyCard()

        card1.preload = self.get_history_order

        input_form = Famcy.input_form()

        table_content = Famcy.table()
        table_content.update({
                "input_button": "checkbox",
                "input_value_col_field": "datetime",
                "page_detail": False,
                "page_detail_content": ["<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>"],
                "page_footer": True,
                "page_footer_detail": {
                    "page_size": 10,
                    "page_list": [10, 20, "all"]
                },
                "column": [[{
                        "title": 'datetime',
                        "field": 'datetime',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'order',
                        "field": 'order',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'total_price',
                        "field": 'total_price',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'used_point',
                        "field": 'used_point',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    }
                ]],
                "data": self.table_info
          })

        submit_btn = Famcy.submitBtn()
        submit_btn.connect(self.submit_table, target=card1)

        input_form.layout.addWidget(table_content, 0, 0)
        input_form.layout.addWidget(submit_btn, 1, 0)

        card1.layout.addWidget(input_form, 0, 0)
        return card1

    def get_history_order(self):
        send_dict = {
            "service": "member",
            "operation": "get_history_order",
            "user_phone": "0905860683"
        }
        res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
        res_ind = json.loads(res_str)["indicator"]
        res_msg = json.loads(res_str)["message"]

        self.table_info = [{
                    "datetime": "1",
                    "order": "2",
                    "total_price": "3",
                    "used_point": "4"
                },
                {
                    "datetime": "5",
                    "order": "6",
                    "total_price": "7",
                    "used_point": "8"
                }]
        self.card_1.layout.content[0][0].layout.content[0][0].update({
            "data": self.table_info
        })

    def submit_table(self, submission_obj, info_list):
        return Famcy.UpdateAlert(alert_message=str(info_list))

page = HistoryPage()
page.register()