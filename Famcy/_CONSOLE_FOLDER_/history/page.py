import Famcy
import os
import json
import requests
import datetime

class CarManagementPage(Famcy.FamcyPage):
    def __init__(self):
        super(CarManagementPage, self).__init__("/car_management", Famcy.ClassicSideStyle(), background_thread=False)

        self.car_queue_info = []
        self.carpark_id = "park1"
        self.entry_station = "E1"

        self.del_card = self.prompt_delete()
        self.insert_card = self.prompt_insert()

        self.layout.addPromptWidget(self.del_card, 40)
        self.layout.addPromptWidget(self.insert_card, 40)


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

        verify_mode = Famcy.inputList()
        verify_mode.update({
                "title": "輸入車牌狀態",
                "value": ["True", "False"],
                "action_after_post": "clean"
            })


        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.update_selected_car, target=card1)

        new_btn = Famcy.submitBtn()
        new_btn.update({"title": "新增"})
        new_btn.connect(self.prompt_submit_input, target=self.insert_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title": "刪除"})
        cancel_btn.connect(self.prompt_submit_input, target=self.del_card)

        input_form.layout.addWidget(input_year, 0, 0)
        input_form.layout.addWidget(input_month, 0, 1)
        input_form.layout.addWidget(input_date, 0, 2)
        input_form.layout.addWidget(input_time, 0, 3)
        input_form.layout.addWidget(input_year2, 1, 0)
        input_form.layout.addWidget(input_month2, 1, 1)
        input_form.layout.addWidget(input_date2, 1, 2)
        input_form.layout.addWidget(input_time2, 1, 3)
        input_form.layout.addWidget(input_license, 2, 0, 1, 2)
        input_form.layout.addWidget(verify_mode, 2, 2, 1, 2)

        input_form.layout.addWidget(search_btn, 0, 4)
        input_form.layout.addWidget(new_btn, 1, 4)
        input_form.layout.addWidget(cancel_btn, 2, 4)

        card1.layout.addWidget(input_form, 0, 0)

        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()
        card2.preload = lambda: self.generate_car_block(card2, init=True)
        
        return card2
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def prompt_insert(self):
        p_card = Famcy.FamcyCard()

        input_form = Famcy.input_form()

        license_num = Famcy.pureInput()
        license_num.update({"title":"車牌號碼", "input_type":"text"})

        time_num = Famcy.pureInput()
        time_num.update({"title":"時間", "input_type":"number"})

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_insert, target=p_card)

        input_form.layout.addWidget(license_num, 0, 0, 1, 2)
        input_form.layout.addWidget(time_num, 1, 0, 1, 2)
        input_form.layout.addWidget(cancel_btn, 2, 0)
        input_form.layout.addWidget(submit_btn, 2, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def prompt_delete(self):
        p_card = Famcy.FamcyCard()

        input_form = Famcy.input_form()

        license_num = Famcy.pureInput()
        license_num.update({"title":"車牌號碼", "input_type":"text"})

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_delete, target=p_card)

        input_form.layout.addWidget(license_num, 0, 0, 1, 2)
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
        print("========= info_list: ", info_list)
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = str(info_list[0][0]) + str(info_list[1][0]) + str(info_list[2][0]) + str(info_list[3][0]) + "0000000"
            end_time = str(info_list[4][0]) + str(info_list[5][0]) + str(info_list[6][0]) + str(info_list[7][0]) + "0000000"
            license_num = str(info_list[8][0])
            verify_mode = str(info_list[9][0])

            self.get_car_queue(verify_mode=verify_mode, start_time=start_time, end_time=end_time, platenum=license_num)
            self.generate_car_block(self.card_2)
            return Famcy.UpdateBlockHtml(target=self.card_2)

        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

    def update_insert(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        if len(info_list[0]) > 0 and len(info_list[1]) > 0 and len(info_list[1][0]) == 15:
            license_num = str(info_list[0][0])
            time_num = str(info_list[1][0])

            modified_time = ""
            current_time = datetime.datetime.now()
            modified_time += str(current_time.year)[2:]
            modified_time += str(current_time.month) if len(str(current_time.month)) == 2 else "0" + str(current_time.month)
            modified_time += str(current_time.day) if len(str(current_time.day)) == 2 else "0" + str(current_time.day)
            modified_time += str(current_time.hour) if len(str(current_time.hour)) == 2 else "0" + str(current_time.hour)
            modified_time += str(current_time.minute) if len(str(current_time.minute)) == 2 else "0" + str(current_time.minute)
            modified_time += "00000"

            if self.post_insert(license_num, time_num, modified_time):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                msg = "成功加入資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

    def update_delete(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        if len(info_list[0]) > 0:
            license_num = str(info_list[0][0])

            modified_time = ""
            current_time = datetime.datetime.now()
            modified_time += str(current_time.year)[2:]
            modified_time += str(current_time.month) if len(str(current_time.month)) == 2 else "0" + str(current_time.month)
            modified_time += str(current_time.day) if len(str(current_time.day)) == 2 else "0" + str(current_time.day)
            modified_time += str(current_time.hour) if len(str(current_time.hour)) == 2 else "0" + str(current_time.hour)
            modified_time += str(current_time.minute) if len(str(current_time.minute)) == 2 else "0" + str(current_time.minute)
            modified_time += "00000"

            if self.post_delete(license_num, modified_time):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                msg = "成功刪除資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]
    # ====================================================
    # ====================================================


    # http request function
    # ====================================================
    def get_car_queue(self, verify_mode=None, start_time=None, end_time=None, platenum=None):
        send_dict = {
            "service": "pms",
            "operation": "get_car_queue"
        }

        if verify_mode and not verify_mode == "" and not verify_mode == "---":
            send_dict["verify_mode"] = verify_mode
        if start_time and len(start_time[2:]) == 15:
            send_dict["start_time"] = start_time[2:]
        if end_time and len(end_time[2:]) == 15:
            send_dict["end_time"] = end_time[2:]
        if platenum and not platenum == "":
            send_dict["platenum"] = platenum

        print("=====================send_dict: ", send_dict)

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        self.car_queue_info = json.loads(res_msg)["message"] if json.loads(res_msg)["indicator"] else []

    def post_insert(self, license_num, entry_time, modified_time):
        send_dict = {
            "service": "pms",
            "operation": "insert_movement",
            "entry_time": entry_time,
            "modified_time": modified_time,
            "platenum": license_num,
            "carpark_id": self.carpark_id
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]

    def post_delete(self, license_num, modified_time):
        send_dict = {
            "service": "pms",
            "operation": "update_movement",
            "entry_station": self.entry_station,
            "modified_time": modified_time,
            "platenum": license_num,
            "carpark_id": self.carpark_id
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]

    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def generate_car_block(self, card, init=False):

        if init:
            self.get_car_queue()

        # generate blocks
        card.layout.content = []
        col_num = 4
        for i, temp in enumerate(self.car_queue_info, start=1):
            input_form = Famcy.input_form()
            input_form.body.style["border"] = "1px solid black"
            input_form.body.style["max-width"] = str(100/col_num) + "vw"

            car_pic = Famcy.displayImage()
            car_pic.update({
                    "title": "",
                    "img_name": ["/asset/image" + temp["car_image"]]
                })

            license_num = Famcy.pureInput()
            license_num.update({"title":"車牌號碼", "input_type":"text", "placeholder": temp["platenum"]})

            update_btn = Famcy.submitBtn()
            update_btn.update({"title":"修改車牌"})
            # update_btn.connect(self.prompt_submit_input)

            submit_btn = Famcy.submitBtn()
            submit_btn.update({"title":"車牌正確"})
            # submit_btn.connect(self.prompt_submit_input)

            input_form.layout.addWidget(car_pic, 0, 0, 1, 2)
            input_form.layout.addWidget(license_num, 1, 0, 1, 2)
            input_form.layout.addWidget(update_btn, 2, 0)
            input_form.layout.addWidget(submit_btn, 2, 1)

            card.layout.addWidget(input_form, ((i-1)//col_num)*2, (i-1)%col_num)
    # ====================================================
    # ====================================================

   

page = CarManagementPage()
page.register()