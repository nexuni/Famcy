import Famcy
import json
import requests
import copy
import itertools
import datetime
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import read_config_yaml
from os.path import expanduser
import datetime
from _static_.store_btn_utils import *


G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
HOST_ADDRESS = "http://127.0.0.1:5088" # "https://store.nexuni-api.com/doday/v1"

class storePage(Famcy.FamcyPage):
    def __init__(self):
        super(storePage, self).__init__()

        self.store_id = self.get_cookie('store_id')

        # preload function
        self.menu_data = self.get_return_menu()

        # for declaration
        # ===============
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()
        # ===============

        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 1, 0)
        self.layout.addWidget(self.card_3, 2, 0)

        # postload function
        self.load_item()

        set_store_btn(self, '/store')

        
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

    def card2(self):
        _card2 = Famcy.FamcyCard()
        _card2.title = '管理優惠券'

        _input_form = Famcy.input_form()

        coupon_name = Famcy.pureInput()
        coupon_name.set_submit_value_name('name')
        coupon_name.update({'title':'優惠券名稱*', 'content':'', "action_after_post": "save"})
        
        coupon_key = Famcy.pureInput()
        coupon_key.set_submit_value_name('key')
        coupon_key.update({'title':'優惠券代碼*', 'content':'', "action_after_post": "save"})
        
        coupon_amount = Famcy.pureInput()
        coupon_amount.set_submit_value_name('amount')
        coupon_amount.update({
            'title':'優惠券數量*',
            'content':'',
            'input_type':'number',
            "action_after_post": "save"
        })

        coupon_start_time = Famcy.pureInput()
        coupon_start_time.set_submit_value_name('start_time')
        coupon_start_time.update({'title':'優惠券開始時間*', 'content':'', "input_type": "date", "action_after_post": "save"})

        coupon_end_time = Famcy.pureInput()
        coupon_end_time.set_submit_value_name('end_time')
        coupon_end_time.update({'title':'優惠券結束時間*', 'content':'', "input_type": "date", "action_after_post": "save"})

        default_store = Famcy.multipleChoicesRadioInput()
        default_store.set_submit_value_name('default_for_store')
        default_store.update({'title':'預設優惠', 'value':['設定優惠券為預設優惠'], "action_after_post": "save"})

        _card2.current_coupon_cat = ""
        _card2.coupon_cat = Famcy.multipleChoicesRadioInput()
        _card2.coupon_cat.set_submit_value_name('item_cat')
        _card2.coupon_cat.update({
            'title':'優惠類別*',
            'value':['全品項', '絕配系列', '豆漿系列']
        })
        _card2.coupon_cat.connect(self.update_coupon_item_list)

        _card2.current_coupon_item = ""
        _card2.coupon_item = Famcy.multipleChoicesRadioInput()
        _card2.coupon_item.set_submit_value_name('item')
        _card2.coupon_item.update({
            'title':'優惠品項*',
            'value':['全品項', '絕配系列', '豆漿系列']
        })
        _card2.coupon_item.connect(self.update_coupon_item_list)

        _card2.current_coupon_addon = ""
        _card2.coupon_addon = Famcy.multipleChoicesRadioInput()
        _card2.coupon_addon.set_submit_value_name('item_addon')
        _card2.coupon_addon.update({
            'title':'優惠選配*',
            'value':['全品項', '絕配系列', '豆漿系列']
        })
        _card2.coupon_addon.connect(self.update_coupon_item_list)

        coupon_plan = Famcy.singleChoiceRadioInput()
        coupon_plan.set_submit_value_name('plan')
        coupon_plan.update({
            'title':'優惠券方案*',
            'value':['買一送一', '買二送一', '買三送一', '95折', '8折', '7折', '5折'],
            "action_after_post": "save"
        })

        sb_btn = Famcy.submitBtn()
        sb_btn.update({'title': '新增'})
        sb_btn.connect(self.add_new_coupon)

        _input_form.layout.addWidget(coupon_name, 0, 0)
        _input_form.layout.addWidget(coupon_key, 0, 1)
        _input_form.layout.addWidget(coupon_amount, 0, 2)
        _input_form.layout.addWidget(coupon_start_time, 1, 0)
        _input_form.layout.addWidget(coupon_end_time, 1, 1)
        _input_form.layout.addWidget(default_store, 1, 2)
        _input_form.layout.addWidget(_card2.coupon_cat, 2, 0)
        _input_form.layout.addWidget(_card2.coupon_item, 2, 1, 2, 1)
        _input_form.layout.addWidget(_card2.coupon_addon, 2, 2, 2, 1)
        _input_form.layout.addWidget(coupon_plan, 3, 0)
        _input_form.layout.addWidget(sb_btn, 4, 0)
        
        _card2.layout.addWidget(_input_form, 0, 0)
        
        return _card2

    def card3(self):
        _card3 = Famcy.FamcyCard()
        _card3.title = '顯示店面優惠券'

        _input_form = Famcy.input_form()

        self.coupon_table = Famcy.table_block()
        self.coupon_table.set_submit_value_name("coupon")
        self.coupon_table.update({
            "input_button": "none",
            "input_value_col_field": "promotion_key",
            "toolbar": False,
            "page_footer": False,

            "table_height": "auto",

            "column": [[
                {
                    "title": '店面代碼',
                    "field": 'store_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '優惠券名稱',
                    "field": 'title',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '優惠券代碼',
                    "field": 'promotion_key',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '優惠券數量',
                    "field": 'usage_amount',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '需要點數',
                    "field": 'required_points',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '開始時間',
                    "field": 'start_time',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '結束時間',
                    "field": 'end_time',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '預設優惠',
                    "field": 'default_for_store',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '優惠內容',
                    "field": 'effector',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
            ]],
            "data": []
        })
        self.update_coupon_table()

        # sb_btn = Famcy.submitBtn()
        # sb_btn.update({'title': '更新'})

        _input_form.layout.addWidget(self.coupon_table, 0, 0)
        # _input_form.layout.addWidget(sb_btn, 1, 0)
        
        _card3.layout.addWidget(_input_form, 0, 0)
        
        return _card3

    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def update_coupon_item_list(self, sb, info):
        if self.card_2.current_coupon_cat != info["item_cat"] or self.card_2.current_coupon_item != info["item"] or self.card_2.current_coupon_addon != info["item_addon"]:
            self.load_item(info)
            return Famcy.UpdateBlockHtml(target=self.card_2)

    def add_new_coupon(self, sb, info):
        if info['name'] and info['key'] and info['amount'] and info["item_cat"] and info['item'] and info["item_addon"] and info['plan']:
            res_ind, res_msg = self.post_add_new_promotion(info)
            update_response = []
            if res_ind:
                self.update_coupon_table()
                update_response = [Famcy.UpdateBlockHtml(target=self.card_3)]
            return update_response+[Famcy.UpdateAlert(target=self.card_2, alert_message=res_msg)]
        return Famcy.UpdateAlert(target=self.card_2, alert_message='資料錯誤，請刷新再試')

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
    def get_return_menu(self):
        query = HOST_ADDRESS + '?service=menu&operation=return_menu&device=doday_console&store_id=' + str(self.store_id) # + '&menu_name=' + self.current_main_menu
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        print("get_return_menu res_dict: ", res_dict)
        return res_dict

    def post_add_new_promotion(self, info):
        send_dict = {
            'service':'promotion',
            'operation':'add_new_promotion',
            'brand_id':'Doday',
            'store_id':self.store_id,
            'exclusive_member':'',
            'description':'',
            'title':info['name'],
            'effector':json.dumps(self.set_effector_list(info)),
            'promotion_key':info['key'],
            'usage_amount':int(info['amount']),
            'default_for_store': self.store_id if info["default_for_store"] else "",
            "start_time": self.convert_to_epoch_time(info["start_time"]),
            "end_time": self.convert_to_epoch_time(info["end_time"]),
        }
        print("post_add_new_promotion: ", send_dict)
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        print('res_dict: ', res_dict['message'])
        return res_dict['indicator'], res_dict['message']

    def post_update_store_information(self, edit_day_type, start_time, end_time, d, action="add"):
        send_dict = {
            "service": "order",
            "operation": "update_store_information",
            "edit_day_type": edit_day_type,                     # by-dates/by-days/all
            "store_id": self.store_id,
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
        query = HOST_ADDRESS+"?service=order&operation=get_store_information&store_id="+self.store_id
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", json.loads(res_dict["message"]))
        return res_dict["indicator"], json.loads(res_dict["message"])

    def get_get_promotion_info(self):
        query = HOST_ADDRESS+"?service=promotion&operation=get_promotion_info&promotion_key=ALL_PROMOTION_KEY&store_id="+self.store_id
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", res_dict["message"])
        return res_dict["indicator"], res_dict["message"]
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def load_item(self, info={"item_cat": None, "item": None, "item_addon": None}):
        item_list = []
        addon_list = []
        if info["item_cat"] and info["item_cat"] in self.menu_data["titles"]:
            i = self.menu_data["titles"].index(info["item_cat"])
            item_list = [item["name"] for item in self.menu_data["items"][i]]

            if info["item"] and info["item"] in item_list:
                j = item_list.index(info["item"])
                addon_list = self.menu_data["items"][i][j]["addon_title"]
        
        self.card_2.coupon_cat.update({"value": ["全品項"]+self.menu_data["titles"], "defaultValue": info["item_cat"] if isinstance(info["item_cat"], list) else [info["item_cat"]]})
        self.card_2.coupon_item.update({"value": ["全品項"]+item_list, "defaultValue": info["item"] if isinstance(info["item"], list) else [info["item"]]})
        self.card_2.coupon_addon.update({"value": ["全品項"]+addon_list, "defaultValue": info["item_addon"] if isinstance(info["item_addon"], list) else [info["item_addon"]]})


    def update_coupon_table(self):
        res_ind, res_msg = self.get_get_promotion_info()
        if res_ind:
            self.coupon_table.update({ "data": res_msg if isinstance(res_msg, list) else [res_msg] })

    def set_table_data(self):
        res_ind, res_msg = self.get_get_store_information()
        if res_ind:
            self.put_data_in_table(json.loads(res_msg["special_hours"]))

    def set_effector_list(self, info):
        target_list = []
        item_cat = info["item_cat"] if isinstance(info["item_cat"], list) else [info["item_cat"]]
        item = info["item"] if isinstance(info["item"], list) else [info["item"]]
        item_addon = info["item_addon"] if isinstance(info["item_addon"], list) else [info["item_addon"]]

        for i_cat, i_item, i_addon in itertools.zip_longest(item_cat, item, item_addon):
            print("i_cat, i_item, i_addon: ", i_cat, i_item, i_addon)
            i_cat = "*" if i_cat == "全品項" or not i_cat else i_cat
            i_item = "*" if i_item == "全品項" or not i_item else i_item
            i_addon = "*" if i_addon == "全品項" or not i_addon else i_addon
            target_list.append(i_cat+"/"+i_item+"/"+i_addon)

        if info["plan"] == "買一送一":
            return [{"promotype": "buyget", "promostrategy": [], "promopricing": "1/1",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        elif info["plan"] == "買二送一":
            return [{"promotype": "buyget", "promostrategy": [], "promopricing": "2/1",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        elif info["plan"] == "買三送一":
            return [{"promotype": "buyget", "promostrategy": [], "promopricing": "3/1",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        elif info["plan"] == "95折":
            return [{"promotype": "discount", "promostrategy": [], "promopricing": "95",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        elif info["plan"] == "8折":
            return [{"promotype": "discount", "promostrategy": [], "promopricing": "80",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        elif info["plan"] == "7折":
            return [{"promotype": "discount", "promostrategy": [], "promopricing": "70",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        elif info["plan"] == "5折":
            return [{"promotype": "discount", "promostrategy": [], "promopricing": "50",\
             "max_save_price": 10000, "max_apply_items": 1000,\
             "target": target_list}]

        # elif info["plan"] == "固定扣金額":
        #     return [{"promotype": "offset", "promostrategy": [], "promopricing": "5",\
        #      "target": target_list,\
        #      "max_save_price": 10000, "max_apply_items": 1000}]

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

    def convert_to_epoch_time(self, date=None):
        if date:
            date_list = date.split("-")
            y = int(date_list[0])
            m = int(date_list[1])
            d = int(date_list[2])

        return int(datetime.datetime(y,m,d,0,0).timestamp())
    # ====================================================
    # ====================================================

   
storePage.register("/store", Famcy.NexuniStyle(), permission_level=0, background_thread=False)