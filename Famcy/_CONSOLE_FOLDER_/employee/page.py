import Famcy
import json
import requests
import urllib.parse
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import read_config_yaml
from os.path import expanduser
import datetime


G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
STORE_ID = "DDA"
HOST_ADDRESS = "http://127.0.0.1:5089" # "https://management.doday.com.tw/v1"

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
        employee.set_submit_value_name("name")
        employee.update({
                "title": "選擇員工",
                "value": ["Bonnie", "Chia"]
            })
        year_month = Famcy.pureInput()
        year_month.set_submit_value_name("yearmonth")
        year_month.update({
                "title": "選擇查看月份",
                "input_type": "month"
            })
        sb_btn = Famcy.submitBtn(parent=_card1)
        sb_btn.update({
                "title": "查詢"
            })
        sb_btn.connect(self.generate_employee_info_table)

        _input_form.layout.addWidget(employee, 0, 0)
        _input_form.layout.addWidget(year_month, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        self.salary_table = Famcy.table_block()
        self.salary_table.update({
            "input_button": "none",                     # ("checkbox" / "radio" / "none")
            
            "toolbar": False,                                # (true / false)
            "page_footer": True,                            # (true / false)
            "page_footer_detail": {                         # if page_footer == true
                "page_size": 100,
                "page_list": [1, 2, "all"]
            },

            "table_height": "150px",

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
            "data": []
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
        employee.set_submit_value_name("employee")
        employee.update({
                "title": "選擇員工",
                "value": ["Julia", "Leo", "Weitung"]
            })
        edit_action = Famcy.inputList()
        edit_action.set_submit_value_name("edit_action")
        edit_action.update({
                "title": "選擇更改方式",
                "value": ["增加上班打卡時間", "增加下班打卡時間", "刪除打卡時間"]
            })
        edit_time = Famcy.pureInput()
        edit_time.set_submit_value_name("time")
        edit_time.update({
                "title": "選擇時間",
                "input_type": "datetime-local"
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "更改"
            })
        sb_btn.connect(self.edit_employee_checkin_data)

        _input_form.layout.addWidget(employee, 0, 0)
        _input_form.layout.addWidget(edit_action, 1, 0)
        _input_form.layout.addWidget(edit_time, 2, 0)
        _input_form.layout.addWidget(sb_btn, 3, 0)

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
        employee_name.set_submit_value_name("name")
        employee_name.update({
                "title": "輸入員工帳號"
            })
        edit_action = Famcy.inputList()
        edit_action.set_submit_value_name("edit_action")
        edit_action.update({
                "title": "選擇編輯帳號",
                "value": ["新增帳號", "刪除帳號"]
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "確認"
            })
        sb_btn.connect(self.add_new_user)

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
    def generate_employee_info_table(self, sb, info):
        # TODO: can work in "https://management.doday.com.tw/v1", but cannot work in "http://127.0.0.1:5089"

        temp_dict = {'addition': {}, 'comment': 'comment', 'deductions': {}}

        # get checkin data
        s = self.get_history_checkin_data(info["yearmonth"].replace("-", ""), info["name"])
        temp_dict["salary_hours"] = round(float(s['salary_hour']),2)

        res_ind, res_msg = self.get_salary_data(info["yearmonth"][:4], info["yearmonth"][-2:], {info["name"]: temp_dict})

        if res_ind:
            # get employee's info
            employee_info = res_msg[info["name"]]

            # calculate bonus
            plus_amount = 0
            for j in employee_info["addition"].keys(): plus_amount += employee_info["addition"][j]
            
            # calculate extra paid
            deduction_amount = 0
            for j in employee_info["deductions"].keys(): deduction_amount += employee_info["deductions"][j]
            
            # update table info
            self.salary_table.update({
                    "data": [
                        {
                            "name": employee_info["name"],
                            "doday_id": info["name"],
                            "account_num": employee_info["saving_account"],
                            "job_type": employee_info["working_type"],
                            "salary_per_hour": employee_info['monthly_rate'],
                            "work_time": employee_info['salary_hours'],
                            "salary": employee_info['salary_amount'],
                            "bonus": plus_amount,
                            "extra_paid": deduction_amount,
                            "final_salary": employee_info['salary_amount']+plus_amount-deduction_amount
                        }
                    ]
                })
            return Famcy.UpdateBlockHtml(target=self.salary_table)

        else:
            return Famcy.UpdateAlert(target=self.card_1, alert_message=res_msg)

    def edit_employee_checkin_data(self, sb, info):
        time_list = info["time"].replace(":", "-").replace("T", "-").split("-")
        epoch_time = int(datetime.datetime(int(time_list[0]), int(time_list[1]), int(time_list[2]), int(time_list[3]), int(time_list[4])).timestamp())
        
        if info["edit_action"] == "刪除打卡時間":
            res_msg = self.post_modification(info["employee"], epoch_time)
        else:
            checkin_state = "0" if "上班" in info["edit_action"] else "1"
            res_msg = self.post_checkin(info["employee"], epoch_time, checkin_state)

        return Famcy.UpdateAlert(target=self.card_2, alert_message=res_msg)

    def add_new_user(self, sb, info):
        # TODO: cancel account
        # TODO: these APIs (checkin, modification, generate) are really weird, if posible should
        # rewrite these function
        if info["edit_action"] == "新增帳號":
            res_msg = self.post_generate(info["name"])
        else:
            res_msg = "操作有誤，請重新再試"
        return Famcy.UpdateAlert(target=self.card_4, alert_message=res_msg)

        
        
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_history_checkin_data(self, yearmonth, name):
        query = HOST_ADDRESS + "?service=checkin&operation=getcheckindata&yearmonth="+yearmonth+"&username="+name
        r = requests.get(query, headers=HEADER).text
        
        res_dict = json.loads(r)
        print("res_dict1: ", res_dict)
        return res_dict

    def get_salary_data(self, year, month, data):
        query = HOST_ADDRESS + "?service=employee_management&operation=calculate_salary"+"&year="+str(year)+"&month="+str(int(month))+"&data="+json.dumps(data)
        r = requests.get(query, headers=HEADER).text
        
        res_dict = json.loads(r)
        print("res_dict2: ", res_dict)
        return res_dict["indicator"], res_dict["message"]

    def post_checkin(self, name, epoch_time, checkin_state):
        send_dict = {
            "service":"checkin",
            "operation":"checkin",
            "time": epoch_time,
            "username": name,
            "checkin_state": checkin_state,
            "checkin_store": STORE_ID
        }

        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        return urllib.parse.unquote(r)

    def post_modification(self, name, time):
        send_dict = {
            "service":"checkin",
            "operation":"modification",
            "time": time,
            "username": name,
            "checkin_state": "-1",
            "checkin_store": STORE_ID
        }

        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        return urllib.parse.unquote(r)

    def post_generate(self, name):
        send_dict = {
            "service": "checkin", 
            "operation": "generate", 
            "username": name, 
            "checkin_store": STORE_ID
        }

        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        return urllib.parse.unquote(r)

    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
employeePage.register("/employee", Famcy.NexuniStyle(), permission_level=0, background_thread=False)