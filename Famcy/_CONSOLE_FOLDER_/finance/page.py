import Famcy
import json
import requests

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
                "value": ["全部", "店面", "Uber", "Foodpanda"],
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
        res_ind, res_msg = self.get_chart_data(info)

        if res_ind:
            self.daily_revenue_graph.update({
                "values": [{
                    "x": res_msg["day"]["data"]["x"],
                    "y": res_msg["day"]["data"]["y"],
                    "mode": "lines+markers",
                    "color": "rgb(225, 0, 0)",
                    "marker_size": 8,
                    "line_width": 3
                }]
            })
            self.weekly_revenue_graph.update({
                "values": [{
                    "x": res_msg["week"]["data"]["x"],
                    "y": res_msg["week"]["data"]["y"],
                    "mode": "lines+markers",
                    "color": "rgb(225, 0, 0)",
                    "marker_size": 8,
                    "line_width": 3
                }]
            })
            self.monthly_revenue_graph.update({
                "values": [{
                    "x": res_msg["month"]["data"]["x"],
                    "y": res_msg["month"]["data"]["y"],
                    "mode": "lines+markers",
                    "color": "rgb(225, 0, 0)",
                    "marker_size": 8,
                    "line_width": 3
                }]
            })
            self.item_rank_graph.update({
                "values": [{
                    "x": res_msg["item"]["data"]["x"],
                    "y": res_msg["item"]["data"]["y"],
                    "color": "rgb(225, 0, 0)"
                }],
            })
            return [Famcy.UpdateBlockHtml(target=self.card_1), Famcy.UpdateBlockHtml(target=self.card_2), Famcy.UpdateBlockHtml(target=self.card_3), Famcy.UpdateBlockHtml(target=self.card_4)]

        else:
            return Famcy.UpdateAlert(target=self.card_0, alert_message=res_msg)
        
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_chart_data(self, info):
        send_dict = {
            "platform": "store", # "uber"   info["type"]
            "store_name": "DDA",
            "date": info["date"].replace("-","")
        }

        # res_str = Famcy.FManager.http_client.client_get("doday_http_url", send_dict, gauth=False)
        res_str = requests.get("http://127.0.0.1:5000/revenue", params=send_dict).text
        res_ind = json.loads(res_str)["indicator"]
        res_msg = json.loads(res_str)["message"]

        return res_ind, res_msg
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
financePage.register("/finance", Famcy.ClassicStyle(), permission_level=0, background_thread=False)