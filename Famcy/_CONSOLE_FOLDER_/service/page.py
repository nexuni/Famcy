import Famcy
import os
import json
import datetime
import requests
import pandas as pd

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

		input_date = Famcy.pureInput()
		input_time = Famcy.pureInput()
		input_date2 = Famcy.pureInput()
		input_time2 = Famcy.pureInput()

		default_date, default_time, default_end_date, default_end_time = self.get_default_date_time()

		input_date.update({"title": "輸入起始日期", "input_type": "date", "defaultValue": default_date})
        input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": default_time})
        input_date2.update({"title": "輸入結束日期", "input_type": "date", "defaultValue": default_end_date})
        input_time2.update({"title": "輸入結束時間", "input_type": "time", "defaultValue": default_end_time})


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

		download_btn = Famcy.submitBtn()
		download_btn.update({"title": "下載表格"})
		download_btn.connect(self.download_table, target=card1)


		input_form.layout.addWidget(input_date, 0, 0, 2, 1)
		input_form.layout.addWidget(input_time, 0, 1, 2, 1)
		input_form.layout.addWidget(input_date2, 0, 2, 2, 1)
		input_form.layout.addWidget(input_time2, 0, 3, 2, 1)

		input_form.layout.addWidget(input_license, 2, 0, 2, 1)
		input_form.layout.addWidget(input_phone, 2, 1, 2, 1)
		input_form.layout.addWidget(download_btn, 2, 3, 2, 1)

		input_form.layout.addWidget(search_btn, 0, 4)
		input_form.layout.addWidget(insert_btn, 1, 4)
		input_form.layout.addWidget(new_btn, 2, 4)
		input_form.layout.addWidget(cancel_btn, 3, 4)

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
					"page_size": 15,
					"page_list": [15, "all"]
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

		input_date = Famcy.pureInput()
		input_time = Famcy.pureInput()
		input_date2 = Famcy.pureInput()
		input_time2 = Famcy.pureInput()

		input_date.update({"title": "輸入起始日期", "input_type": "date"})
		input_time.update({"title": "輸入起始時間", "input_type": "time"})
		input_date2.update({"title": "輸入結束日期", "input_type": "date"})
		input_time2.update({"title": "輸入結束時間", "input_type": "time"})

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
		input_form.layout.addWidget(input_date, 1, 0)
		input_form.layout.addWidget(input_time, 1, 1)
		input_form.layout.addWidget(input_date2, 2, 0)
		input_form.layout.addWidget(input_time2, 2, 1)
		input_form.layout.addWidget(database_name, 3, 0)
		input_form.layout.addWidget(season_type, 3, 1)
		input_form.layout.addWidget(month_fee, 4, 0)
		input_form.layout.addWidget(comments, 4, 1)
		input_form.layout.addWidget(cancel_btn, 5, 0)
		input_form.layout.addWidget(submit_btn, 5, 1)

		p_card.layout.addWidget(input_form, 0, 0)

		return p_card

	def p_card_update(self):
		p_card = Famcy.FamcyPromptCard()

		input_form = Famcy.input_form()

		input_id = Famcy.pureInput()
		input_id.update({"title":"ID:", "input_type":"number"})

		license_num = Famcy.pureInput()
		license_num.update({"title":"車牌號碼:", "input_type":"text"})

		input_date = Famcy.pureInput()
		input_time = Famcy.pureInput()
		input_date2 = Famcy.pureInput()
		input_time2 = Famcy.pureInput()

		input_date.update({"title": "輸入起始日期", "input_type": "date"})
		input_time.update({"title": "輸入起始時間", "input_type": "time"})
		input_date2.update({"title": "輸入結束日期", "input_type": "date"})
		input_time2.update({"title": "輸入結束時間", "input_type": "time"})

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
		input_form.layout.addWidget(input_date, 2, 0)
		input_form.layout.addWidget(input_time, 2, 1)
		input_form.layout.addWidget(input_date2, 3, 0)
		input_form.layout.addWidget(input_time2, 3, 1)
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
			start_time = info_list[0][0][:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
			end_time = info_list[2][0][:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
			license_num = str(info_list[4][0])
			phonenum = str(info_list[5][0])

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
			start_time = info_list[2][0][:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
			end_time = info_list[4][0][:4] + info_list[4][0][5:7] + info_list[4][0][8:10] + info_list[5][0][:2] + info_list[5][0][3:] + "00000"
			comments = str(info_list[6][0])

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
			start_num = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
			end_num = info_list[4][0][2:4] + info_list[4][0][5:7] + info_list[4][0][8:10] + info_list[5][0][:2] + info_list[5][0][3:] + "00000"
			database_name = str(info_list[6][0])
			season_type = str(info_list[7][0])
			month_fee = str(info_list[8][0])
			comments = str(info_list[9][0])

			if self.post_insert(phonenum, license_num, start_num, end_num, database_name, season_type, month_fee, comments):
				self.get_season_data()
				msg = "成功加入資料"

		return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

	def download_table(self, submission_obj, info_list):
		msg = "資料填寫有誤"

		try:
			df1 = pd.DataFrame.from_records(self.table_info)
			df1.to_excel("output.xlsx",sheet_name='sheet1')

			msg = "成功加入資料"
		except Exception as e:
			pass

		return Famcy.UpdateAlert(alert_message=msg)
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

	def get_default_date_time(self):
        current_time = datetime.datetime.now()

        default_date = ""
        default_date += str(current_time.year) + "-"
        default_date += str(current_time.month) + "-" if len(str(current_time.month)) == 2 else "0" + str(current_time.month) + "-"
        default_date += str(current_time.day) if len(str(current_time.day)) == 2 else "0" + str(current_time.day)

        default_end_date = ""
        default_end_date += str(current_time.year) + "-"
        default_end_date += str(current_time.month) + "-" if len(str(current_time.month)) == 2 else "0" + str(current_time.month) + "-"
        default_end_date += str(int(current_time.day)+1) if len(str(int(current_time.day)+1)) == 2 else "0" + str(int(current_time.day)+1)

        return default_date, "00:00", default_end_date, "00:00"
	# ====================================================
	# ====================================================
   

page = SeasonPage()
page.register()