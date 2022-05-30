import Famcy

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
        edit_action.update({
                "title": "操作性質",
                "value": ["放入錢幣", "拿出錢幣"]
            })
        coin_type = Famcy.inputList()
        coin_type.update({
                "title": "硬幣種類",
                "value": ["1", "5", "10", "50"]
            })
        amount = Famcy.pureInput()
        amount.update({
                "title": "數量",
                "input_type": "number"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "更改"
            })

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
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
machinePage.register("/machine", Famcy.ClassicStyle(), permission_level=0, background_thread=False)