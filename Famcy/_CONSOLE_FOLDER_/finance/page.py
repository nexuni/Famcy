import Famcy
import json
import requests
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import read_config_yaml
from os.path import expanduser
import datetime

G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
STORE_ID = "DDA"
HOST_ADDRESS = "http://127.0.0.1:5088/" # "https://store.nexuni-api.com/doday/v1"

class financePage(Famcy.FamcyPage):
    def __init__(self):
        super(financePage, self).__init__()

        # for declaration
        # ===============
        self.card_0 = self.card0()
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()
        self.card_4 = self.card4()
        # ===============

        self.layout.addWidget(self.card_0, 0, 0)
        self.layout.addWidget(self.card_1, 1, 0)
        self.layout.addWidget(self.card_2, 2, 0)
        self.layout.addWidget(self.card_3, 3, 0)
        self.layout.addWidget(self.card_4, 4, 0)
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        # Select date and type in this card
        _card0 = Famcy.FamcyCard()
        _card0.title = "選擇日期和種類產生圖表"

        _input_form = Famcy.input_form()

        selected_day = Famcy.pureInput()
        selected_day.set_submit_value_name("date")
        selected_day.update({
                "title": "選擇日期",
                "desc": ".",
                "input_type": "date"

            })
        selected_type = Famcy.inputList()
        selected_type.set_submit_value_name("type")
        selected_type.update({
                "title": "選擇種類",
                "desc": ".",
                "value": ["全部", "店面", "外送"],
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "產生圖表"
            })
        sb_btn.connect(self.generate_chart)

        _input_form.layout.addWidget(selected_day, 0, 0)
        _input_form.layout.addWidget(selected_type, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        _card0.layout.addWidget(_input_form, 0, 0)

        return _card0

    def card1(self):
        # this card shows daily revenue of the store
        _card1 = Famcy.FamcyCard()
        _card1.title = "單日營業額"

        self.daily_revenue_graph = Famcy.line_chart()
        self.daily_revenue_graph.update({
                "title": "營業額",
                "labels": ["台幣"],
                "values": [{
                    "x": [],
                    "y": [],
                    "mode": "lines+markers",
                    "color": "rgb(225, 0, 0)",
                    "marker_size": 8,
                    "line_width": 3
                }]
            })

        _card1.layout.addWidget(self.daily_revenue_graph, 0, 0)

        return _card1

    def card2(self):
        # this card shows weekly revenue of the store
        _card2 = Famcy.FamcyCard()
        _card2.title = "單周營業額"

        self.weekly_revenue_graph = Famcy.line_chart()
        self.weekly_revenue_graph.update({
                "title": "營業額",
                "labels": ["台幣"],
                "values": [{
                    "x": [],
                    "y": [],
                    "mode": "lines+markers",
                    "color": "rgb(225, 0, 0)",
                    "marker_size": 8,
                    "line_width": 3
                }]
            })

        _card2.layout.addWidget(self.weekly_revenue_graph, 0, 0)

        return _card2

    def card3(self):
        # this card shows monthly revenue of the store
        _card3 = Famcy.FamcyCard()
        _card3.title = "單月營業額"

        self.monthly_revenue_graph = Famcy.line_chart()
        self.monthly_revenue_graph.update({
                "title": "營業額",
                "labels": ["台幣"],
                "values": [{
                    "x": [],
                    "y": [],
                    "mode": "lines+markers",
                    "color": "rgb(225, 0, 0)",
                    "marker_size": 8,
                    "line_width": 3
                }]
            })

        _card3.layout.addWidget(self.monthly_revenue_graph, 0, 0)

        return _card3

    def card4(self):
        # this card shows rank of items
        _card4 = Famcy.FamcyCard()
        _card4.title = "單日產品銷售排行"

        self.item_rank_graph = Famcy.bar_chart()
        self.item_rank_graph.update({
                "values": [{
                    "x": [],
                    "y": [],
                    "color": "rgb(225, 0, 0)"
                }],
                "labels": [""],
                "title": "產品銷售排行",
                "xy_axis_title": ["產品", "銷售數量"],
                "size": ["100%", 500]
            })

        _card4.layout.addWidget(self.item_rank_graph, 0, 0)

        return _card4
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def generate_chart(self, sb, info):
        d_res_ind, d_res_msg = self.get_chart_data(info, "day")
        w_res_ind, w_res_msg = self.get_chart_data(info, "week")
        m_res_ind, m_res_msg = self.get_chart_data(info, "month")
        p_res_ind, p_res_msg = self.get_chart_data(info, "product")

        if d_res_ind and w_res_ind and m_res_ind and p_res_ind:
            self.daily_revenue_graph.update({
                "values": [i for i in d_res_msg["data_list"]]
            })
            self.weekly_revenue_graph.update({
                "values": [i for i in w_res_msg["data_list"]]
            })
            self.monthly_revenue_graph.update({
                "values": [i for i in m_res_msg["data_list"]]
            })
            self.item_rank_graph.update({
                "values": [i for i in p_res_msg["data_list"]]
            })
            return [Famcy.UpdateBlockHtml(target=self.card_1), Famcy.UpdateBlockHtml(target=self.card_2), Famcy.UpdateBlockHtml(target=self.card_3), Famcy.UpdateBlockHtml(target=self.card_4)]

        else:
            return Famcy.UpdateAlert(target=self.card_0, alert_message="資料異常，請重新再試")
        
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_chart_data(self, info, graph_type):
        selected_day = self.convert_to_epoch_time(info["date"])

        # set parameter platform
        # if info["type"] == "全部":
        #     p = "platform=all"
        # elif info["type"] == "店面":
        #     p = "platform=store"
        # elif info["type"] == "外送":
        #     p = "platform=delivery"
        p = "platform="+json.dumps(["all", "store", "delivery"])

        # get different graph
        if graph_type == "day":
            t = "start_time="+json.dumps([selected_day, selected_day, selected_day])+"&end_time="+json.dumps([str(int(selected_day)+60*60*24), str(int(selected_day)+60*60*24), str(int(selected_day)+60*60*24)])
            s = "scope="+json.dumps(["hourly", "hourly", "hourly"])

        elif graph_type == "week":
            t = "start_time="+json.dumps([str(int(selected_day)-60*60*24*7), str(int(selected_day)-60*60*24*7), str(int(selected_day)-60*60*24*7)])+"&end_time="+json.dumps([selected_day, selected_day, selected_day])
            s = "scope="+json.dumps(["daily", "daily", "daily"])

        elif graph_type == "month":
            t = "start_time="+json.dumps([str(int(selected_day)-60*60*24*30), str(int(selected_day)-60*60*24*30), str(int(selected_day)-60*60*24*30)])+"&end_time="+json.dumps([selected_day, selected_day, selected_day])
            s = "scope="+json.dumps(["daily", "daily", "daily"])

        elif graph_type == "product":
            t = "start_time="+json.dumps([selected_day, selected_day, selected_day])+"&end_time="+json.dumps([str(int(selected_day)+60*60*24), str(int(selected_day)+60*60*24), str(int(selected_day)+60*60*24)])
            s = "scope="+json.dumps(["product", "product", "product"])

        query = HOST_ADDRESS+"?service=order&operation=get_order_revenue&advance=True&store_id="+STORE_ID+"&"+t+"&"+s+"&"+p
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)

        return res_dict["indicator"], res_dict["message"]
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def convert_to_epoch_time(self, date=None, y=None, m=None, d=None):
        if date:
            date_list = date.split("-")
            y = int(date_list[0])
            m = int(date_list[1])
            d = int(date_list[2])

        return str(int(datetime.datetime(y,m,d,0,0).timestamp()))
    # ====================================================
    # ====================================================

   
financePage.register("/finance", Famcy.NexuniStyle(), permission_level=0, background_thread=False)