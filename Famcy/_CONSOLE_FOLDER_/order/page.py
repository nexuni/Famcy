import Famcy

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
        order_num.update({
                "title": "輸入單號",
                "desc": "ex. DDA-20210901-5003"
            })

        year_month = Famcy.pureInput()
        year_month.update({
                "title": "選擇日期",
                "desc": ".",
                "input_type": "date"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "查詢"
            })

        _input_form.layout.addWidget(order_num, 0, 0)
        _input_form.layout.addWidget(year_month, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        self.order_table = Famcy.table_block()
        self.order_table.update({
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
                    "title": '點餐編號',
                    "field": 'order_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '序號',
                    "field": 'num',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '店',
                    "field": 'store',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '系列',
                    "field": 'category',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '品名',
                    "field": 'item_name',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '配料',
                    "field": 'addon',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '用餐方式',
                    "field": 'stay_or_togo',
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
            "data": [
                {
                    "order_id": "DDA-20210901-5003",
                    "num": "1",
                    "store": "DDA",
                    "category": "推薦系列",
                    "item_name": "絕配1. 紅豆、芋圓、粉圓豆花",
                    "addon": '{"冷熱冰量": ["去冰"], "湯底": ["糖水(半糖)"], "附加選項(熱的才可選擇薑汁)": []}',
                    "stay_or_togo": "stay",
                    "amount": "2",
                    "final_price": "120",
                    "payment_method": "creditcard",
                    "status": "preparing",
                    "member_phone": "01234567890",
                    "sync": "True"
                }
            ]
        })

        _card1.layout.addWidget(_input_form, 0, 0)
        _card1.layout.addWidget(self.order_table, 1, 0)

        return _card1

    def card2(self):
        # this card shows daily revenue of the store
        _card2 = Famcy.FamcyCard()
        _card2.title = "會員管理"

        _input_form = Famcy.input_form()

        order_num = Famcy.pureInput()
        order_num.update({
                "title": "電話號碼",
                "desc": "ex. 0900123456"
            })

        year_month = Famcy.pureInput()
        year_month.update({
                "title": "點數",
                "desc": "5/-5"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "查詢"
            })

        _input_form.layout.addWidget(order_num, 0, 0)
        _input_form.layout.addWidget(year_month, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        self.member_table = Famcy.table_block()
        self.member_table.update({
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
            "data": [
                {
                    "name": "julia",
                    "points": "100",
                    "member_phone": "01234567890",
                    "birthday": "20010703",
                    "member_level": "none",
                    "img_link": ""
                    
                }
            ]
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

   
orderPage.register("/order", Famcy.ClassicStyle(), permission_level=0, background_thread=False)