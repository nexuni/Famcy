import Famcy
import os
import json
import requests
import datetime

class CarManagementPage(Famcy.FamcyPage):
    def __init__(self):
        super(CarManagementPage, self).__init__()

        self.car_queue_info = []
        self.carpark_id = "park1"
        self.entry_station = "E1"
        self.save_searching_data = {}

        self.del_card = self.prompt_delete()
        self.insert_card = self.prompt_insert()

        self.layout.addStaticWidget(self.del_card, 40)
        self.layout.addStaticWidget(self.insert_card, 40)


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

        verify_mode = Famcy.inputList()
        verify_mode.update({
                "title": "輸入車牌狀態",
                "value": ["尚未驗證", "已驗證"],
                "action_after_post": "clean"
            })


        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.update_selected_car, target=card1)

        new_btn = Famcy.submitBtn()
        new_btn.update({"title": "新增"})
        new_btn.connect(self.prompt_submit_input, target=self.insert_card)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        input_form.layout.addWidget(input_license, 1, 0)
        input_form.layout.addWidget(verify_mode, 1, 1)

        input_form.layout.addWidget(new_btn, 0, 4)
        input_form.layout.addWidget(search_btn, 1, 4)

        card1.layout.addWidget(input_form, 0, 0)

        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()
        self.car_block_list = []
        col_num = 4
        for i in range(100):
            input_form = Famcy.input_form()
            input_form.body.style["border"] = "1px solid black"
            input_form.body.style["max-width"] = str(100/col_num) + "vw"

            car_pic = Famcy.displayImage()
            car_pic.update({"title": ""})

            license_num = Famcy.pureInput()
            license_num.update({"title":"車牌號碼", "input_type":"text"})

            input_date = Famcy.pureInput()
            input_time = Famcy.pureInput()
            input_date.update({"title": "輸入起始日期", "input_type": "date"})
            input_time.update({"title": "輸入起始時間", "input_type": "time"})

            update_btn = Famcy.submitBtn()
            update_btn.update({"title":"修改車牌"})
            update_btn.connect(self.modify_platenum, target=card2)

            submit_btn = Famcy.submitBtn()
            submit_btn.update({"title":"車牌正確"})
            submit_btn.connect(self.submit_platenum, target=card2)

            update_time_btn = Famcy.submitBtn()
            update_time_btn.update({"title":"修改進場時間"})
            update_time_btn.connect(self.modify_time, target=card2)

            delete_btn = Famcy.submitBtn()
            delete_btn.update({"title":"刪除車牌"})
            delete_btn.connect(self.prompt_submit_input, target=self.del_card)

            input_form.layout.addWidget(car_pic, 0, 0, 1, 2)
            input_form.layout.addWidget(license_num, 1, 0, 1, 2)
            input_form.layout.addWidget(input_date, 2, 0, 1, 2)
            input_form.layout.addWidget(input_time, 3, 0, 1, 2)
            input_form.layout.addWidget(update_btn, 4, 0)
            input_form.layout.addWidget(submit_btn, 4, 1)
            input_form.layout.addWidget(update_time_btn, 5, 0)
            input_form.layout.addWidget(delete_btn, 5, 1)

            self.car_block_list.append(input_form)

        self.generate_car_block(card2, init=True)
        
        return card2
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def prompt_insert(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        license_num = Famcy.pureInput()
        license_num.update({"title":"車牌號碼", "input_type":"text"})

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time"})

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_insert, target=p_card)

        input_form.layout.addWidget(license_num, 0, 0, 1, 2)
        input_form.layout.addWidget(input_date, 1, 0)
        input_form.layout.addWidget(input_time, 1, 1)
        input_form.layout.addWidget(cancel_btn, 2, 0)
        input_form.layout.addWidget(submit_btn, 2, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def prompt_delete(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        text_msg = Famcy.displayParagraph()
        text_msg.update({"title": "確認是否刪除車牌?", "content": ""})

        confirm_btn = Famcy.submitBtn()
        confirm_btn.update({"title":"確認"})
        confirm_btn.connect(self.update_delete)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"取消"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(text_msg, 0, 0, 1, 2)
        input_form.layout.addWidget(confirm_btn, 1, 0)
        input_form.layout.addWidget(cancel_btn, 1, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def prompt_remove_input(self, submission_obj, info_list):
        return Famcy.UpdateRemoveElement(prompt_flag=True)

    def prompt_submit_input(self, submission_obj, info_list):
        submission_obj.target.last_card = submission_obj.origin
        return Famcy.UpdatePrompt()

    def update_selected_car(self, submission_obj, info_list):
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            license_num = str(info_list[4][0])
            verify_mode = str(info_list[5][0])
            if verify_mode == "尚未驗證":
                verify_mode = 'True'
            else:
                verify_mode = 'False'
            self.get_car_queue(verify_mode=verify_mode, start_time=start_time, end_time=end_time, platenum=license_num)
            self.generate_car_block(self.card_2)
            return Famcy.UpdateBlockHtml(target=self.card_2)

        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

    def update_insert(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        if len(info_list[0]) > 0 and len(info_list[1]) > 0 and len(info_list[2]) > 0:
            license_num = str(info_list[0][0])
            time_num = info_list[1][0][2:4] + info_list[1][0][5:7] + info_list[1][0][8:10] + info_list[2][0][:2] + info_list[2][0][3:] + "00000"
            modified_time = self.generate_modified_time()

            if self.post_insert(license_num, time_num, modified_time):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                msg = "成功加入資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

    def update_delete(self, submission_obj, info_list):
        msg = "系統異常，請重新再試"
        modified_time = submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard").last_card.value["modified_time"]
        if self.post_update("XXXXXX", modified_time):
            self.get_car_queue()
            self.generate_car_block(self.card_2)
            msg = "成功刪除資料"

        return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdateBlockHtml(target=self.card_2), Famcy.UpdateAlert(alert_message=msg, target=self.card_2)]

    def submit_platenum(self, submission_obj, info_list):
        msg = "系統異常，請重新再試"
        if len(info_list[0]) > 0:
            license_num = str(info_list[0][0])
            modified_time = submission_obj.origin.value["modified_time"]

            if self.post_update(license_num, modified_time, comments="checked"):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                msg = "成功確認資料"

        return [Famcy.UpdateBlockHtml(), Famcy.UpdateAlert(alert_message=msg)]

    def modify_platenum(self, submission_obj, info_list):
        msg = "系統異常，請重新再試"
        if len(info_list[0]) > 0:
            license_num = str(info_list[0][0])
            modified_time = submission_obj.origin.value["modified_time"]

            if self.post_update(license_num, modified_time):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                msg = "成功修改資料"

        return [Famcy.UpdateBlockHtml(), Famcy.UpdateAlert(alert_message=msg)]

    def modify_time(self, submission_obj, info_list):
        msg = "系統異常，請重新再試"
        if len(info_list[0]) > 0:
            license_num = submission_obj.origin.value["platenum"]
            modified_time = submission_obj.origin.value["modified_time"]
            entry_time = info_list[1][0][2:4] + info_list[1][0][5:7] + info_list[1][0][8:10] + info_list[2][0][:2] + info_list[2][0][3:] + "00000"

            if self.post_update(license_num, modified_time, entry_time=entry_time):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                msg = "成功修改資料"

        return [Famcy.UpdateBlockHtml(), Famcy.UpdateAlert(alert_message=msg)]
    # ====================================================
    # ====================================================


    # http request function
    # ====================================================
    def get_car_queue(self, verify_mode=None, start_time=None, end_time=None, platenum=None):
        if verify_mode:
            self.save_searching_data["verify_mode"] = verify_mode
        elif "verify_mode" not in self.save_searching_data.keys():
            self.save_searching_data["verify_mode"] = 'True'

        send_dict = {
            "service": "pms",
            "operation": "get_car_queue",
            "verify_mode": self.save_searching_data["verify_mode"]
        }

        if start_time and len(start_time[2:]) == 15:
            send_dict["start_time"] = start_time[2:]
            self.save_searching_data["start_time"] = start_time[2:]
        elif "start_time" in self.save_searching_data.keys():
            send_dict["start_time"] = self.save_searching_data["start_time"]

        if end_time and len(end_time[2:]) == 15:
            send_dict["end_time"] = end_time[2:]
            self.save_searching_data["end_time"] = end_time[2:]
        elif "end_time" in self.save_searching_data.keys():
            send_dict["end_time"] = self.save_searching_data["end_time"]

        if platenum:
            send_dict["platenum"] = platenum

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

    def post_update(self, license_num, modified_time, comments=None, entry_time=None):
        send_dict = {
            "service": "pms",
            "operation": "update_movement",
            "entry_station": self.entry_station,
            "modified_time": modified_time,
            "platenum": license_num,
            "carpark_id": self.carpark_id
        }

        if comments:
            send_dict["comments"] = comments
        if entry_time:
            send_dict["entry_time"] = entry_time

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
        card.layout.clearWidget()
        col_num = 4
        for i, temp in enumerate(self.car_queue_info, start=1):
            if i < len(self.car_block_list):
                input_form = self.car_block_list[i]

                input_form.layout.content[0][0].update({"img_name": ["/asset/image" + temp["car_image"]]})
                input_form.layout.content[1][0].update({"defaultValue": temp["platenum"]})
                input_form.layout.content[2][0].update({"defaultValue": "20"+temp["entry_time"][:2]+"-"+temp["entry_time"][2:4]+"-"+temp["entry_time"][4:6]})
                input_form.layout.content[3][0].update({"defaultValue": temp["entry_time"][6:8]+":"+temp["entry_time"][8:10]})
                
                input_form.layout.content[4][0].update({"modified_time": temp["modified_time"]})
                input_form.layout.content[5][0].update({"modified_time": temp["modified_time"]})
                input_form.layout.content[6][0].update({"platenum": temp["platenum"], "modified_time": temp["modified_time"]})
                input_form.layout.content[7][0].update({"modified_time": temp["modified_time"]})

                card.layout.addWidget(input_form, ((i-1)//col_num)*2, (i-1)%col_num)
            else:
                break


    def generate_modified_time(self):
        modified_time = ""
        current_time = datetime.datetime.now()
        modified_time += str(current_time.year)[2:]
        modified_time += str(current_time.month) if len(str(current_time.month)) == 2 else "0" + str(current_time.month)
        modified_time += str(current_time.day) if len(str(current_time.day)) == 2 else "0" + str(current_time.day)
        modified_time += str(current_time.hour) if len(str(current_time.hour)) == 2 else "0" + str(current_time.hour)
        modified_time += str(current_time.minute) if len(str(current_time.minute)) == 2 else "0" + str(current_time.minute)
        modified_time += "00000"

        return modified_time

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

   

# page = CarManagementPage()
CarManagementPage.register("/car_management", Famcy.ClassicStyle(), background_thread=False)