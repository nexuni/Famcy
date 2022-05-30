import Famcy
import json
import requests

class storePage(Famcy.FamcyPage):
    def __init__(self):
        super(storePage, self).__init__()

        # for declaration
        # ===============
        self.card_1 = self.card1()
        # ===============

        self.layout.addWidget(self.card_1, 0, 0)

        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card1(self):
        # this card provides manager to edit opening time of the store
        _card1 = Famcy.FamcyCard()
        _card1.title = "編輯員工打卡紀錄"

        _input_form = Famcy.input_form()

        edit_day = Famcy.pureInput()
        edit_day.set_submit_value_name("date")
        edit_day.update({
                "title": "輸入日期/星期",
                "desc": "日期格式: YYYYMMDD, 星期格式: (星期一/monday)"
            })
        start_time = Famcy.pureInput()
        start_time.set_submit_value_name("start_time")
        start_time.update({
                "title": "輸入開始營業時間",
                "desc": ".",
                "input_type": "time"
            })
        end_time = Famcy.pureInput()
        end_time.set_submit_value_name("end_time")
        end_time.update({
                "title": "輸入結束營業時間",
                "desc": ".",
                "input_type": "time"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "更改"
            })
        sb_btn.connect(self.edit_opening_hour)

        _input_form.layout.addWidget(edit_day, 0, 0)
        _input_form.layout.addWidget(start_time, 0, 1)
        _input_form.layout.addWidget(end_time, 0, 2)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 3)

        _card1.layout.addWidget(_input_form, 0, 0)

        return _card1

    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def edit_opening_hour(self, sb, info):
        res_ind, res_msg = self.post_opening_hour(info)
        return Famcy.UpdateAlert(target=self.card_1, alert_message=res_msg)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def post_opening_hour(self, info):
        send_dict = {
            "store_name": "DDA",
            "edit_day": info["date"], # "monday"
            "start_time": info["start_time"].replace(":", ""),
            "end_time": info["end_time"].replace(":", ""),
        }

        # res_str = Famcy.FManager.http_client.client_get("doday_http_url", send_dict, gauth=False)
        res_str = requests.get("http://127.0.0.1:5000/store_open", params=send_dict).text
        res_ind = json.loads(res_str)["indicator"]
        res_msg = json.loads(res_str)["message"]

        return res_ind, res_msg
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
storePage.register("/store", Famcy.ClassicStyle(), permission_level=0, background_thread=False)