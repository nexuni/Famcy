import Famcy
import json
import requests
import datetime
from gadgethiServerUtils.authentication import *

G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
STORE_ID = "DDA"
HOST_ADDRESS = "http://127.0.0.1:5088/" # "https://store.nexuni-api.com/doday/v1"

class machinePage(Famcy.FamcyPage):
    def __init__(self):
        super(machinePage, self).__init__()

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
        # this card shows daily revenue of the store
        _card1 = Famcy.FamcyCard()
        _card1.title = "點餐機零錢增減管理"

        _input_form = Famcy.input_form()

        edit_action = Famcy.inputList()
        edit_action.set_submit_value_name("edit_action")
        edit_action.update({
                "title": "操作性質",
                "value": ["放入錢幣", "拿出錢幣"]
            })
        coin_type = Famcy.inputList()
        coin_type.set_submit_value_name("coin_type")
        coin_type.update({
                "title": "硬幣種類",
                "value": ["1", "5", "10", "50"]
            })
        amount = Famcy.pureInput()
        amount.set_submit_value_name("amount")
        amount.update({
                "title": "數量",
                "input_type": "number"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "更改"
            })
        sb_btn.connect(self.update_coin_status)

        _input_form.layout.addWidget(edit_action, 0, 0)
        _input_form.layout.addWidget(coin_type, 0, 1)
        _input_form.layout.addWidget(amount, 0, 2)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 3)

        self.machine_table = Famcy.table_block()
        self.machine_table.update({
            "input_button": "none",

            "page_detail": False,                            # (true / false)
            "page_detail_content": "key_value",             # if page_detail == true: (key_value / HTML_STR => ["<p>line1</p>", "<p>line2</p>"])

            "toolbar": False,                                # (true / false)
            "page_footer": True,                            # (true / false)
            "page_footer_detail": {                         # if page_footer == true
                "page_size": 100,
                "page_list": [1, 2, "all"]
            },

            "table_height": "200px",

            "column": [[{
                    "title": '點餐機編號',
                    "field": 'machine_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '零錢數量(1元)',
                    "field": 'one',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '零錢數量(5元)',
                    "field": 'five',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '零錢數量(10元)',
                    "field": 'ten',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '零錢數量(50元)',
                    "field": 'fifty',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '信用卡收入',
                    "field": 'creditcard',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '優游卡收入',
                    "field": 'yoyocard',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": 'LINEPAY收入',
                    "field": 'linepay',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '狀態',
                    "field": 'status',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": [
                {
                    "machine_id": "DDA01",
                    "one": "10",
                    "five": "1",
                    "ten": "10",
                    "fifty": "20",
                    "creditcard": "100",
                    "yoyocard": "50",
                    "linepay": "200",
                    "status": ""
                }
            ]
        })

        _card1.layout.addWidget(_input_form, 0, 0)
        _card1.layout.addWidget(self.machine_table, 1, 0)

        return _card1
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def update_coin_status(self, sb, info):
        # TODO: server don't have "cash_config_path" and this file, 
        # don't know how to update table
        edit_action = "add" if info["edit_action"] == "放入錢幣" else "deduct"
        amount = str(info["amount"]) if info["amount"] else "0"
        res_ind, res_msg = self.post_add_or_return_coin(edit_action, amount, str(info["coin_type"]))

        return Famcy.UpdateAlert(target=self.card_1, alert_message=res_msg)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def post_add_or_return_coin(self, process, amount, coin):
        send_dict = {
            "service": "cash_management",
            "operation": "add_or_return_coin",
            "process": process,
            "amount": str(amount),
            "coin_type": coin
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", res_dict)
        return res_dict["indicator"], res_dict["message"]
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
machinePage.register("/machine", Famcy.NexuniStyle(), permission_level=0, background_thread=False)