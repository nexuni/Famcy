import Famcy

class employeePage(Famcy.FamcyPage):
    def __init__(self):
        super(employeePage, self).__init__()

        # for declaration
        # ===============
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()
        self.card_4 = self.card4()
        # ===============

        self.layout.addWidget(self.card_1, 0, 0, 1, 3)
        self.layout.addWidget(self.card_2, 1, 0)
        self.layout.addWidget(self.card_3, 1, 1)
        self.layout.addWidget(self.card_4, 1, 2)
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card1(self):
        # this card shows daily revenue of the store
        _card1 = Famcy.FamcyCard()
        _card1.title = "查看員工薪水"

        _input_form = Famcy.input_form()

        employee = Famcy.inputList()
        employee.update({
                "title": "選擇員工",
                "value": ["Julia", "Leo", "Weitung"]
            })
        year_month = Famcy.pureInput()
        year_month.update({
                "title": "選擇查看月份",
                "input_type": "month"
            })
        sb_btn = Famcy.submitBtn(parent=_card1)
        sb_btn.update({
                "title": "查詢"
            })
        # sb_btn.setGeometry(200, 200, 200, 200)

        _input_form.layout.addWidget(employee, 0, 0)
        _input_form.layout.addWidget(year_month, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        self.salary_table = Famcy.table_block()
        self.salary_table.update({
            "input_button": "radio",                     # ("checkbox" / "radio" / "none")
            "input_value_col_field": "name",          # if input_button != "none"

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
                    "title": '員工代碼',
                    "field": 'doday_id',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '匯款帳號',
                    "field": 'account_num',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '工作性質',
                    "field": 'job_type',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '時薪/月薪',
                    "field": 'salary_per_hour',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '工作時長',
                    "field": 'work_time',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '薪水',
                    "field": 'salary',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '總加給項目',
                    "field": 'bonus',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '總應付項目',
                    "field": 'extra_paid',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '應收薪水',
                    "field": 'final_salary',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": [
                {
                    "name": "Julia",
                    "doday_id": "julia",
                    "account_num": "01234567890",
                    "job_type": "part-time",
                    "salary_per_hour": "170",
                    "work_time": "140",
                    "salary": "19600",
                    "bonus": "200",
                    "extra_paid": "-600",
                    "final_salary": "20000"
                }
            ]
        })

        _card1.layout.addWidget(_input_form, 0, 0)
        _card1.layout.addWidget(self.salary_table, 1, 0)

        return _card1

    def card2(self):
        # this card provides managers to edit employees' working time
        _card2 = Famcy.FamcyCard()
        _card2.title = "編輯員工打卡紀錄"

        _input_form = Famcy.input_form()

        employee = Famcy.inputList()
        employee.update({
                "title": "選擇員工",
                "value": ["Julia", "Leo", "Weitung"]
            })
        edit_action = Famcy.inputList()
        edit_action.update({
                "title": "選擇更改方式",
                "value": ["增加打卡時間", "刪除打卡時間"]
            })
        start_time = Famcy.pureInput()
        start_time.update({
                "title": "選擇開始時間",
                "input_type": "datetime-local"
            })
        end_time = Famcy.pureInput()
        end_time.update({
                "title": "選擇結束時間",
                "input_type": "datetime-local"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "更改"
            })

        _input_form.layout.addWidget(employee, 0, 0)
        _input_form.layout.addWidget(edit_action, 1, 0)
        _input_form.layout.addWidget(start_time, 2, 0)
        _input_form.layout.addWidget(end_time, 3, 0)
        _input_form.layout.addWidget(sb_btn, 4, 0)

        _card2.layout.addWidget(_input_form, 0, 0)

        return _card2

    def card3(self):
        # this card generates the salary table of selected month
        _card3 = Famcy.FamcyCard()
        _card3.title = "薪水結算"

        _input_form = Famcy.input_form()

        year_month = Famcy.pureInput()
        year_month.update({
                "title": "選擇查看月份",
                "input_type": "month"
            })

        _input_form.layout.addWidget(year_month, 0, 0)

        _upload_form = Famcy.upload_form()

        salary_file = Famcy.uploadFile()
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "上傳"
            })

        _upload_form.layout.addWidget(salary_file, 0, 0)
        _upload_form.layout.addWidget(sb_btn, 1, 0)

        _card3.layout.addWidget(_input_form, 0, 0)
        _card3.layout.addWidget(_upload_form, 1, 0)

        return _card3

    def card4(self):
        # this card provides managers to add or delete employees' account
        _card4 = Famcy.FamcyCard()
        _card4.title = "新增移除員工帳號"

        _input_form = Famcy.input_form()

        employee_name = Famcy.pureInput()
        employee_name.update({
                "title": "輸入員工帳號"
            })
        edit_action = Famcy.inputList()
        edit_action.update({
                "title": "選擇編輯帳號",
                "value": ["新增帳號", "刪除帳號"]
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "確認"
            })

        _input_form.layout.addWidget(employee_name, 0, 0)
        _input_form.layout.addWidget(edit_action, 1, 0)
        _input_form.layout.addWidget(sb_btn, 2, 0)

        _card4.layout.addWidget(_input_form, 0, 0)

        return _card4
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

   
employeePage.register("/employee", Famcy.NexuniStyle(), permission_level=0, background_thread=False)