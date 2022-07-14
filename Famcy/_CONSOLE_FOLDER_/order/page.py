import Famcy
import json
import requests
import datetime
from gadgethiServerUtils.authentication import *

G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
STORE_ID = "DDA"
HOST_ADDRESS = "http://127.0.0.1:5088/" # "https://store.nexuni-api.com/doday/v1"


class orderPage(Famcy.FamcyPage):
    def __init__(self):
        super(orderPage, self).__init__()

        # for declaration
        # ===============
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        # ===============

        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 1, 0)
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card1(self):
        # this card shows daily revenue of the store
        _card1 = Famcy.FamcyCard()
        _card1.title = "訂單管理"

        _input_form = Famcy.input_form()

        order_num = Famcy.pureInput()
        order_num.set_submit_value_name("order_num")
        order_num.update({
                "title": "輸入單號",
                "desc": "ex. DDA-20210901-5003"
            })

        selected_date = Famcy.pureInput()
        selected_date.set_submit_value_name("selected_date")
        selected_date.update({
                "title": "選擇日期",
                "desc": ".",
                "input_type": "date"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "查詢"
            })
        sb_btn.connect(self.show_order_detail)

        _input_form.layout.addWidget(order_num, 0, 0)
        _input_form.layout.addWidget(selected_date, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        self.order_table = Famcy.table_block()
        self.order_table.update({
            "input_button": "none",

            "page_detail": False,                            # (true / false)
            "page_detail_content": "key_value",             # if page_detail == true: (key_value / HTML_STR => ["<p>line1</p>", "<p>line2</p>"])

            "toolbar": False,                                # (true / false)
            "page_footer": False,

            "table_height": "200px",

            "column": [[{
                    "title": '點餐編號',
                    "field": 'order_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '序號',
                    "field": 'order_no',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '店',
                    "field": 'store_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '系列',
                    "field": 'name1',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '品名',
                    "field": 'name2',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '配料',
                    "field": 'name3with4',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '用餐方式',
                    "field": 'stayortogo',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '數量',
                    "field": 'amount',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '總金額',
                    "field": 'final_price',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '付款方式',
                    "field": 'payment_method',
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
                },
                {
                    "title": '會員電話',
                    "field": 'member_phone',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": 'sync',
                    "field": 'sync',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": []
        })

        _card1.layout.addWidget(_input_form, 0, 0)
        _card1.layout.addWidget(self.order_table, 1, 0)

        return _card1

    def card2(self):
        # this card shows daily revenue of the store
        _card2 = Famcy.FamcyCard()
        _card2.title = "會員管理"

        _input_form = Famcy.input_form()

        phone_num = Famcy.pureInput()
        phone_num.set_submit_value_name("phone_num")
        phone_num.update({
                "title": "電話號碼",
                "desc": "ex. 0900123456"
            })

        points = Famcy.pureInput()
        points.set_submit_value_name("points")
        points.update({
                "title": "點數",
                "desc": "5/-5"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "查詢"
            })
        sb_btn.connect(self.edit_member_info)

        _input_form.layout.addWidget(phone_num, 0, 0)
        _input_form.layout.addWidget(points, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        self.member_table = Famcy.table_block()
        self.member_table.update({
            "input_button": "none",

            "toolbar": False,                                # (true / false)
            "page_footer": False,

            "table_height": "200px",

            "column": [[{
                    "title": '姓名',
                    "field": 'name',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '點數',
                    "field": 'points',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '手機號碼',
                    "field": 'member_phone',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '出生年月日',
                    "field": 'birthday',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '會員等級',
                    "field": 'member_level',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '照片連結',
                    "field": 'img_link',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": []
        })

        _card2.layout.addWidget(_input_form, 0, 0)
        _card2.layout.addWidget(self.member_table, 1, 0)

        return _card2
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def show_order_detail(self, sb, info):
        if info["selected_date"]:
            selected_date = self.convert_to_epoch_time(info["selected_date"])
            start_time = selected_date
            end_time = selected_date + 60*60*24
        else:
            start_time = None
            end_time = None

        res_ind, res_msg = self.get_get_order_information(info["order_num"], start_time, end_time)

        self.order_table.update({
            "data": res_msg
        })

        if res_ind:
            return Famcy.UpdateBlockHtml(target=self.card_1)
        else:
            return Famcy.UpdateAlert(target=self.card_1, alert_message=res_msg)

    def edit_member_info(self, sb, info):
        res_list = []
        if info["points"] and info["points"] != "":
            res_ind, res_msg = self.post_clerk_add_point(info["phone_num"], info["points"])
            res_list = [Famcy.UpdateAlert(target=self.card_2, alert_message=res_msg)]
            
        res_ind, res_msg = self.get_get_member_info(info["phone_num"])
        self.member_table.update({
                "data": [{
                        "name": res_msg["username"],
                        "points": res_msg["reward_points"],
                        "member_phone": res_msg["user_phone"],
                        "birthday": res_msg["birthday"],
                        "member_level": res_msg["membership_level"],
                        "img_link": res_msg["profile_pic_url"]
                    }]
            })
        res_list = [Famcy.UpdateBlockHtml(target=self.card_2)] + res_list
        return res_list
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_get_order_information(self, order_id=None, epoch_time=None, epoch_time_end=None):
        o = "&order_id="+str(order_id) if order_id else ""
        es = "&start_time="+str(epoch_time) if epoch_time else ""
        ee = "&end_time="+str(epoch_time_end) if epoch_time_end else ""
        query = HOST_ADDRESS+"?service=order&operation=get_order_information&store_id="+STORE_ID+o+es+ee
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", res_dict)
        return res_dict["indicator"], res_dict["message"]

    def get_get_member_info(self, phone_num):
        query = HOST_ADDRESS+"?service=member&operation=get_member_info&user_phone="+phone_num
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", res_dict)
        return res_dict["indicator"], json.loads(res_dict["message"])

    def post_clerk_add_point(self, phone_num, points):
        send_dict = {
            "service": "member",
            "operation": "clerk_add_point",
            "user_phone": phone_num,
            "adding_points": points
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", res_dict)
        return res_dict["indicator"], res_dict["message"]
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def convert_to_epoch_time(self, date=None):
        if date:
            date_list = date.split("-")
            y = int(date_list[0])
            m = int(date_list[1])
            d = int(date_list[2])

        return int(datetime.datetime(y,m,d,0,0).timestamp())
    # ====================================================
    # ====================================================

   
orderPage.register("/order", Famcy.NexuniStyle(), permission_level=0, background_thread=False)