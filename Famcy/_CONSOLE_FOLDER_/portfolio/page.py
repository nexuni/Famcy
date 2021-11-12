import Famcy
import json

class PortfolioPage(Famcy.FamcyPage):
    def __init__(self):
        super(PortfolioPage, self).__init__("/portfolio", Famcy.PortfolioStyle(), background_thread=False)
        
        self.table_info = []

        self.card_1 = self.card1()
        self.layout.addWidget(self.card_1, 0, 0)

    def card1(self):
        card1 = Famcy.FamcyCard()
        # card1.title = "test"

        card1.preload = self.get_history_order
        card1.body.style += "padding: 50px;"

        input_form = Famcy.input_form()

        table_content = Famcy.table_block()
        table_content.update({
                "input_button": "checkbox",
                "input_value_col_field": "datetime",
                "page_detail": False,
                "page_detail_content": ["<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>"],
                "page_footer": True,
                "page_footer_detail": {
                    "page_size": 10,
                    "page_list": [10, 20, "all"]
                },
                "column": [[{
                        "title": 'datetime',
                        "field": 'datetime',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'order',
                        "field": 'order',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'total_price',
                        "field": 'total_price',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'used_point',
                        "field": 'used_point',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    }
                ]],
                "data": self.table_info
          })

        submit_btn = Famcy.submitBtn()
        submit_btn.connect(self.submit_table, target=card1)

        input_form.layout.addWidget(table_content, 0, 0)
        input_form.layout.addWidget(submit_btn, 1, 0)

        card1.layout.addWidget(input_form, 0, 0)
        return card1

    def get_history_order(self):
        send_dict = {
            "service": "member",
            "operation": "get_history_order",
            "user_phone": "0905860683"
        }
        res_str = Famcy.FManager.http_client.client_get("member_http_url", send_dict, gauth=True)
        res_ind = json.loads(res_str)["indicator"]
        res_msg = json.loads(res_str)["message"]

        self.table_info = [{
                    "datetime": "1",
                    "order": "2",
                    "total_price": "3",
                    "used_point": "4"
                },
                {
                    "datetime": "5",
                    "order": "6",
                    "total_price": "7",
                    "used_point": "8"
                }]
        self.card_1.layout.content[0][0].layout.content[0][0].update({
            "data": self.table_info
        })

    def submit_table(self, submission_obj, info_list):
        return Famcy.UpdateAlert(alert_message=str(info_list))

page = PortfolioPage()
page.register()