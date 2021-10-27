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
#   "service": "member",
#   "operation": "get_member_status",
#   "user_phone": Famcy._current_user.phone_num
# }
# res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
# res_ind = json.loads(res_str)["indicator"]
# res_msg = json.loads(res_str)["message"]

# member_status = ""
# member_date_range = ""

# if res_ind:
#   member_status = res_msg["member_status"]
#   member_date_range = res_msg["member_date_range"][0] + " - " + res_msg["member_date_range"][0]




# send_dict = {
#   "service": "member",
#   "operation": "get_point_info",
#   "user_phone": Famcy._current_user.phone_num
# }
# res_str = Famcy.CLIENT_SERVER.client_get("member_http_url", send_dict, gauth=True)
# res_ind = json.loads(res_str)["indicator"]
# res_msg = json.loads(res_str)["message"]

# member_point = "0"
# accumulated_point = "0"
# accumulated_money = "0"

# if res_ind:
#   member_point = res_msg["reward_points"]
#   accumulated_point = res_msg["accumulated_point"]
#   accumulated_money = res_msg["accumulated_money"]





# PAGE_HEADER = {
#   "title": ["豆日子會員專區"],
#     "size": ["inner_section"],
#     "type": ["doday_member_card"]
# }

# card_section = Famcy.doday_member_card.generate_template_content()
# card_section.update({
#     "main_status": member_status,
#         "sub_title": member_date_range,
#         "member_point": member_point,
#         "accumulated_point": accumulated_point,
#         "accumulated_money": accumulated_money,
#   })

# PAGE_CONTENT = [card_section]
# PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT)

class OverviewPage(Famcy.FamcyPage):
	def __init__(self):
		super(OverviewPage, self).__init__("/overview", Famcy.ClassicStyle(), layout_mode=Famcy.FamcyLayoutMode.custom, background_thread=False)

		self.card_1 = self.card1()
		self.card_2 = self.card2()
		self.card_3 = self.card3()
		self.card_4 = self.card4()
		self.card_5 = self.card5()

		self.layout.addWidget(self.card_1, 0, 0)
		self.layout.addWidget(self.card_2, 1, 0)
		self.layout.addWidget(self.card_3, 2, 0)
		self.layout.addWidget(self.card_4, 3, 0)
		self.layout.addWidget(self.card_5, 4, 0)

		self.layout.addCusWidget(self.card_1, 0, 0, 1, 2)
		self.layout.addCusWidget(self.card_2, 1, 0)
		self.layout.addCusWidget(self.card_3, 1, 1)
		self.layout.addCusWidget(self.card_4, 2, 0, 1, 2)
		self.layout.addCusWidget(self.card_5, 3, 0, 1, 2)
		self.layout.updateCustomLayoutContent(_min="960px")

	def card1(self):
		card1 = Famcy.FamcyCard()

		pie_chart = Famcy.pie_chart()

		card1.layout.addWidget(pie_chart, 0, 0)
		return card1

	def card2(self):
		card2 = Famcy.FamcyCard()

		line_chart = Famcy.line_chart()

		card2.layout.addWidget(line_chart, 0, 0)
		return card2

	def card3(self):
		card3 = Famcy.FamcyCard()

		bar_chart = Famcy.bar_chart()

		card3.layout.addWidget(bar_chart, 0, 0)
		return card3

	def card4(self):
		card4 = Famcy.FamcyCard()

		event_calendar = Famcy.event_calendar()

		card4.layout.addWidget(event_calendar, 0, 0)
		return card4

	def card5(self):
		card5 = Famcy.FamcyCard()

		input_time = Famcy.input_form()

		with_btn_calendar = Famcy.with_btn_calendar()
		submit_btn = Famcy.submitBtn()
		submit_btn.connect(self.submit_time, target=card5)

		input_time.layout.addWidget(with_btn_calendar, 0, 0)
		input_time.layout.addWidget(submit_btn, 1, 0)

		card5.layout.addWidget(input_time, 0, 0)
		return card5

	def submit_time(self, submission_obj, info_list):
		return Famcy.UpdateAlert(alert_message=str(info_list))		

page = OverviewPage()
page.register()