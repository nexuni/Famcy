import Famcy
import os
import json
import requests
import datetime

class PosPage(Famcy.FamcyPage):
    def __init__(self):
        super(PosPage, self).__init__("/pos", Famcy.ClassicSideStyle(), background_thread=False)

        self.car_queue_info = []
        self.carpark_id = "park1"
        self.entry_station = "E1"

        self.fee_card = self.prompt_fee()
        self.pos_card = self.prompt_pos()
        # self.insert_card = self.prompt_insert()
        
        self.layout.addPromptWidget(self.fee_card, 40)
        self.layout.addPromptWidget(self.pos_card, 40)
        # self.layout.addPromptWidget(self.insert_card, 40)

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

        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.update_selected_car, target=card1)

        print_btn = Famcy.submitBtn()
        print_btn.update({"title": "印發票"})
        # print_btn.connect(self.prompt_submit_input, target=self.insert_card)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title": "送出車牌"})
        submit_btn.connect(self.submit_car_block, target=self.pos_card)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        input_form.layout.addWidget(input_license, 1, 0)
        
        input_form.layout.addWidget(submit_btn, 1, 1)
        input_form.layout.addWidget(print_btn, 1, 2)
        input_form.layout.addWidget(search_btn, 1, 3)

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
    def prompt_pos(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        license_num = Famcy.pureInput()
        license_num.update({"title":"車牌號碼", "input_type":"text"})

        date_num = Famcy.pureInput()
        date_num.update({"title":"日期", "input_type":"date"})

        time_num = Famcy.pureInput()
        time_num.update({"title":"時間", "input_type":"time"})

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_pos, target=self.fee_card)

        input_form.layout.addWidget(license_num, 0, 0, 1, 2)
        input_form.layout.addWidget(date_num, 1, 0, 1, 2)
        input_form.layout.addWidget(time_num, 2, 0, 1, 2)
        input_form.layout.addWidget(cancel_btn, 3, 0)
        input_form.layout.addWidget(submit_btn, 3, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def prompt_fee(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        fee = Famcy.inputList()
        fee.update({
                "title": "選擇付款方式",
                "value": ["cash", "yoyo"]
            })

        comments = Famcy.pureInput()
        comments.update({"title":"備註:", "input_type":"text"})

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.return_action)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        # submit_btn.connect(self.update_pos, target=self.fee_card)

        input_form.layout.addWidget(fee, 0, 0, 1, 2)
        input_form.layout.addWidget(comments, 1, 0, 1, 2)
        input_form.layout.addWidget(cancel_btn, 2, 0)
        input_form.layout.addWidget(submit_btn, 2, 1)

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

    def return_action(self, submission_obj, info_list):
        return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdatePrompt()]

    def prompt_car_block(self, submission_obj, info_list):
        input_form = submission_obj.origin.find_parent(submission_obj.origin, "input_form")

        license = str(input_form.layout.content[1][0].value["content"])
        time = str(input_form.layout.content[2][0].value["content"])

        self.pos_card.layout.content[0][0].layout.content[0][0].update({"placeholder": license})
        self.pos_card.layout.content[0][0].layout.content[1][0].update({"defaultValue": "20"+time[:2]+"-"+time[2:4]+"-"+time[4:6]})
        self.pos_card.layout.content[0][0].layout.content[2][0].update({"defaultValue": time[6:8]+":"+time[8:10]})

        return Famcy.UpdatePrompt()

    def submit_car_block(self, submission_obj, info_list):
        print("info_list: ", info_list)
        input_form = submission_obj.origin.find_parent(submission_obj.origin, "input_form")

        license = str(info_list[4][0])
        self.pos_card.layout.content[0][0].layout.content[0][0].update({"placeholder": license})

        return Famcy.UpdatePrompt()

    def update_selected_car(self, submission_obj, info_list):
        print("========= info_list: ", info_list)
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            license_num = str(info_list[4][0])

            self.get_car_queue(start_time=start_time, end_time=end_time, platenum=license_num)
            self.generate_car_block(self.card_2)
            return Famcy.UpdateBlockHtml(target=self.card_2)

        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

    def update_pos(self, submission_obj, info_list):
        last_p_card = submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard")
        self.fee_card.layout.content[0][0].layout.content[2][0].connect(self.return_action,target=last_p_card)

        if len(info_list[0]) > 0 and len(info_list[1]) > 0 and len(info_list[2]) > 0:
            license_num = str(info_list[0][0])
            modified_time = info_list[1][0][2:4] + info_list[1][0][5:7] + info_list[1][0][8:10] + info_list[2][0][:2] + info_list[2][0][3:] + "00000"

            if self.post_update_movement(license_num, modified_time):
                self.get_car_queue()
                self.generate_car_block(self.card_2)
                return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdatePrompt()]

            else:
                return Famcy.UpdateAlert(alert_message="系統異常，請重新再試", target=self.pos_card)

    # ====================================================
    # ====================================================


    # http request function
    # ====================================================
    def post_update_movement(self, platenum, modified_time):
        send_dict = {
            "service": "pms",
            "operation": "update_movement",
            "carpark_id": self.carpark_id,
            "entry_station": self.entry_station,
            "platenum": platenum,
            "modified_time": modified_time
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]


    def get_car_queue(self, start_time=None, end_time=None, platenum=None):
        # TODO: API need to be changed
        send_dict = {
            "service": "pms",
            "operation": "get_car_queue"
        }

        if start_time and len(start_time[2:]) == 15:
            send_dict["start_time"] = start_time[2:]
        if end_time and len(end_time[2:]) == 15:
            send_dict["end_time"] = end_time[2:]
        if platenum and not platenum == "":
            send_dict["platenum"] = platenum

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        self.car_queue_info = json.loads(res_msg)["message"] if json.loads(res_msg)["indicator"] else []

        print("res_msg: ", res_msg)

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

            license_num = Famcy.displayTag()
            license_num.update({"title":"車牌號碼", "content": temp["platenum"]})

            time_num = Famcy.displayTag()
            time_num.update({"title":"進場時間", "content": temp["modified_time"]})

            submit_btn = Famcy.submitBtn()
            submit_btn.update({"title":"送出車牌"})
            submit_btn.connect(self.prompt_car_block, target=self.pos_card)

            input_form.layout.addWidget(car_pic, 0, 0)
            input_form.layout.addWidget(license_num, 1, 0)
            input_form.layout.addWidget(time_num, 2, 0)
            input_form.layout.addWidget(submit_btn, 3, 0)

            card.layout.addWidget(input_form, ((i-1)//col_num)*2, (i-1)%col_num)

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

   

page = PosPage()
page.register()