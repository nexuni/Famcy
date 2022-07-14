import Famcy
import json
import requests
import copy
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import read_config_yaml
from os.path import expanduser
import datetime


G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
STORE_ID = "DDC"
HOST_ADDRESS = "http://127.0.0.1:5088" # "https://store.nexuni-api.com/doday/v1"

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
        _card1.title = "編輯店面營業時間"

        # ====================================================
        # ====================================================
        # This section finds out how manager want to edit 
        # opening hour
        # ====================================================
        _input_form1 = Famcy.input_form()

        title1 = Famcy.displayParagraph()
        title1.update({
                "title": "選擇修改方式*",
                "content": ""
            })

        edit_date_sb_btn = Famcy.submitBtn()
        edit_date_sb_btn["edit_type"] = "by-dates"
        edit_date_sb_btn.update({
                "title": "選擇日期修改營業時間"
            })
        edit_date_sb_btn.connect(self.show_date_input_block)

        edit_day_sb_btn = Famcy.submitBtn()
        edit_day_sb_btn["edit_type"] = "by-days"
        edit_day_sb_btn.update({
                "title": "選擇星期修改營業時間"
            })
        edit_day_sb_btn.connect(self.show_date_input_block)

        edit_store_sb_btn = Famcy.submitBtn()
        edit_store_sb_btn["edit_type"] = "all"
        edit_store_sb_btn.update({
                "title": "修改店面營業時間"
            })
        edit_store_sb_btn.connect(self.show_date_input_block)

        _input_form1.layout.addWidget(title1, 0, 0)
        _input_form1.layout.addWidget(edit_date_sb_btn, 1, 0)
        _input_form1.layout.addWidget(edit_day_sb_btn, 1, 1)
        _input_form1.layout.addWidget(edit_store_sb_btn, 1, 2)
        # ====================================================

        # ====================================================
        # ====================================================
        # This section decides that manager is going to close
        # the store on the selected date or weekdays, or just
        # edit opening time
        # ====================================================
        _input_form2 = Famcy.input_form()

        title2 = Famcy.displayParagraph()
        title2.update({
                "title": "選擇修改營業時間或設定店休*",
                "content": ""
            })

        edit_closed_sb_btn = Famcy.submitBtn()
        edit_closed_sb_btn["edit_status"] = "closed"
        edit_closed_sb_btn.update({
                "title": "設定店休"
            })
        edit_closed_sb_btn.connect(self.show_time_input_block)

        edit_time_sb_btn = Famcy.submitBtn()
        edit_time_sb_btn["edit_status"] = "edit_time"
        edit_time_sb_btn.update({
                "title": "修改營業時間"
            })
        edit_time_sb_btn.connect(self.show_time_input_block)

        _input_form2.layout.addWidget(title2, 0, 0)
        _input_form2.layout.addWidget(edit_closed_sb_btn, 1, 0)
        _input_form2.layout.addWidget(edit_time_sb_btn, 1, 1)
        # ====================================================

        # ====================================================
        # ====================================================
        # Input form that will be showed after the form above
        # are selected
        # ====================================================
        self.edit_time_input_form = Famcy.input_form()

        self.edit_day = Famcy.inputList()
        self.edit_day.set_submit_value_name("day")
        self.edit_day.update({
                "title": "選擇星期修改營業時間",
                "desc": ".",
                "value": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
                "returnValue": [1, 2, 3, 4, 5, 6, 7]
            })
        self.edit_day.body.style["display"] = "none"

        self.edit_date = Famcy.pureInput()
        self.edit_date.set_submit_value_name("date")
        self.edit_date.update({
                "input_type": "date",
                "title": "選擇日期修改營業時間",
                "desc": "."
            })
        self.edit_date.body.style["display"] = "none"

        self.start_time = Famcy.pureInput()
        self.start_time.set_submit_value_name("start_time")
        self.start_time.update({
                "title": "輸入開始營業時間*",
                "desc": ".",
                "input_type": "time"
            })
        self.start_time.body.style["display"] = "none"

        self.end_time = Famcy.pureInput()
        self.end_time.set_submit_value_name("end_time")
        self.end_time.update({
                "title": "輸入結束營業時間*",
                "desc": ".",
                "input_type": "time"
            })
        self.end_time.body.style["display"] = "none"

        self.card1_sb_btn = Famcy.submitBtn()
        self.card1_sb_btn.update({
                "title": "修改營業時間"
            })
        self.card1_sb_btn.body.style["display"] = "none"
        self.card1_sb_btn["edit_type"] = None
        self.card1_sb_btn["edit_status"] = None
        self.card1_sb_btn.connect(self.edit_opening_hour)

        self.edit_time_input_form.layout.addWidget(self.edit_day, 0, 0)
        self.edit_time_input_form.layout.addWidget(self.edit_date, 0, 1)
        self.edit_time_input_form.layout.addWidget(self.start_time, 0, 2)
        self.edit_time_input_form.layout.addWidget(self.end_time, 0, 3)
        self.edit_time_input_form.layout.addWidget(self.card1_sb_btn, 1, 0)
        # ====================================================

        # ====================================================
        # ====================================================
        # This section shows edit history of the store opening
        # time
        # ====================================================
        self.table_input_form = Famcy.input_form()

        self.opening_hour_table = Famcy.table_block()
        self.opening_hour_table.set_submit_value_name("edit_id")
        self.opening_hour_table.update({
            "input_button": "radio",
            "input_value_col_field": "edit_id",
            "toolbar": False,
            "page_footer": False,

            "table_height": "auto",

            "column": [[{
                    "title": '序號',
                    "field": 'edit_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '修改方式',
                    "field": 'edit_type',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '修改日期/星期',
                    "field": 'edit_date',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '店面開始營業時間',
                    "field": 'start_time',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '店面結束營業時間',
                    "field": 'end_time',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": []
        })
        self.set_table_data()

        delete_sb_btn = Famcy.submitBtn()
        delete_sb_btn.update({
                "title": "刪除紀錄"
            })
        delete_sb_btn.connect(self.delete_edit_history)

        self.table_input_form.layout.addWidget(self.opening_hour_table, 0, 0)
        self.table_input_form.layout.addWidget(delete_sb_btn, 1, 0)
        # ====================================================

        _card1.layout.addWidget(_input_form1, 0, 0)
        _card1.layout.addWidget(_input_form2, 0, 1)
        _card1.layout.addWidget(self.edit_time_input_form, 1, 0, 1, 2)
        _card1.layout.addWidget(self.table_input_form, 2, 0, 1, 2)

        return _card1

    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def show_date_input_block(self, sb, info):
        if sb.origin["edit_type"] == "by-dates":
            self.card1_sb_btn["edit_type"] = "by-dates"
            self.edit_day.body.style["display"] = "none"
            self.edit_date.body.style["display"] = "block"

        elif sb.origin["edit_type"] == "by-days":
            self.card1_sb_btn["edit_type"] = "by-days"
            self.edit_day.body.style["display"] = "block"
            self.edit_date.body.style["display"] = "none"

        elif sb.origin["edit_type"] == "all":
            self.card1_sb_btn["edit_type"] = "all"
            self.edit_day.body.style["display"] = "none"
            self.edit_date.body.style["display"] = "none"

        else:
            self.edit_day.body.style["display"] = "none"
            self.edit_date.body.style["display"] = "none"
            return Famcy.UpdateAlert(target=self.card_1, alert_message="資料錯誤，請刷新再試")

        self.card1_sb_btn.body.style["display"] = "block" if self.card1_sb_btn["edit_type"] and self.card1_sb_btn["edit_status"] else "none"

        return Famcy.UpdateBlockHtml(target=self.edit_time_input_form)

    def show_time_input_block(self, sb, info):
        if sb.origin["edit_status"] == "edit_time":
            self.card1_sb_btn["edit_status"] = "edit_time"
            self.start_time.body.style["display"] = "block"
            self.end_time.body.style["display"] = "block"

        elif sb.origin["edit_status"] == "closed":
            self.card1_sb_btn["edit_status"] = "closed"
            self.start_time.body.style["display"] = "none"
            self.end_time.body.style["display"] = "none"

        else:
            self.start_time.body.style["display"] = "none"
            self.end_time.body.style["display"] = "none"
            return Famcy.UpdateAlert(target=self.card_1, alert_message="資料錯誤，請刷新再試")

        self.card1_sb_btn.body.style["display"] = "block" if self.card1_sb_btn["edit_type"] and self.card1_sb_btn["edit_status"] else "none"

        return Famcy.UpdateBlockHtml(target=self.edit_time_input_form)

    def edit_opening_hour(self, sb, info):
        if sb.origin["edit_status"] == "edit_time":
            start_time = info["start_time"]
            end_time = info["end_time"]
        else:
            start_time = "XX"
            end_time = "XX"

        if sb.origin["edit_type"] == "by-dates":
            d = int(info["date"][-2:])
        elif sb.origin["edit_type"] == "by-days":
            d = int(info["day"])
        else:
            d = None

        res_ind, res_msg = self.post_update_store_information(self.card1_sb_btn["edit_type"], start_time, end_time, [d])
        if res_ind:
            self.put_data_in_table(json.loads(res_msg["special_hours"]))
        return [Famcy.UpdateBlockHtml(target=self.table_input_form), Famcy.UpdateAlert(target=self.card_1, alert_message="成功更新店面資訊")]

    def delete_edit_history(self, sb, info):
        table_data = copy.deepcopy(self.opening_hour_table.value["data"])[int(info["edit_id"]) - 1]
        edit_day_type = "by-dates" if table_data["edit_type"] == "日期" else "by-days"
        start_time = table_data["start_time"]
        end_time = table_data["end_time"]
        d = [int(i) for i in table_data["edit_date"].replace("號", "").replace("星期", "").split(" | ")]
        res_ind, res_msg = self.post_update_store_information(edit_day_type, start_time, end_time, d, "del")
        if res_ind:
            self.put_data_in_table(json.loads(res_msg["special_hours"]))
        return [Famcy.UpdateBlockHtml(target=self.table_input_form), Famcy.UpdateAlert(target=self.card_1, alert_message="成功更新店面資訊")]

    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def post_update_store_information(self, edit_day_type, start_time, end_time, d, action="add"):
        send_dict = {
            "service": "order",
            "operation": "update_store_information",
            "edit_day_type": edit_day_type,                     # by-dates/by-days/all
            "store_id": STORE_ID,
            "start_time": start_time,
            "end_time": end_time,
            "edit_day_list": json.dumps(d),
            "action": action
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", json.loads(res_dict["message"]))
        return res_dict["indicator"], json.loads(res_dict["message"])

    def get_get_store_information(self):
        query = HOST_ADDRESS+"?service=order&operation=get_store_information&store_id="+STORE_ID
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", json.loads(res_dict["message"]))
        return res_dict["indicator"], json.loads(res_dict["message"])
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def set_table_data(self):
        res_ind, res_msg = self.get_get_store_information()
        if res_ind:
            self.put_data_in_table(json.loads(res_msg["special_hours"]))

    def put_data_in_table(self, time_data):
        i = 1
        _data = []

        for temp in time_data:
            _temp_dict = {}
            _temp_dict["edit_id"] = str(i)
            _temp_dict["start_time"] = temp["hours"]["opening_time"]
            _temp_dict["end_time"] = temp["hours"]["closing_time"]
            _temp_dict["edit_date"] = ""

            if temp["type"] == "by-dates":
                _temp_dict["edit_type"] = "日期"
                if len(temp["arg"]) > 0:
                    for d in temp["arg"]: _temp_dict["edit_date"] += str(d) + "號 | "
                    _temp_dict["edit_date"] = _temp_dict["edit_date"][:-3]
            elif temp["type"] == "by-days":
                _temp_dict["edit_type"] = "星期"
                if len(temp["arg"]) > 0:
                    for d in temp["arg"]: _temp_dict["edit_date"] += "星期" + str(d) + " | "
                    _temp_dict["edit_date"] = _temp_dict["edit_date"][:-3]
            else:
                _temp_dict["edit_type"] = "店面"
            _data.append(_temp_dict)
            i += 1

        self.opening_hour_table.update({
                "data": _data
            })
    # ====================================================
    # ====================================================

   
storePage.register("/store", Famcy.NexuniStyle(), permission_level=0, background_thread=False)