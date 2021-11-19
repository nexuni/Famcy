import Famcy
import os
import json
import datetime
import requests

class SeasonPage(Famcy.FamcyPage):
	def __init__(self):
		super(SeasonPage, self).__init__("/season", Famcy.ClassicSideStyle(), background_thread=False)

		self.table_info = []

		self.p_del_card = self.p_card_delete()
		self.p_update_card = self.p_card_update()

		self.layout.addPromptWidget(self.p_del_card)
		self.layout.addPromptWidget(self.p_update_card)


		self.card_1 = self.card1()
		self.card_2 = self.card2()

		self.layout.addWidget(self.card_1, 0, 0)
		self.layout.addWidget(self.card_2, 1, 0)


	# card
	# ====================================================
	def card1(self):
		card1 = Famcy.FamcyCard()

		input_form = Famcy.input_form()

		input_year = Famcy.inputList()
		input_month = Famcy.inputList()
		input_date = Famcy.inputList()
		input_time = Famcy.inputList()

		input_year.update({
				"title": "輸入起始年份",
				"value": [str(int(datetime.datetime.now().year)-1), str(int(datetime.datetime.now().year)), str(int(datetime.datetime.now().year)+1), str(int(datetime.datetime.now().year)+2), str(int(datetime.datetime.now().year)+3)],
			})
		input_month.update({
				"title": "輸入起始月份",
				"value": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
			})
		input_date.update({
				"title": "輸入起始日期",
				"value": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
			})
		input_time.update({
				"title": "輸入起始時間",
				"value": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],
			})


		input_year2 = Famcy.inputList()
		input_month2 = Famcy.inputList()
		input_date2 = Famcy.inputList()
		input_time2 = Famcy.inputList()

		input_year2.update({
				"title": "輸入結束年份",
				"value": [str(int(datetime.datetime.now().year)-1), str(int(datetime.datetime.now().year)), str(int(datetime.datetime.now().year)+1), str(int(datetime.datetime.now().year)+2), str(int(datetime.datetime.now().year)+3)],
			})
		input_month2.update({
				"title": "輸入結束月份",
				"value": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
			})
		input_date2.update({
				"title": "輸入結束日期",
				"value": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"],
			})
		input_time2.update({
				"title": "輸入起始時間",
				"value": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],
			})


		input_license = Famcy.pureInput()
		input_license.update({"title": "輸入車牌號碼"})

		input_phone = Famcy.pureInput()
		input_phone.update({"title": "輸入電話號碼", "input_type":"number"})


		search_btn = Famcy.submitBtn()
		search_btn.update({"title": "查詢"})
		search_btn.connect(self.update_selected_car, target=card1)

		new_btn = Famcy.submitBtn()
		new_btn.update({"title": "更新"})
		new_btn.connect(self.prompt_submit_input, target=self.p_update_card)

		cancel_btn = Famcy.submitBtn()
		cancel_btn.update({"title": "刪除"})
		cancel_btn.connect(self.prompt_submit_input, target=self.p_del_card)

		input_form.layout.addWidget(input_year, 0, 0)
		input_form.layout.addWidget(input_month, 0, 1)
		input_form.layout.addWidget(input_date, 0, 2)
		input_form.layout.addWidget(input_time, 0, 3)
		input_form.layout.addWidget(input_year2, 1, 0)
		input_form.layout.addWidget(input_month2, 1, 1)
		input_form.layout.addWidget(input_date2, 1, 2)
		input_form.layout.addWidget(input_time2, 1, 3)
		input_form.layout.addWidget(input_license, 2, 0, 1, 2)
		input_form.layout.addWidget(input_phone, 2, 2, 1, 2)

		input_form.layout.addWidget(search_btn, 0, 4)
		input_form.layout.addWidget(new_btn, 1, 4)
		input_form.layout.addWidget(cancel_btn, 2, 4)

		card1.layout.addWidget(input_form, 0, 0)

		return card1

	def card2(self):
		card2 = Famcy.FamcyCard()
		card2.preload = self.get_season_data

		table_content = Famcy.table_block()
		table_content.update({
				"toolbar": False,
				"input_button": "none",
				"input_value_col_field": "platenum",
				"page_detail": False,
				"page_detail_content": ["<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>"],
				"page_footer": True,
				"page_footer_detail": {
					"page_size": 7,
					"page_list": [7, "all"]
				},
				"column": [[
					{
						"title": 'ID',
						"field": 'id',
						"rowspan": 1,
						"align": 'center',
						"valign": 'middle',
						"sortable": True
					},
					{
						"title": '更新時間',
						"field": 'modified_time',
						"rowspan": 1,
						"align": 'center',
						"valign": 'middle',
						"sortable": True
					},
					{
						"title": '車牌號碼',
						"field": 'platenum',
						"rowspan": 1,
						"align": 'center',
						"valign": 'middle',
						"sortable": True
					},
					{
						"title": '入口',
						"field": 'entry_station',
						"rowspan": 1,
						"align": 'center',
						"valign": 'middle',
						"sortable": True
					},
					{
						"title": '出口',
						"field": 'exit_station',
						"rowspan": 1,
						"align": 'center',
						"valign": 'middle',
						"sortable": True
					},
					{
						"title": '停車性質',
						"field": 'parked_type',
						"rowspan": 1,
						"align": 'center',
						"valign": 'middle',
						"sortable": True
					}
				]],
				"data": self.table_info
		  })

		card2.layout.addWidget(table_content, 0, 0)

		return card2
	# ====================================================
	# ====================================================


	# prompt card
	# ====================================================
	def p_card_update(self):
		p_card = Famcy.FamcyPromptCard()

		input_form = Famcy.input_form()

		input_id = Famcy.pureInput()
		input_id.update({"title":"ID:", "input_type":"number"})

		license_num = Famcy.pureInput()
		license_num.update({"title":"車牌號碼:", "input_type":"text"})

		time_num = Famcy.pureInput()
		time_num.update({"title":"起始時間-結束時間:", "input_type":"number", "num_range": [15, 15]})

		comments = Famcy.pureInput()
		comments.update({"title":"備註:", "input_type":"text"})

		submit_btn = Famcy.submitBtn()
		submit_btn.update({"title":"確認"})
		# submit_btn.connect(self.prompt_submit_input)

		cancel_btn = Famcy.submitBtn()
		cancel_btn.update({"title":"返回"})
		cancel_btn.connect(self.prompt_remove_input)

		input_form.layout.addWidget(input_id, 0, 0, 1, 2)
		input_form.layout.addWidget(license_num, 1, 0, 1, 2)
		input_form.layout.addWidget(time_num, 2, 0, 1, 2)
		input_form.layout.addWidget(comments, 3, 0, 1, 2)
		input_form.layout.addWidget(cancel_btn, 4, 0)
		input_form.layout.addWidget(submit_btn, 4, 1)

		p_card.layout.addWidget(input_form, 0, 0)

		return p_card

	def p_card_delete(self):
		p_card = Famcy.FamcyPromptCard()

		input_form = Famcy.input_form()

		input_id = Famcy.pureInput()
		input_id.update({"title":"ID:", "input_type":"number"})

		submit_btn = Famcy.submitBtn()
		submit_btn.update({"title":"確認"})
		submit_btn.connect(self.update_delete_season, target=p_card)

		cancel_btn = Famcy.submitBtn()
		cancel_btn.update({"title":"返回"})
		cancel_btn.connect(self.prompt_remove_input)

		input_form.layout.addWidget(input_id, 0, 0, 1, 2)
		input_form.layout.addWidget(cancel_btn, 1, 0)
		input_form.layout.addWidget(submit_btn, 1, 1)

		p_card.layout.addWidget(input_form, 0, 0)

		return p_card
	# ====================================================
	# ====================================================


	# submission function
	# ====================================================
	def prompt_remove_input(self, submission_obj, info_list):
		return Famcy.UpdateRemoveElement(prompt_flag=True)

	def prompt_submit_input(self, submission_obj, info_list):
		return Famcy.UpdatePrompt()

	def update_selected_car(self, submission_obj, info_list):
		flag = True
		for _ in info_list:
			if not len(_) > 0:
				flag = False
				break
		if flag:
			start_time = str(info_list[0][0]) + str(info_list[1][0]) + str(info_list[2][0]) + str(info_list[3][0]) + "0000000"
			end_time = str(info_list[4][0]) + str(info_list[5][0]) + str(info_list[6][0]) + str(info_list[7][0]) + "0000000"
			license_num = str(info_list[8][0])
			phonenum = str(info_list[9][0])

			self.get_season_data(phonenum=phonenum, start_time=start_time, end_time=end_time, platenum=license_num)
			return Famcy.UpdateBlockHtml(target=self.card_2)

		return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

	def update_delete_season(self, submission_obj, info_list):
		msg = "資料填寫有誤"
		if len(info_list[0]) > 0:
			_id = str(info_list[0][0])

			if self.post_delete(_id):
				self.get_season_data()
				msg = "成功刪除資料"

		return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]
	# ====================================================
	# ====================================================


	# http request function
	# ====================================================
	def get_season_data(self, phonenum=None, start_time=None, end_time=None, platenum=None):
		send_dict = {
			"service": "website",
			"operation": "get_season_data",
			"database_name": "season"
		}

		if phonenum and not phonenum == "" and not phonenum == "---":
			send_dict["phonenum"] = phonenum
		if start_time and len(start_time[2:]) == 15:
			send_dict["start_time"] = start_time[2:]
		if end_time and len(end_time[2:]) == 15:
			send_dict["end_time"] = end_time[2:]
		if platenum and not platenum == "":
			send_dict["platenum"] = platenum

		res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
		self.table_info = json.loads(res_msg)["message"] if json.loads(res_msg)["indicator"] else []
		self.card_2.layout.content[0][0].update({
				"data": self.table_info
			})

	def post_delete(self, _id):
		send_dict = {
			"service": "website",
			"operation": "modify_season_data",
			"entry_station": str(_id),
			"database_name": "season"
		}

		res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
		print(res_msg)
		return json.loads(res_msg)["indicator"]
	# ====================================================
	# ====================================================
   

page = SeasonPage()
page.register()