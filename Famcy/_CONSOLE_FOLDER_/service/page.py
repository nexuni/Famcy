import Famcy
import os
import json
import datetime
import requests

class SeasonPage(Famcy.FamcyPage):
	def __init__(self):
		super(SeasonPage, self).__init__("/season", Famcy.ClassicSideStyle(), background_thread=False)

		self.table_info = []
		self.carpark_id = "park1"

		self.p_del_card = self.p_card_delete()
		self.p_update_card = self.p_card_update()
		self.p_insert_card = self.p_card_insert()

		self.layout.addPromptWidget(self.p_del_card)
		self.layout.addPromptWidget(self.p_update_card)
		self.layout.addPromptWidget(self.p_insert_card, 60)


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
		search_btn.connect(self.update_search, target=card1)

		insert_btn = Famcy.submitBtn()
		insert_btn.update({"title": "新增"})
		insert_btn.connect(self.prompt_submit_input, target=self.p_insert_card)

		new_btn = Famcy.submitBtn()
		new_btn.update({"title": "更新"})
		new_btn.connect(self.prompt_submit_input, target=self.p_update_card)

		cancel_btn = Famcy.submitBtn()
		cancel_btn.update({"title": "刪除"})
		cancel_btn.connect(self.prompt_submit_input, target=self.p_del_card)

		input_form.layout.addWidget(input_year, 0, 0, 4, 1)
		input_form.layout.addWidget(input_month, 0, 1, 4, 1)
		input_form.layout.addWidget(input_date, 0, 2, 4, 1)
		input_form.layout.addWidget(input_time, 0, 3, 4, 1)

		input_form.layout.addWidget(input_year2, 4, 0, 4, 1)
		input_form.layout.addWidget(input_month2, 4, 1, 4, 1)
		input_form.layout.addWidget(input_date2, 4, 2, 4, 1)
		input_form.layout.addWidget(input_time2, 4, 3, 4, 1)

		input_form.layout.addWidget(input_license, 8, 0, 4, 2)
		input_form.layout.addWidget(input_phone, 8, 2, 4, 2)

		input_form.layout.addWidget(search_btn, 0, 4, 3, 1)
		input_form.layout.addWidget(insert_btn, 3, 4, 3, 1)
		input_form.layout.addWidget(new_btn, 6, 4, 3, 1)
		input_form.layout.addWidget(cancel_btn, 9, 4, 3, 1)

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
	def p_card_insert(self):
		p_card = Famcy.FamcyPromptCard()

		input_form = Famcy.input_form()

		phonenum = Famcy.pureInput()
		phonenum.update({"title":"電話號碼:", "input_type":"number"})

		license_num = Famcy.pureInput()
		license_num.update({"title":"車牌號碼:", "input_type":"text"})

		start_time = Famcy.pureInput()
		start_time.update({"title":"起始時間:", "input_type":"number"})

		end_time = Famcy.pureInput()
		end_time.update({"title":"結束時間:", "input_type":"number"})

		database_name = Famcy.inputList()
		database_name.update({
				"title": "資料庫名:",
				"value": ["season", "season_ticket"],
			})

		season_type = Famcy.inputList()
		season_type.update({
				"title": "月票種類:",
				"value": ["season", "dailyseason"],
			})

		month_fee = Famcy.pureInput()
		month_fee.update({"title":"月費:", "input_type":"number"})

		comments = Famcy.pureInput()
		comments.update({"title":"備註:", "input_type":"text"})

		submit_btn = Famcy.submitBtn()
		submit_btn.update({"title":"確認"})
		submit_btn.connect(self.update_insert, target=p_card)

		cancel_btn = Famcy.submitBtn()
		cancel_btn.update({"title":"返回"})
		cancel_btn.connect(self.prompt_remove_input)

		input_form.layout.addWidget(phonenum, 0, 0)
		input_form.layout.addWidget(license_num, 0, 1)
		input_form.layout.addWidget(start_time, 1, 0)
		input_form.layout.addWidget(end_time, 1, 1)
		input_form.layout.addWidget(database_name, 2, 0)
		input_form.layout.addWidget(season_type, 2, 1)
		input_form.layout.addWidget(month_fee, 3, 0)
		input_form.layout.addWidget(comments, 3, 1)
		input_form.layout.addWidget(cancel_btn, 4, 0)
		input_form.layout.addWidget(submit_btn, 4, 1)

		p_card.layout.addWidget(input_form, 0, 0)

		return p_card

	def p_card_update(self):
		p_card = Famcy.FamcyPromptCard()

		input_form = Famcy.input_form()

		input_id = Famcy.pureInput()
		input_id.update({"title":"ID:", "input_type":"number"})

		license_num = Famcy.pureInput()
		license_num.update({"title":"車牌號碼:", "input_type":"text"})

		start_time = Famcy.pureInput()
		start_time.update({"title":"起始時間:", "input_type":"number"})

		end_time = Famcy.pureInput()
		end_time.update({"title":"結束時間:", "input_type":"number"})

		comments = Famcy.pureInput()
		comments.update({"title":"備註:", "input_type":"text"})

		submit_btn = Famcy.submitBtn()
		submit_btn.update({"title":"確認"})
		submit_btn.connect(self.update_modify, target=p_card)

		cancel_btn = Famcy.submitBtn()
		cancel_btn.update({"title":"返回"})
		cancel_btn.connect(self.prompt_remove_input)

		input_form.layout.addWidget(input_id, 0, 0, 1, 2)
		input_form.layout.addWidget(license_num, 1, 0, 1, 2)
		input_form.layout.addWidget(start_time, 2, 0, 1, 2)
		input_form.layout.addWidget(end_time, 3, 0, 1, 2)
		input_form.layout.addWidget(comments, 4, 0, 1, 2)
		input_form.layout.addWidget(cancel_btn, 5, 0)
		input_form.layout.addWidget(submit_btn, 5, 1)

		p_card.layout.addWidget(input_form, 0, 0)

		return p_card

	def p_card_delete(self):
		p_card = Famcy.FamcyPromptCard()

		input_form = Famcy.input_form()

		input_id = Famcy.pureInput()
		input_id.update({"title":"ID:", "input_type":"number"})

		submit_btn = Famcy.submitBtn()
		submit_btn.update({"title":"確認"})
		submit_btn.connect(self.update_delete, target=p_card)

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

	def update_search(self, submission_obj, info_list):
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

	def update_delete(self, submission_obj, info_list):
		msg = "資料填寫有誤"
		if len(info_list[0]) > 0:
			_id = str(info_list[0][0])
			license_num = "XXXXXX"

			if self.post_modify(_id, license_num):
				self.get_season_data()
				msg = "成功刪除資料"

		return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

	def update_modify(self, submission_obj, info_list):
		msg = "資料填寫有誤"
		flag = True
		for _ in info_list:
			if not len(_) > 0:
				flag = False
				break
		if flag:
			_id = str(info_list[0][0])
			license_num = str(info_list[1][0])
			start_time = str(info_list[2][0])
			end_time = str(info_list[3][0])
			comments = str(info_list[4][0])

			if self.post_modify(_id, license_num, start_time=start_time, end_time=end_time, comments=comments):
				self.get_season_data()
				msg = "成功修改資料"

		return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

	def update_insert(self, submission_obj, info_list):
		msg = "資料填寫有誤"
		flag = True
		for _ in info_list:
			if not len(_) > 0:
				flag = False
				break
		if flag:
			phonenum = str(info_list[0][0])
			license_num = str(info_list[1][0])
			start_num = str(info_list[2][0])
			end_num = str(info_list[3][0])
			database_name = str(info_list[4][0])
			season_type = str(info_list[5][0])
			month_fee = str(info_list[6][0])
			comments = str(info_list[7][0])

			if self.post_insert(phonenum, license_num, start_num, end_num, database_name, season_type, month_fee, comments):
				self.get_season_data()
				msg = "成功加入資料"

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

		if phonenum and not phonenum == "" and len(str(phonenum)) == 10:
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

	def post_modify(self, _id, license_num, start_time=None, end_time=None, comments=None):
		send_dict = {
			"service": "website",
			"operation": "modify_season_data",
			"id_number": str(_id),
			"database_name": "season",
			"platenum": license_num
		}

		if start_time and len(start_time[2:]) == 15:
			send_dict["start_time"] = start_time[2:]
		if end_time and len(end_time[2:]) == 15:
			send_dict["end_time"] = end_time[2:]
		if comments and not comments == "":
			send_dict["comments"] = comments

		res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
		print(res_msg)
		return json.loads(res_msg)["indicator"]

	def post_insert(self, phonenum, license_num, start_num, end_num, database_name, season_type, month_fee, comments):
		send_dict = {
			"service": "website",
			"operation": "post_season_data",
			"carpark_id": self.carpark_id,
			"phonenum": phonenum,
			"platenum": license_num,
			"start_time": start_num,
			"end_time": end_num,
			"database_name": database_name,
			"season_type": season_type,
			"months_fee": month_fee,
			"comments": comments
		}

		res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
		print(res_msg)
		return json.loads(res_msg)["indicator"]
	# ====================================================
	# ====================================================
   

page = SeasonPage()
page.register()