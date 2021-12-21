import Famcy
import os
import json
import requests

class VideoStream(Famcy.FamcyPage):
    def __init__(self):
        super(VideoStream, self).__init__("/ipcam", Famcy.VideoStreamStyle("/ipcam"))

v1 = VideoStream()
v1.register()

class BackgroundTaskCoin(Famcy.FamcyPage):
    def __init__(self):
        super(BackgroundTaskCoin, self).__init__("/BackgroundTaskCoin", Famcy.APIStyle())

class OverviewPage(Famcy.FamcyPage):
    def __init__(self):
        super(OverviewPage, self).__init__("/overview", Famcy.ClassicSideStyle(), background_thread=True, background_freq=0.2)

        # for declaration
        # ===============
        self.table_info = []
        self.total_lots = '0'
        self.total_occupied_lots = '0'
        self.h50 = ''
        self.h10 = ''
        self.h5 = ''
        self.printed_receipt = '0'
        self.carpark_id = ''
        self.carpark_id_ = ''
        self.device_btn_list = self.get_device_configs()
        self.error_msg = ''

        self.prompt_info = {"apm": {}, "station": {}, "ipcam": {}, "led": {}, "update_info": {}, "confirm": {}}

        self.confirm_card = self.confirm_block()
        self.apm_card = self.prompt_apm()
        self.station_card = self.prompt_station()
        self.ipcam_card = self.prompt_ipcam()
        self.led_card = self.prompt_led()
        self.p_edit = self.prompt_update_info()

        self.layout.addStaticWidget(self.confirm_card, 30)
        self.layout.addStaticWidget(self.apm_card, 50)
        self.layout.addStaticWidget(self.station_card, 50)
        self.layout.addStaticWidget(self.ipcam_card, 50)
        self.layout.addStaticWidget(self.led_card, 50)
        self.layout.addStaticWidget(self.p_edit, 60)

        # for parking_lots_remaining
        self.card_1 = self.card1()
        # for device setting
        self.card_2 = self.card2()
        # for table
        self.card_3 = self.card3()
        # for picture
        self.card_4 = self.card4()

        self.layout.addWidget(self.card_1, 0, 0, 1, 4)
        self.layout.addWidget(self.card_2, 0, 4, 1, 6)
        self.layout.addWidget(self.card_3, 1, 0, 3, 7)
        self.layout.addWidget(self.card_4, 1, 7, 3, 3)

        self.thread_update_msg = Famcy.FamcyBackgroundTask(self)
        self.thread_update_device_btn = Famcy.FamcyBackgroundTask(self)
        self.thread_update_table = Famcy.FamcyBackgroundTask(self)

    # background task function 
    # ====================================================
    def background_thread_inner(self):
        """
        This is the inner loop of 
        the background thread. 
        """
        # def update_msg_action(submission_obj, info_list):
        #     self.get_error_msg()
        #     # return Famcy.UpdateBlockHtml()

        # def update_device_btn_action(submission_obj, info_list):
        #     self.get_error_msg()
        #     # return Famcy.UpdateBlockHtml()

        # def update_table_action(submission_obj, info_list):
        #     _ = self.get_device_configs()
        #     # return Famcy.UpdateBlockHtml()

        # self.thread_update_msg.associate(update_msg_action, info_dict={}, target=self.card_2.layout.content[1][0])
        # Famcy.FamcyBackgroundQueue.add(self.thread_update_msg, Famcy.FamcyPriority.Standard)

        # # self.thread_update_device_btn.associate(update_device_btn_action, info_dict={}, target=self.card_2.layout.content[0][0])
        # # self.ws.send_to_websocket(self.thread_update_device_btn.tojson())
        # # Famcy.FamcyBackgroundQueue.add(self.thread_update_device_btn, Famcy.FamcyPriority.Standard)

        # self.thread_update_table.associate(update_table_action, info_dict={}, target=self.card_3.layout.content[0][0].layout.content[0][0])
        # Famcy.FamcyBackgroundQueue.add(self.thread_update_table, Famcy.FamcyPriority.Standard)
        pass

    def update_info_action(self, submission_obj, info_list):
        self.get_hopper_available_lot()

    def add_task_coin(self, action, info_dict, target):
        self.thread_update_info.associate(action, info_dict=info_dict, target=target)
        Famcy.FamcyBackgroundQueue.add(self.thread_update_info, Famcy.FamcyPriority.Standard)
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card1(self):
        card1 = Famcy.FamcyCard()
        card1.preload = self.get_hopper_available_lot

        input_form = Famcy.input_form()

        parking_lots_remaining = Famcy.displayParagraph()
        parking_lots_remaining.update({
            "title": "車格設定",
            "content":'總車格數: %s<br>總佔位數: %s<br>總空位數: %s'%(str(self.total_lots),str(self.total_occupied_lots),str(int(self.total_lots)-int(self.total_occupied_lots)))
            })

        change_remaining = Famcy.displayParagraph()
        change_remaining.update({
            "title": "零錢設定",
            "content":"50元: %s<br>10元: %s<br>5元: %s"%(self.h50,self.h10,self.h5)})

        receipt_remaining = Famcy.displayParagraph()
        receipt_remaining.update({
            "title": "發票設定",
            "content":"已列印: %s<br>剩餘發票數: %s<br>剩餘號碼: %s"%(self.printed_receipt,str(1400-int(self.printed_receipt)),'0')})

        submit_btn = Famcy.submitBtn()
        submit_btn.body.style["word-break"] = "break-all !important"
        submit_btn.update({"title":"前往修改"})
        submit_btn.connect(self.prompt_submit_input, target=self.p_edit)

        input_form.layout.addWidget(parking_lots_remaining, 0, 0)
        input_form.layout.addWidget(change_remaining, 0, 1)
        input_form.layout.addWidget(receipt_remaining, 0, 2)
        input_form.layout.addWidget(submit_btn, 1, 0, 1, 3)

        card1.layout.addWidget(input_form, 0, 0)

        self.thread_update_info = Famcy.FamcyBackgroundTask(self)
        BTCoin = BackgroundTaskCoin()
        BTCoin.style.setAction(lambda: self.add_task_coin(self.update_info_action, {}, input_form))
        BTCoin.style.setReturnValue(indicator=True, message="add to task")
        BTCoin.register()


        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()
        card2.preload = self.get_error_msg

        input_form = Famcy.input_form()

        config_dict = {"第一收費機":"cash_machine","第二收費機":"cash_machine","第三收費機":"cash_machine"}
        col_num = 3
        for i, temp in enumerate(self.device_btn_list, start=0):
            submit_btn = Famcy.submitBtn()
            submit_btn.update({"title":temp["chinese_name"], "ip":temp["ip"]})

            target = card2
            if temp["type"] == "APM":
                target = self.apm_card
            elif temp["type"] == "STATION":
                target = self.station_card
            elif temp["type"] == "IPCAM":
                target = self.ipcam_card
            elif temp["type"] == "LED":
                target = self.led_card

            submit_btn.connect(self.prompt_submit_input, target=target)

            input_form.layout.addWidget(submit_btn, i//col_num, i%col_num)

        error_msg = Famcy.displayParagraph()
        error_msg.body.style["border"] = "1px solid black"
        error_msg.update({
                "title": "ERROR",
                "content": self.error_msg
            })

        card2.layout.addWidget(input_form, 0, 0)
        card2.layout.addWidget(error_msg, 1, 0)

        return card2

    def card3(self):
        card3 = Famcy.FamcyCard()
        card3.preload = self.get_car_queue

        table_content = Famcy.table_block()
        table_content.update({
                "toolbar": False,
                "input_button": "radio",
                "input_value_col_field": "car_image",
                "page_detail": False,
                "page_detail_content": ["<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>"],
                "page_footer": True,
                "page_footer_detail": {
                    "page_size": 7,
                    "page_list": [7, "all"]
                },
                "column": [[
                    # {
                    #     "title": '停車場ID',
                    #     "field": 'carpark_id',
                    #     "rowspan": 1,
                    #     "align": 'center',
                    #     "valign": 'middle',
                    #     "sortable": True
                    # },
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
                    },
                    {
                        "title": 'img',
                        "field": 'car_image',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True,
                        "visible": False
                    }
                ]],
                "data": self.table_info
          })

        input_form = Famcy.input_form()
        input_form.body.style["word-break"] = "break-all !important"

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"查詢車輛"})
        submit_btn.connect(self.submit_car_img, target=self)

        input_form.layout.addWidget(table_content, 0, 0)
        input_form.layout.addWidget(submit_btn, 1, 0)

        card3.layout.addWidget(input_form, 0, 0)
        return card3 

    def card4(self):
        card4 = Famcy.FamcyCard()

        block1 = Famcy.displayImage()
        block1.update({
            "title": "車牌照片",
            "img_name": ["/asset/image/doday_icon.png"],
            "img_size": ["100%"]
        })
        card4.layout.addWidget(block1, 0, 0)
        return card4
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def prompt_update_info(self):
        pcard = Famcy.FamcyPromptCard()
        pcard["pname"] = "update_info"

        input_form = Famcy.input_form()

        # total_lots_input = Famcy.pureInput()
        # total_lots_input.update({"title":"修改總車格","input_type":"number","num_range":[0,10000],"placeholder":self.total_lots})

        # total_lots_input_submit_btn = Famcy.submitBtn()
        # total_lots_input_submit_btn.update({"title":"送出總車格"})
        # total_lots_input_submit_btn.connect(self.update_total_lot, target=pcard)

        # input_form.layout.addWidget(total_lots_input, 0, 0, 1, 2)
        # input_form.layout.addWidget(total_lots_input_submit_btn, 0, 2)


        occupied_lots_input = Famcy.pureInput()
        occupied_lots_input.update({"title":"修改佔用車格","input_type":"number","num_range":[0,10000],"placeholder":self.total_occupied_lots})

        occupied_lots_input_submit_btn = Famcy.submitBtn()
        occupied_lots_input_submit_btn.update({"title":"送出佔用車格"})
        occupied_lots_input_submit_btn.connect(self.update_occupied_lot, target=pcard)

        input_form.layout.addWidget(occupied_lots_input, 0, 0, 1, 2)
        input_form.layout.addWidget(occupied_lots_input_submit_btn, 0, 2)


        select_coin_type = Famcy.inputList()
        select_coin_type.update({
                "title": "選擇零錢種類",
                "value": ["5", "10", "50"]
            })

        coin_input = Famcy.pureInput()
        coin_input.update({"title":"修改零錢數量","input_type":"number","num_range":[0,10000]})
        select_coin_type.connect(self.update_list, target=coin_input)

        coin_input_submit_btn = Famcy.submitBtn()
        coin_input_submit_btn.update({"title":"送出零錢數量"})
        coin_input_submit_btn.connect(self.update_coin, target=pcard)

        input_form.layout.addWidget(select_coin_type, 1, 0)
        input_form.layout.addWidget(coin_input, 1, 1)
        input_form.layout.addWidget(coin_input_submit_btn, 1, 2)


        # receipt_input = Famcy.pureInput()
        # receipt_input.update({"title":"修改已列印發票數","input_type":"number","num_range":[0,10000],"placeholder":self.printed_receipt})

        receipt_input_submit_btn = Famcy.submitBtn()
        receipt_input_submit_btn.update({"title":"更換發票(歸零)"})
        receipt_input_submit_btn.connect(self.update_receipt,target=pcard)

        # input_form.layout.addWidget(receipt_input, 2, 0, 1, 2)
        input_form.layout.addWidget(receipt_input_submit_btn, 2, 0, 1, 3)


        escape_submit_btn = Famcy.submitBtn()
        escape_submit_btn.update({"title":"返回畫面"})
        escape_submit_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(escape_submit_btn, 3, 0, 1, 3)

        pcard.layout.addWidget(input_form, 0, 0)

        return pcard

    def prompt_apm(self):
        pcard = Famcy.FamcyPromptCard()
        pcard["pname"] = "apm"
        self.prompt_info[pcard["pname"]] = {}

        input_form = Famcy.input_form()

        return_change = Famcy.pureInput()
        return_change.update({"title":"找錢","input_type":"number","num_range":[0,10000]})

        text_msg = Famcy.pureInput()
        text_msg.update({"title":"訊息"})

        submit_change_btn = Famcy.submitBtn()
        submit_change_btn.update({"title":"送出找錢", "confirm_id": "refund"})
        # submit_change_btn.connect(self.update_apm_refund, target=pcard)
        submit_change_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][submit_change_btn.value["confirm_id"]] = {"confirm_msg": "確認是否送出找錢?"}

        submit_msg_btn = Famcy.submitBtn()
        submit_msg_btn.update({"title":"送出訊息", "confirm_id": "display_message"})
        submit_msg_btn.connect(self.update_apm_msg, target=pcard)

        restart_btn = Famcy.submitBtn()
        restart_btn.update({"title":"重新啟動", "confirm_id": "reboot"})
        restart_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][restart_btn.value["confirm_id"]] = {"confirm_msg": "確認是否重新啟動?"}

        escape_submit_btn = Famcy.submitBtn()
        escape_submit_btn.update({"title":"返回畫面"})
        escape_submit_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(return_change, 0, 0, 1, 4)
        input_form.layout.addWidget(text_msg, 1, 0, 1, 4)
        input_form.layout.addWidget(escape_submit_btn, 2, 0)
        input_form.layout.addWidget(submit_change_btn, 2, 1)
        input_form.layout.addWidget(submit_msg_btn, 2, 2)
        input_form.layout.addWidget(restart_btn, 2, 3)

        pcard.layout.addWidget(input_form, 0, 0)

        return pcard

    def prompt_station(self):
        pcard = Famcy.FamcyPromptCard()
        pcard["pname"] = "station"
        self.prompt_info[pcard["pname"]] = {}

        input_form = Famcy.input_form()

        escape_submit_btn = Famcy.submitBtn()
        escape_submit_btn.update({"title":"返回畫面"})
        escape_submit_btn.connect(self.prompt_remove_input)

        restart_btn = Famcy.submitBtn()
        restart_btn.update({"title":"重新啟動", "confirm_id": "reboot"})
        restart_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][restart_btn.value["confirm_id"]] = {"confirm_msg": "確認是否重新啟動?"}

        open_btn = Famcy.submitBtn()
        open_btn.update({"title":"開啟車桿", "confirm_id": "open_barrier"})
        open_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][open_btn.value["confirm_id"]] = {"confirm_msg": "確認是否開啟車桿?"}

        closed_btn = Famcy.submitBtn()
        closed_btn.update({"title":"關閉車桿", "confirm_id": "close_barrier"})
        closed_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][closed_btn.value["confirm_id"]] = {"confirm_msg": "確認是否關閉車桿?"}

        input_form.layout.addWidget(escape_submit_btn, 0, 0)
        input_form.layout.addWidget(restart_btn, 0, 1)
        input_form.layout.addWidget(open_btn, 0, 2)
        input_form.layout.addWidget(closed_btn, 0, 3)

        pcard.layout.addWidget(input_form, 0, 0)

        return pcard

    def prompt_ipcam(self):
        pcard = Famcy.FamcyPromptCard()
        pcard["pname"] = "ipcam"
        self.prompt_info[pcard["pname"]] = {}

        videoStream = Famcy.video_stream()
        videoStream.update({
            "rtsp_address": ["rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"],
            "video_timeout": [15],
            "holder_width": ["100%"],
            "holder_height": ["40vh"],
            "img_path": ["/ipcam"]
        })

        input_form = Famcy.input_form()

        restart_btn = Famcy.submitBtn()
        restart_btn.update({"title":"重新啟動", "confirm_id": "reboot"})
        restart_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][restart_btn.value["confirm_id"]] = {"confirm_msg": "確認是否重新啟動?"}

        escape_submit_btn = Famcy.submitBtn()
        escape_submit_btn.update({"title":"返回畫面"})
        escape_submit_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(escape_submit_btn, 0, 0)
        input_form.layout.addWidget(restart_btn, 0, 1)

        pcard.layout.addWidget(videoStream, 0, 0)
        pcard.layout.addWidget(input_form, 1, 0)

        return pcard

    def prompt_led(self):
        pcard = Famcy.FamcyPromptCard()
        pcard["pname"] = "apm"
        self.prompt_info[pcard["pname"]] = {}

        input_form = Famcy.input_form()

        text_msg = Famcy.inputParagraph()
        text_msg.update({"title":"訊息"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"送出訊息", "confirm_id": "display_message"})
        submit_btn.connect(self.update_led_msg, target=pcard)

        restart_btn = Famcy.submitBtn()
        restart_btn.update({"title":"重新啟動", "confirm_id": "reboot"})
        restart_btn.connect(self.confirm_action, target=self.confirm_card)
        self.prompt_info[pcard["pname"]][restart_btn.value["confirm_id"]] = {"confirm_msg": "確認是否重新啟動?"}

        escape_submit_btn = Famcy.submitBtn()
        escape_submit_btn.update({"title":"返回畫面"})
        escape_submit_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(text_msg, 0, 0, 1, 3)
        input_form.layout.addWidget(escape_submit_btn, 1, 0)
        input_form.layout.addWidget(submit_btn, 1, 1)
        input_form.layout.addWidget(restart_btn, 1, 2)

        pcard.layout.addWidget(input_form, 0, 0)

        return pcard



    def confirm_block(self):
        pcard = Famcy.FamcyPromptCard()
        pcard["pname"] = "confirm"

        input_form = Famcy.input_form()

        text_msg = Famcy.displayParagraph()
        text_msg.update({"title": "確認是否執行?", "content": ""})

        confirm_btn = Famcy.submitBtn()
        confirm_btn.update({"title":"確認"})
        pcard.preload = lambda: confirm_btn.connect(self.succeed_action, target=self.card_2)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"取消"})

        input_form.layout.addWidget(text_msg, 0, 0, 1, 2)
        input_form.layout.addWidget(confirm_btn, 1, 0)
        input_form.layout.addWidget(cancel_btn, 1, 1)

        pcard.layout.addWidget(input_form, 0, 0)

        return pcard
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def confirm_action(self, submission_obj, info_list):
        last_p_card = submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard")
        print("=========last_p_card: ", self, last_p_card, last_p_card.attributes, submission_obj.origin)
        submission_obj.target["ip"] = last_p_card["ip"]
        submission_obj.target["pname"] = last_p_card["pname"]
        submission_obj.target["btn_name"] = submission_obj.origin.value["confirm_id"]
        submission_obj.target["info_list"] = info_list
        submission_obj.target.last_card = last_p_card

        self.confirm_card.layout.content[0][0].layout.content[2][0].connect(self.return_action,target=submission_obj.target.last_card)

        if submission_obj.target["btn_name"] in self.prompt_info[submission_obj.target["pname"]].keys():
            self.confirm_card.layout.content[0][0].layout.content[0][0].update({"title": self.prompt_info[submission_obj.target["pname"]][submission_obj.target["btn_name"]]["confirm_msg"]})

        return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdatePrompt()]

    def succeed_action(self, submission_obj, info_list):
        last_p_card = submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard")
        if last_p_card["ip"]:
            msg = self.submit_device_action(last_p_card["pname"], last_p_card["btn_name"], last_p_card["ip"], last_p_card["info_list"])
        return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdateAlert(alert_message=msg)]

    def return_action(self, submission_obj, info_list):
        return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdatePrompt()]

    # open prompt
    def prompt_submit_input(self, submission_obj, info_list):
        if submission_obj.target == self.apm_card:
            _ = self.post_apm("get_message", submission_obj.origin.value["ip"], [])
        submission_obj.target["ip"] = submission_obj.origin.value["ip"] if "ip" in submission_obj.origin.value.keys() else None
        return Famcy.UpdatePrompt()

    # closed prompt
    def prompt_remove_input(self, submission_obj, info_list):
        return Famcy.UpdateRemoveElement(prompt_flag=True)

    # table submit function
    def submit_car_img(self, submission_obj, info_list):
        if len(info_list[0]) > 0:
            pass
        self.card_4.layout.content[0][0].update({
                "img_name": ["/asset/image/" + info_list[0][0]]
            })

        return Famcy.UpdateTabHtml()

    # def update_total_lot(self, submission_obj, info_list):
    #     if len(info_list[0]) > 0:
    #         total_lot = info_list[0][0]
    #         if len(total_lot) > 0 and self.post_edit_lot(totallot=str(total_lot)):
    #             self.total_lots = total_lot
    #             self.card_1.layout.content[0][0].layout.content[0][0].update({
    #                 "content":'總車格數: %s<br>總佔位數: %s<br>總空位數: %s'%(str(self.total_lots),str(self.total_occupied_lots),str(int(self.total_lots)-int(self.total_occupied_lots)))
    #             })
    #             return Famcy.UpdateAlert(alert_message="已成功修改總車格: "+str(total_lot))

    #     return Famcy.UpdateAlert(alert_message="資料修改失敗")

    def update_occupied_lot(self, submission_obj, info_list):
        if len(info_list[0]) > 0:
            occupied_lot = info_list[0][0]
            if len(occupied_lot) > 0 and self.post_edit_lot(occupiedlot=str(occupied_lot)):
                self.total_occupied_lots = occupied_lot
                self.card_1.layout.content[0][0].layout.content[0][0].update({
                    "content":'總車格數: %s<br>總佔位數: %s<br>總空位數: %s'%(str(self.total_lots),str(self.total_occupied_lots),str(int(self.total_lots)-int(self.total_occupied_lots)))
                })
                return [Famcy.UpdateAlert(alert_message="已成功修改佔用車格: "+str(occupied_lot)), Famcy.UpdateBlockHtml(target=self.card_1)]

        return Famcy.UpdateAlert(alert_message="資料修改失敗")

    def update_receipt(self, submission_obj, info_list):
        if self.post_receipt():
            self.printed_receipt = "1400"
            self.card_1.layout.content[0][0].layout.content[2][0].update({
                "content":"已列印: %s<br>剩餘發票數: %s<br>剩餘號碼: %s"%(str(1400-int(self.printed_receipt)),self.printed_receipt,'0')
            })
            return [Famcy.UpdateAlert(alert_message="已成功修改已列印發票數: "+str(self.printed_receipt)), Famcy.UpdateBlockHtml(target=self.card_1)]

        return Famcy.UpdateAlert(alert_message="資料修改失敗")

    def update_list(self, submission_obj, info_list):
        if len(info_list[1]) > 0 and len(info_list[2]) > 0:
            _coin = info_list[1][0]
            edit_coin = info_list[2][0]
            if _coin == "5":
                self.p_edit.layout.content[0][0].layout.content[3][0].update({"placeholder":self.h5})
            elif _coin == "10":
                self.p_edit.layout.content[0][0].layout.content[3][0].update({"placeholder":self.h10})
            elif _coin == "50":
                self.p_edit.layout.content[0][0].layout.content[3][0].update({"placeholder":self.h50})

            if len(edit_coin) > 0:
                return self.update_coin(submission_obj, info_list)

        return Famcy.UpdateBlockHtml()

    def update_coin(self, submission_obj, info_list):
        if len(info_list[1]) > 0 and len(info_list[2]) > 0:
            _coin = info_list[1][0]
            edit_coin = info_list[2][0]
            flag = False
            if _coin == "5":
                if len(edit_coin) > 0 and self.post_edit_coin(h5=edit_coin):
                    flag = True
                    self.h5 = edit_coin
            elif _coin == "10":
                if len(edit_coin) > 0 and self.post_edit_coin(h10=edit_coin):
                    flag = True
                    self.h10 = edit_coin
            elif _coin == "50":
                if len(edit_coin) > 0 and self.post_edit_coin(h50=edit_coin):
                    flag = True
                    self.h50 = edit_coin

            if flag:
                self.card_1.layout.content[0][0].layout.content[1][0].update({
                    "content":"50元: %s<br>10元: %s<br>5元: %s"%(str(self.h50),str(self.h10),str(self.h5))})
                return [Famcy.UpdateAlert(alert_message="已成功修改零錢("+str(_coin)+"元): "+str(edit_coin)), Famcy.UpdateBlockHtml(target=self.card_1)]

        return Famcy.UpdateAlert(alert_message="資料修改失敗")

    # def update_apm_refund(self, submission_obj, info_list):
    #     if len(info_list[0]) > 0:
    #         msg = self.submit_device_action(submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard")["pname"], submission_obj.origin.value["confirm_id"], submission_obj.origin["ip"], info_list)
    #     return Famcy.UpdateAlert(alert_message=msg)

    def update_apm_msg(self, submission_obj, info_list):
        if len(info_list[1]) > 0:
            msg = self.submit_device_action(submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard")["pname"], submission_obj.origin.value["confirm_id"], submission_obj.origin["ip"], info_list)
        return Famcy.UpdateAlert(alert_message=msg)

    def update_led_msg(self, submission_obj, info_list):
        if len(info_list[0]) > 0:
            msg = self.submit_device_action(submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard")["pname"], submission_obj.origin.value["confirm_id"], submission_obj.origin["ip"], info_list)
        return Famcy.UpdateAlert(alert_message=msg)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_hopper_available_lot(self):
        send_dict = {
            "service": "pms",
            "operation": "get_hopper"
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_msg = json.loads(res_msg)["message"]
        self.h50 = res_msg[0]['h50']
        self.h10 = res_msg[0]['h10']
        self.h5 = res_msg[0]['h5']
        self.printed_receipt = res_msg[0]['receipt']
        self.carpark_id_ = res_msg[0]["carpark_id"]

        self.card_1.layout.content[0][0].layout.content[1][0].update({
                "content":"50元: %s<br>10元: %s<br>5元: %s"%(self.h50,self.h10,self.h5)
            })

        self.card_1.layout.content[0][0].layout.content[2][0].update({
                "content":"已列印: %s<br>剩餘發票數: %s<br>剩餘號碼: %s"%(str(1400-int(self.printed_receipt)),self.printed_receipt,'0')
            })

        send_dict = {
            "service": "pms",
            "operation": "get_available_lot"
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_msg = json.loads(res_msg)["message"]
        self.total_lots = res_msg[0]['totallot']
        self.total_occupied_lots = res_msg[0]['total_occupied']
        self.carpark_id = res_msg[0]["carpark_id"]

        self.card_1.layout.content[0][0].layout.content[0][0].update({
                "content":'總車格數: %s<br>總佔位數: %s<br>總空位數: %s'%(str(self.total_lots),str(self.total_occupied_lots),str(int(self.total_lots)-int(self.total_occupied_lots)))
            })

        # update prompt placeholder
        self.p_edit.layout.content[0][0].layout.content[0][0].update({"placeholder":self.total_occupied_lots})
        self.p_edit.layout.content[0][0].layout.content[5][0].update({"placeholder":self.printed_receipt})

    def get_car_queue(self):
        send_dict = {
            "service": "pms",
            "operation": "get_car_queue"
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_msg = json.loads(res_msg)["message"]
        self.table_info = self.make_time_readable(res_msg,["modified_time"])

        self.card_3.layout.content[0][0].layout.content[0][0].update({
            "data": self.table_info
        })

    def get_device_configs(self):
        send_dict = {
            "service": "pms",
            "operation": "get_device_configs"
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_msg = json.loads(res_msg)["message"]
        return res_msg
        # return self.device_convertion(res_msg)

    def get_error_msg(self):
        send_dict = {
            "service": "pms",
            "operation": "get_operation_error_log"
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_msg = json.loads(res_msg)["message"]
        self.error_msg = str(res_msg)

        self.card_2.layout.content[1][0].update({
                "content": self.error_msg
            })

    def post_edit_lot(self, totallot=None, occupiedlot=None):
        send_dict = {
            "service": "pms",
            "carpark_id": self.carpark_id,
            "operation": "update_lot"
        }
        if totallot:
            send_dict["totallot"] = totallot
        if occupiedlot:
            send_dict["total_occupied"] = occupiedlot
        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)

        return json.loads(res_msg)["indicator"]

    def post_edit_coin(self, h50=None, h10=None, h5=None):
        send_dict = {
            "service": "pms",
            "carpark_id": self.carpark_id_,
            "operation": "update_hopper"
        }
        if h50:
            send_dict["h50"] = str(h50)
        if h10:
            send_dict["h10"] = str(h10)
        if h5:
            send_dict["h5"] = str(h5)
        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)

        return json.loads(res_msg)["indicator"]

    def post_receipt(self):
        send_dict = {
            "service": "pms",
            "carpark_id": self.carpark_id_,
            "operation": "update_receipt"
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)

        return json.loads(res_msg)["indicator"]

    def post_apm(self, btn_name, ip_info, list_info):
        send_dict = {
            "service": "pms",
            "operation": "device_management_APM",
            "button": btn_name,
            "ip": ip_info
        }
        if btn_name == "display_message":
            if len(list_info[1]) > 0 and list_info[1][0] != "":
                send_dict["message"] = list_info[1][0]
            else:
                return False
        elif btn_name == "refund":
            if len(list_info[0]) > 0 and list_info[0][0] != "":
                send_dict["amount"] = list_info[0][0]
            else:
                return False

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        if json.loads(res_msg)["indicator"] and btn_name == "get_message":
            self.apm_card.layout.content[0][0].layout.content[1][0].value["defaultValue"] = json.loads(res_msg)["message"][0]
        return json.loads(res_msg)["indicator"]

    def post_station(self, btn_name, ip_info):
        send_dict = {
            "service": "pms",
            "operation": "device_management_STATION",
            "button": btn_name,
            "ip": ip_info
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]

    def post_ipcam(self, btn_name, ip_info):
        send_dict = {
            "service": "pms",
            "operation": "device_management_IPCAM",
            "button": btn_name,
            "ip": ip_info
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]

    def post_led(self, btn_name, ip_info, list_info):
        send_dict = {
            "service": "pms",
            "operation": "device_management_LED",
            "button": btn_name,
            "ip": ip_info
        }
        if btn_name == "display_message" and list_info[0][0] != "":
            if len(list_info[0]) > 0:
                send_dict["message"] = list_info[0][0]
            else:
                return False
        # POST
        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]
        
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # def device_convertion(self, data):
    #     pre_deal_dict = {}
    #     return_list = []
    #     for item in data.keys():
    #         if '.' in data[item]:
    #             pre_deal_dict[item] = data[item]

    #     for deal_item in pre_deal_dict.keys():
    #         if 'apm' in deal_item:
    #             return_list.append({"type":"APM","ip":pre_deal_dict[deal_item],"name":deal_item})
    #         elif 'ipcam' in deal_item and '_mon' not in deal_item:
    #             return_list.append({"type":"IPCAM","ip":pre_deal_dict[deal_item],"name":deal_item})
    #         elif 'e1' == deal_item:
    #             return_list.append({"type":"STATION","ip":pre_deal_dict[deal_item],"name":deal_item})
    #         elif 'x1' == deal_item:
    #             return_list.append({"type":"STATION","ip":pre_deal_dict[deal_item],"name":deal_item})

    #     return return_list
    def make_time_readable(self,data,columns_name):
        """
        Use to make time friendly to read
        """
        for row in data:
            for column in columns_name:
                if len(row[column]) == 15:
                    row[column] = str(row[column][:2]+"年 "+row[column][2:4]+"月"+row[column][4:6]+"日 "+row[column][6:8]+":"+row[column][8:10]+":"+row[column][10:12])
                if len(row[column]) == 12:
                    row[column] = str(row[column][:2]+"年 "+row[column][2:4]+"月"+row[column][4:6]+"日 "+row[column][6:8]+":"+row[column][8:10]+":"+row[column][10:12])
        return data

    def submit_device_action(self, pname, btn_name, ip_info, list_info):
        if pname == "apm":
            if self.post_apm(btn_name, ip_info, list_info):
                return "執行成功"
        elif pname == "ipcam":
            if self.post_ipcam(btn_name, ip_info):
                return "執行成功"
        elif pname == "station":
            if self.post_station(btn_name, ip_info):
                return "執行成功"
        elif pname == "led":
            if self.post_led(btn_name, ip_info, list_info):
                return "執行成功"

        return "執行失敗，請重新再試"

    # def refund_money(self, money):
    #     h50 = int(money) // 50
    #     h10 = (int(money) % 50) // 10
    #     h5 = (int(money) % 10) // 5

    #     return h50, h10, h5
    # ====================================================
    # ====================================================

   

page = OverviewPage()
page.register()