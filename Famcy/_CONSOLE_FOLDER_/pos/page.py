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
        self.receipt_num_card = self.prompt_receipt_number()
        self.receipt_card = self.prompt_receipt()
        self.month_card = self.prompt_month()
        
        self.layout.addStaticWidget(self.fee_card, 40)
        self.layout.addStaticWidget(self.receipt_num_card, 40)
        self.layout.addStaticWidget(self.receipt_card, 40)
        self.layout.addStaticWidget(self.month_card, 40)

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
        print_btn.update({"title": "補印發票"})
        print_btn.connect(self.prompt_submit_input, target=self.receipt_num_card)

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title": "登記月票並繳費"})
        submit_btn.connect(self.prompt_submit_input, target=self.month_card)

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
    def prompt_fee(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        platenum_tag = Famcy.displayTag()
        platenum_tag.update({
                "title": "車牌號碼: ",
                "content": "-"
            })

        time_tag = Famcy.displayTag()
        time_tag.update({
                "title": "入場時間: ",
                "content": "-"
            })

        price_tag = Famcy.displayTag()
        price_tag.update({
                "title": "應付金額: ",
                "content": "NT$ -"
            })

        input_price_tag = Famcy.pureInput()
        input_price_tag.update({
                "title": "實收金額: "
            })

        change_tag = Famcy.displayTag()
        change_tag.update({
                "title": "找零: ",
                "content": "NT$ -"
            })

        submit_price_btn = Famcy.submitBtn()
        submit_price_btn.update({"title":"確認"})
        submit_price_btn.connect(self.count_change, target=change_tag)

        fee = Famcy.inputList()
        fee.update({
                "title": "選擇付款方式",
                "value": ["cash", "yoyo"]
            })

        comments = Famcy.pureInput()
        comments.update({"title":"備註:", "input_type":"text"})

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.switch_to_receipt_page)

        input_form.layout.addWidget(platenum_tag, 0, 0, 1, 4)
        input_form.layout.addWidget(time_tag, 1, 0, 1, 4)
        input_form.layout.addWidget(price_tag, 2, 0, 1, 4)
        input_form.layout.addWidget(input_price_tag, 3, 0, 1, 3)
        input_form.layout.addWidget(submit_price_btn, 3, 3)
        input_form.layout.addWidget(change_tag, 4, 0, 1, 4)
        input_form.layout.addWidget(fee, 5, 0, 1, 4)
        input_form.layout.addWidget(comments, 6, 0, 1, 4)
        input_form.layout.addWidget(cancel_btn, 7, 0, 1, 2)
        input_form.layout.addWidget(submit_btn, 7, 2, 1, 2)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def prompt_receipt_number(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        receipt_id = Famcy.pureInput()
        receipt_id.update({"title":"發票號碼:"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        # submit_btn.connect(self.update_fee, target=p_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(receipt_id, 0, 0, 1, 2)
        input_form.layout.addWidget(cancel_btn, 1, 0)
        input_form.layout.addWidget(submit_btn, 1, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def prompt_receipt(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        input_platenum = Famcy.displayTag()
        input_platenum.update({"title":"車牌號碼:"})

        input_id = Famcy.pureInput()
        input_id.update({"title":"統一編號:"})

        receipt_type = Famcy.inputList()
        receipt_type.update({"title":"發票種類:", "value": ["normal", "tax", "carrier_num"]})

        receipt_src = Famcy.inputList()
        receipt_src.update({"title":"發票:", "value": ["normal", "cloud_receipt"]})

        vehicle_number = Famcy.pureInput()
        vehicle_number.update({"title":"載具:"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_fee, target=p_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.return_action, target=self.fee_card)

        download_link = Famcy.downloadFile()
        download_link.update({"title": "","file_path": 'http://127.0.0.1:5000/robots.xlsx',"file_name": 'download'})
        download_link.body.children[0]["style"] = "visibility: hidden;"

        input_form.layout.addWidget(input_platenum, 0, 0, 1, 2)
        input_form.layout.addWidget(input_id, 1, 0, 1, 2)
        input_form.layout.addWidget(receipt_type, 2, 0, 1, 2)
        input_form.layout.addWidget(receipt_src, 3, 0, 1, 2)
        input_form.layout.addWidget(vehicle_number, 4, 0, 1, 2)
        input_form.layout.addWidget(cancel_btn, 5, 0)
        input_form.layout.addWidget(submit_btn, 5, 1)

        input_form.layout.addWidget(download_link, 6, 0)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def prompt_month(self):
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

    # def prompt_receipt_submit_input(self, submission_obj, info_list):
    #     flag = True
    #     for _ in info_list:
    #         if not len(_) > 0:
    #             flag = False
    #             break
    #     if flag:
    #         platenum = info_list[4][0]
    #         self.receipt_card.layout.content[0][0].layout.content[0][0].update({"content": platenum})
    #     self.receipt_card.layout.content[0][0].layout.content[4][0].connect(self.prompt_remove_input)
    #     return Famcy.UpdatePrompt()

    def submit_car_info(self, submission_obj, info_list):
        if len(info_list[0]) > 0 and len(info_list[1]) > 0 and len(info_list[2]) > 0:
            license_num = str(info_list[0][0])
            entry_time = info_list[1][0][2:4] + info_list[1][0][5:7] + info_list[1][0][8:10] + info_list[2][0][:2] + info_list[2][0][3:] + "00000"

            if self.post_calculate_fee(license_num, entry_time):
                self.fee_card.layout.content[0][0].layout.content[8][0].connect(self.prompt_remove_input)
                return Famcy.UpdatePrompt()

        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試", target=self.card_2)

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

            self.get_car_queue(start_time=start_time, end_time=end_time, platenum=license_num)
            self.generate_car_block(self.card_2)
            return Famcy.UpdateBlockHtml(target=self.card_2)

        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

    def update_fee(self, submission_obj, info_list):
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            platenum = self.fee_card.layout.content[0][0].layout.content[0][0].value["content"]
            entry_time = self.fee_card.layout.content[0][0].layout.content[1][0].value["content"]
            receipt_fee = self.fee_card.layout.content[0][0].layout.content[2][0].value["content"][4:]
            buyer_taxnum = info_list[0][0]
            receipt_type = info_list[1][0]
            receipt_source = info_list[2][0]
            vehicle_number = info_list[3][0]

            ind, loc = self.post_generate_receipt(platenum, entry_time, receipt_fee, buyer_taxnum, receipt_type, receipt_source, vehicle_number)
            if ind:
                if loc:
                    extra_script = "document.getElementById('" + self.receipt_card.layout.content[0][0].layout.content[7][0].id + "_input').click();"
                    return [Famcy.UpdateBlockHtml(target=self.receipt_card)]
                return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdateAlert(alert_message="發票成功列印", target=self.card_1)]
        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

    def switch_to_receipt_page(self, submission_obj, info_list):
        self.receipt_card.layout.content[0][0].layout.content[4][0].connect(self.return_action, target=self.fee_card)
        return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdatePrompt(target=self.receipt_card)]

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
                msg = "成功加入資料"
                self.fee_card.layout.content[0][0].layout.content[8][0].connect(self.return_action, target=self.month_card)
                self.fee_card.layout.content[0][0].layout.content[0][0].update({"content": license_num})
                self.fee_card.layout.content[0][0].layout.content[1][0].update({"content": start_num})
                self.fee_card.layout.content[0][0].layout.content[2][0].update({"content": "NT$ "+month_fee})

                return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdatePrompt(target=self.fee_card)]

        return Famcy.UpdateAlert(alert_message=msg)

    def count_change(self, submission_obj, info_list):
        if len(info_list[0]) > 0:
            total_price = int(self.fee_card.layout.content[0][0].layout.content[2][0].value["content"][4:])
            input_price = int(info_list[0][0])

            self.fee_card.layout.content[0][0].layout.content[5][0].update({"content": "NT$ "+str(input_price-total_price)})
            return Famcy.UpdateBlockHtml()
        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試", target=self.fee_card)

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
        return json.loads(res_msg)["indicator"]

    def post_calculate_fee(self, platenum, entry_time):
        send_dict = {
            "service": "pms",
            "operation": "calculate_fee",
            "platenum": platenum,
            "entry_time": entry_time
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        self.receipt_card.layout.content[0][0].layout.content[0][0].update({"content": platenum})
        self.fee_card.layout.content[0][0].layout.content[0][0].update({"content": platenum})
        self.fee_card.layout.content[0][0].layout.content[1][0].update({"content": entry_time})
        self.fee_card.layout.content[0][0].layout.content[2][0].update({"content": "NT$ "+json.loads(json.loads(res_msg)["message"][0])["parkingfee"]})
        print("json.loads(res_msg): ", json.loads(res_msg))
        return json.loads(res_msg)["indicator"]

    def post_generate_receipt(self, platenum, entry_time, receipt_fee, buyer_taxnum=None, receipt_type=None, receipt_source=None, vehicle_number=None):
        send_dict = {
            "service": "pms",
            "operation": "generate_receipt",
            "platenum": platenum,
            "entry_time": entry_time,
            "receipt_time": self.generate_modified_time(),
            "receipt_fee": receipt_fee
        }

        if buyer_taxnum:
            send_dict["buyer_taxnum"] = buyer_taxnum
        if receipt_type:
            send_dict["receipt_type"] = receipt_type
        if receipt_source:
            send_dict["receipt_source"] = receipt_source
        if vehicle_number:
            send_dict["vehicle_number"] = vehicle_number

        location_flag = False
        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        print("res_msg: ", res_msg)
        if "location" in json.loads(res_msg).keys() and json.loads(res_msg)["location"] and len(json.loads(res_msg)["location"]) > 0:
            location_flag = True
            self.receipt_card.layout.content[0][0].layout.content[7][0].update({"file_path": json.loads(res_msg)["location"]})
        return json.loads(res_msg)["indicator"], location_flag

    def get_car_queue(self, start_time=None, end_time=None, platenum=None):
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
            input_form = Famcy.input_form()
            input_form.body.style["border"] = "1px solid black"
            input_form.body.style["max-width"] = str(100/col_num) + "vw"

            car_pic = Famcy.displayImage()
            car_pic.update({
                    "title": "",
                    "img_name": ["/asset/image" + temp["car_image"]]
                })

            license_num = Famcy.pureInput()
            license_num.update({"title":"車牌號碼", "input_type":"text", "defaultValue": temp["platenum"]})

            input_date = Famcy.pureInput()
            input_time = Famcy.pureInput()
            input_date.update({"title": "輸入起始日期", "input_type": "date", "defaultValue": "20"+temp["entry_time"][:2]+"-"+temp["entry_time"][2:4]+"-"+temp["entry_time"][4:6]})
            input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": temp["entry_time"][6:8]+":"+temp["entry_time"][8:10]})

            update_btn = Famcy.submitBtn()
            update_btn.update({"title":"修改車牌", "modified_time": temp["modified_time"]})
            update_btn.connect(self.modify_platenum, target=card)

            update_time_btn = Famcy.submitBtn()
            update_time_btn.update({"title":"修改進場時間", "platenum": temp["platenum"], "modified_time": temp["modified_time"]})
            update_time_btn.connect(self.modify_time, target=card)

            submit_btn = Famcy.submitBtn()
            submit_btn.update({"title":"前往繳費"})
            submit_btn.connect(self.submit_car_info, target=self.fee_card)

            input_form.layout.addWidget(car_pic, 0, 0, 1, 2)
            input_form.layout.addWidget(license_num, 1, 0, 1, 2)
            input_form.layout.addWidget(input_date, 2, 0, 1, 2)
            input_form.layout.addWidget(input_time, 3, 0, 1, 2)
            input_form.layout.addWidget(update_btn, 4, 0)
            input_form.layout.addWidget(update_time_btn, 4, 1)
            input_form.layout.addWidget(submit_btn, 5, 0, 1, 2)

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