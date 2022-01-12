import Famcy
import io
import os
import json
import datetime
import requests
import boto3
import pandas as pd
import xlsxwriter

class SeasonPage(Famcy.FamcyPage):
    def __init__(self):
        super(SeasonPage, self).__init__()

        self.get_carpark_id()# init carpark_id 

        self.table_info = []
        self.carpark_id = "park1"

        self.p_del_card = self.p_card_delete()
        self.p_update_card = self.p_card_update()
        self.p_insert_card = self.p_card_insert()
        self.p_upload_table_card = self.p_card_upload_table()

        self.layout.addStaticWidget(self.p_del_card)
        self.layout.addStaticWidget(self.p_update_card)
        self.layout.addStaticWidget(self.p_insert_card, 60)
        self.layout.addStaticWidget(self.p_upload_table_card)


        self.card_1 = self.card1()
        self.card_2 = self.card2()

        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 1, 0)


    # card
    # ====================================================
    def card1(self):
        card1 = Famcy.FamcyCard()

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        default_date, default_time, default_end_date, default_end_time = self.get_default_date_time()

        input_date.update({"title": "輸入起始日期", "input_type": "date", "defaultValue": default_date})
        input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": default_time})
        input_date2.update({"title": "輸入結束日期", "input_type": "date", "defaultValue": default_end_date})
        input_time2.update({"title": "輸入結束時間", "input_type": "time", "defaultValue": default_end_time})


        input_license = Famcy.pureInput()
        input_license.update({"title": "輸入車牌號碼"})

        input_phone = Famcy.pureInput()
        input_phone.update({"title": "輸入電話號碼", "input_type":"number"})


        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢月票"})
        search_btn.connect(self.update_search, target=card1)

        insert_btn = Famcy.submitBtn()
        insert_btn.update({"title": "新增月票"})
        insert_btn.connect(self.prompt_submit_input, target=self.p_insert_card)


        upload_btn = Famcy.submitBtn()
        upload_btn.update({"title": "批次上傳月票資料"})
        upload_btn.connect(self.prompt_submit_input, target=self.p_upload_table_card)

        download_btn = Famcy.submitBtn()
        download_btn.update({"title": "下載月票表格"})
        download_btn.connect(self.download_table, target=card1)

        download_link = Famcy.downloadFile()
        download_link.update({"title": "","file_path": 'http://127.0.0.1:5000/robots.xlsx',"file_name": 'download'})
        download_link.body.children[0]["style"] = "visibility: hidden;"

        input_form.layout.addWidget(input_date, 0, 0, 2, 1)
        input_form.layout.addWidget(input_time, 0, 1, 2, 1)
        input_form.layout.addWidget(input_date2, 0, 2, 2, 1)
        input_form.layout.addWidget(input_time2, 0, 3, 2, 1)

        input_form.layout.addWidget(input_license, 2, 0, 2, 1)
        input_form.layout.addWidget(input_phone, 2, 1, 2, 1)

        input_form.layout.addWidget(search_btn, 0, 4)
        input_form.layout.addWidget(insert_btn, 1, 4)
        input_form.layout.addWidget(upload_btn, 2, 4)
        input_form.layout.addWidget(download_btn, 3, 4)

        input_form.layout.addWidget(download_link, 4, 0, 1, 5)

        card1.layout.addWidget(input_form, 0, 0)

        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()
        card2.preload = self.get_season_data

        input_form = Famcy.input_form()
        input_form.body.style["word-break"] = "break-all !important"


        # self.table_info = self.make_time_readable(self.table_info,["validstart","validend"])
        # print("self.table_info===========",self.table_info)
        

        table_content = Famcy.table_block()
        table_content.update({
                "toolbar": False,
                "input_button": "radio",
                "input_value_col_field": "id",
                "page_detail": False,
                "page_detail_content": ["<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>", "<div style='display: flex;'><p style='width: 50%;'>交易紀錄: </p><p style='width: 50%;text-align: right;'>一些紀錄</p></div>"],
                "page_footer": True,
                "page_footer_detail": {
                    "page_size": 15,
                    "page_list": [15, "all"]
                },
                "column": [[
                    {
                        "title": '月票類型',
                        "field": '_season_type',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": '車牌號碼',
                        "field": 'platenum',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": '電話號碼',
                        "field": 'phonenum',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": '開始時間',
                        "field": '_validstart',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": '結束時間',
                        "field": '_validend',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": '月票費用',
                        "field": 'monthly_fee',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    },
                    {
                        "title": 'comments',
                        "field": 'comments',
                        "rowspan": 1,
                        "align": 'center',
                        "valign": 'middle',
                        "sortable": True
                    }
                ]],
                "data": self.table_info
          })

        # self.table_info = self.make_time_readable_reverse(self.table_info,["validstart","validend"])

        new_btn = Famcy.submitBtn()
        new_btn.update({"title": "更新月票資訊"})
        new_btn.connect(self.update_table_prompt, target=self.p_update_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title": "刪除月票"})
        cancel_btn.connect(self.prompt_submit_input, target=self.p_del_card)

        input_form.layout.addWidget(table_content, 0, 0, 1, 2)
        input_form.layout.addWidget(new_btn, 1, 0)
        input_form.layout.addWidget(cancel_btn, 1, 1)

        card2.layout.addWidget(input_form, 0, 0)

        return card2
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def p_card_upload_table(self):
        p_card = Famcy.FamcyPromptCard()

        upload_form = Famcy.upload_form()

        upload_file = Famcy.uploadFile()
        upload_file.update({
                "title": "檔案上傳",
                "file_num": "single",
                "accept_type": ["xls", "xlsx"],
                "file_path": '/home/minc/Downloads/',
            })

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.upload_table, target=p_card)

        upload_form.layout.addWidget(upload_file, 0, 0)
        upload_form.layout.addWidget(submit_btn, 0, 1)

        input_form = Famcy.input_form()

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(cancel_btn, 0, 0)

        p_card.layout.addWidget(upload_form, 0, 0)
        p_card.layout.addWidget(input_form, 1, 0)

        return p_card

    def p_card_insert(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        phonenum = Famcy.pureInput()
        phonenum.update({"title":"電話號碼:", "input_type":"number"})

        license_num = Famcy.pureInput()
        license_num.update({"title":"車牌號碼:", "input_type":"text"})

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time"})

        database_name = Famcy.inputList()
        database_name.update({
                "title": "資料庫名:",
                "value": ["season", "season_ticket"],
            })

        season_type = Famcy.inputList()
        season_type.update({
                "title": "月票種類:",
                "value": ["season", "dailyseason"],
            })

        month_fee = Famcy.pureInput()
        month_fee.update({"title":"月費:", "input_type":"number"})

        comments = Famcy.pureInput()
        comments.update({"title":"備註:", "input_type":"text"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_insert, target=p_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(phonenum, 0, 0)
        input_form.layout.addWidget(license_num, 0, 1)
        input_form.layout.addWidget(input_date, 1, 0)
        input_form.layout.addWidget(input_time, 1, 1)
        input_form.layout.addWidget(input_date2, 2, 0)
        input_form.layout.addWidget(input_time2, 2, 1)
        input_form.layout.addWidget(database_name, 3, 0)
        input_form.layout.addWidget(season_type, 3, 1)
        input_form.layout.addWidget(month_fee, 4, 0)
        input_form.layout.addWidget(comments, 4, 1)
        input_form.layout.addWidget(cancel_btn, 5, 0)
        input_form.layout.addWidget(submit_btn, 5, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def p_card_update(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        input_id = Famcy.pureInput()
        input_id.update({"title":"ID:", "input_type":"number"})

        license_num = Famcy.pureInput()
        license_num.update({"title":"車牌號碼:", "input_type":"text"})

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time"})

        comments = Famcy.pureInput()
        comments.update({"title":"備註:", "input_type":"text"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.update_modify, target=p_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(input_id, 0, 0, 1, 2)
        input_form.layout.addWidget(license_num, 1, 0, 1, 2)
        input_form.layout.addWidget(input_date, 2, 0)
        input_form.layout.addWidget(input_time, 2, 1)
        input_form.layout.addWidget(input_date2, 3, 0)
        input_form.layout.addWidget(input_time2, 3, 1)
        input_form.layout.addWidget(comments, 4, 0, 1, 2)
        input_form.layout.addWidget(cancel_btn, 5, 0)
        input_form.layout.addWidget(submit_btn, 5, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def p_card_delete(self):
        pcard = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        text_msg = Famcy.displayParagraph()
        text_msg.update({"title": "確認是否執行?", "content": ""})

        confirm_btn = Famcy.submitBtn()
        confirm_btn.update({"title":"確認"})
        confirm_btn.connect(self.update_delete)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"取消"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(text_msg, 0, 0, 1, 2)
        input_form.layout.addWidget(confirm_btn, 1, 0)
        input_form.layout.addWidget(cancel_btn, 1, 1)

        pcard.layout.addWidget(input_form, 0, 0)

        return pcard
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def prompt_remove_input(self, submission_obj, info_list):
        return Famcy.UpdateRemoveElement(prompt_flag=True)

    def prompt_submit_input(self, submission_obj, info_list):
        submission_obj.target.last_card = submission_obj.origin.find_parent(submission_obj.origin, "FCard")
        submission_obj.target.last_card["info_list"] = info_list
        return Famcy.UpdatePrompt()

    def update_table_prompt(self, submission_obj, info_list):
        target = submission_obj.target
        if len(info_list[0]) > 0:
            _id = str(info_list[0][0])
            for item in self.table_info:
                if str(item["id"]) == str(_id):
                    target.layout.content[0][0].layout.content[0][0].update({"defaultValue": str(item["id"])})
                    target.layout.content[0][0].layout.content[1][0].update({"defaultValue": item["platenum"]})
                    target.layout.content[0][0].layout.content[2][0].update({"defaultValue": "20"+item["validstart"][:2]+"-"+item["validstart"][2:4]+"-"+item["validstart"][4:6]})
                    target.layout.content[0][0].layout.content[3][0].update({"defaultValue": item["validstart"][6:8]+":"+item["validstart"][8:10]})
                    target.layout.content[0][0].layout.content[4][0].update({"defaultValue": "20"+item["validend"][:2]+"-"+item["validend"][2:4]+"-"+item["validend"][4:6]})
                    target.layout.content[0][0].layout.content[5][0].update({"defaultValue": item["validend"][6:8]+":"+item["validend"][8:10]})
                    target.layout.content[0][0].layout.content[6][0].update({"defaultValue": item["comments"]})
                    return Famcy.UpdatePrompt()

        return Famcy.UpdateAlert(alert_message="請重新再試")


    def update_search(self, submission_obj, info_list):
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            license_num = str(info_list[4][0])
            phonenum = str(info_list[5][0])

            self.get_season_data(phonenum=phonenum, start_time=start_time, end_time=end_time, platenum=license_num)
            return Famcy.UpdateBlockHtml(target=self.card_2)

        return Famcy.UpdateAlert(alert_message="系統異常，請重新再試")

    def update_delete(self, submission_obj, info_list):
        _info_list = submission_obj.origin.find_parent(submission_obj.origin, "FPromptCard").last_card["info_list"]
        print("_info_list: ", _info_list)
        msg = "資料填寫有誤"
        if len(_info_list) > 0 and len(_info_list[0]) > 0:
            _id = str(_info_list[0][0])
            license_num = "XXXXXX"

            if self.post_modify(_id, license_num):
                self.get_season_data()
                msg = "成功刪除資料"

            return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdateBlockHtml(target=self.card_2), Famcy.UpdateAlert(alert_message=msg, target=self.card_2)]
        return Famcy.UpdateAlert(alert_message=msg, target=self.p_del_card)

    def update_modify(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            _id = str(info_list[0][0])
            license_num = str(info_list[1][0])
            start_time = info_list[2][0][:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            end_time = info_list[4][0][:4] + info_list[4][0][5:7] + info_list[4][0][8:10] + info_list[5][0][:2] + info_list[5][0][3:] + "00000"
            comments = str(info_list[6][0])

            if self.post_modify(_id, license_num, start_time=start_time, end_time=end_time, comments=comments):
                self.get_season_data()
                msg = "成功修改資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

    def update_insert(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            phonenum = str(info_list[0][0])
            license_num = str(info_list[1][0])
            start_num = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            end_num = info_list[4][0][2:4] + info_list[4][0][5:7] + info_list[4][0][8:10] + info_list[5][0][:2] + info_list[5][0][3:] + "00000"
            database_name = str(info_list[6][0])
            season_type = str(info_list[7][0])
            month_fee = str(info_list[8][0])
            comments = str(info_list[9][0])
            if self.post_insert(phonenum, license_num, start_num, end_num, database_name, season_type, month_fee, comments):
                self.get_season_data()
                msg = "成功加入資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2)]

    def download_table(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        extra_script = ""

        try:
            file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".xlsx"

            s3_client = boto3.client("s3")

            books_df = pd.DataFrame(
                data=self.change_table_info_to_dict(),
                columns=self.change_table_info_to_dict().keys(),
            )

            with io.BytesIO() as csv_buffer:
                with pd.ExcelWriter(csv_buffer, engine='xlsxwriter') as writer:
                    books_df.to_excel(writer,index=False)

                response = s3_client.put_object(
                    Bucket="gadgethi-css", Key="pms_download/"+file_name, Body=csv_buffer.getvalue()
                )

            self.card_1.layout.content[0][0].layout.content[10][0].update({"file_path": 'https://gadgethi-css.s3.amazonaws.com/pms_download/'+file_name})
            extra_script = "document.getElementById('" + self.card_1.layout.content[0][0].layout.content[10][0].id + "_input').click();"

            msg = "成功加入資料"
        except Exception as e:
            msg=str(e)

        return [Famcy.UpdateBlockHtml(target=self.card_1.layout.content[0][0].layout.content[10][0]), Famcy.UpdateAlert(alert_message=msg, extra_script=extra_script)]

    def upload_table(self, submission_obj, info_list):
        print("======upload_table========")
        msg = "檔案上傳失敗，請重新再試"
        if info_list[0][0]["indicator"]:
            file_path = self.p_upload_table_card.layout.content[0][0].layout.content[0][0].value["file_path"]+info_list[0][0]["message"]
            print("file_path: ", file_path)
            table_info = self.read_excel_file(file_path)
            if self.post_insert(table_info["phonenum"], table_info["platenum"], table_info["validstart"], table_info["validend"], "season", table_info["season_type"], table_info["monthly_fee"], table_info["comments"]):
                self.get_season_data()
                msg = "成功加入資料"
                print("end")
                extra_script = "$('#table_%s').bootstrapTable('load', %s)" % (self.card_2.layout.content[0][0].layout.content[0][0].id, self.table_info)
            
        return [Famcy.UpdateRemoveElement(prompt_flag=True, extra_script=extra_script), Famcy.UpdateAlert(alert_message=msg, target=self.card_2)]
    # ====================================================
    # ====================================================


    # http request function
    # ====================================================
    def get_season_data(self, phonenum=None, start_time=None, end_time=None, platenum=None):
        send_dict = {
            "service": "website",
            "operation": "get_season_data",
            "database_name": "season"
        }

        if phonenum and not phonenum == "" and len(str(phonenum)) == 10:
            send_dict["phonenum"] = phonenum
        if start_time and len(start_time[2:]) == 15:
            send_dict["start_time"] = start_time[2:]
        if end_time and len(end_time[2:]) == 15:
            send_dict["end_time"] = end_time[2:]
        if platenum and not platenum == "":
            send_dict["platenum"] = platenum

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        self.table_info = json.loads(res_msg)["message"] if json.loads(res_msg)["indicator"] else []
        self.table_info = self.make_time_readable(self.table_info,["validstart","validend"],{"validstart":"_validstart","validend":"_validend"})
        for row in self.table_info:
            row['_season_type'] = self.Lg_transform("SEASON_CHOICE",row['season_type'])

        self.card_2.layout.content[0][0].layout.content[0][0].update({
                "data": self.table_info
            })
        print("self.table_info: ", self.table_info)

    def post_modify(self, _id, license_num, start_time=None, end_time=None, comments=None):
        send_dict = {
            "service": "website",
            "operation": "modify_season_data",
            "id_number": str(_id),
            "database_name": "season",
            "platenum": license_num
        }

        if start_time and len(start_time[2:]) == 15:
            send_dict["start_time"] = start_time[2:]
        if end_time and len(end_time[2:]) == 15:
            send_dict["end_time"] = end_time[2:]
        if comments and not comments == "":
            send_dict["comments"] = comments

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        print(res_msg)
        return json.loads(res_msg)["indicator"]

    def post_insert(self, phonenum, license_num, start_num, end_num, database_name, season_type, month_fee, comments):
        send_dict = {
            "service": "website",
            "operation": "post_season_data",
            "carpark_id": self.carpark_id,
            "phonenum": phonenum,
            "platenum": license_num,
            "start_time": start_num,
            "end_time": end_num,
            "database_name": database_name,
            "season_type": season_type,
            "months_fee": month_fee,
            "comments": comments
        }

        res_msg = Famcy.FManager.http_client.client_post("main_http_url", send_dict)
        print(res_msg)
        return json.loads(res_msg)["indicator"]

    def get_default_date_time(self):
        current_time = datetime.datetime.now()

        default_date = ""
        default_date += str(current_time.year) + "-"
        default_date += str(current_time.month) + "-" if len(str(current_time.month)) == 2 else "0" + str(current_time.month) + "-"
        default_date += str(current_time.day) if len(str(current_time.day)) == 2 else "0" + str(current_time.day)

        default_end_date = ""
        default_end_date += str(current_time.year) + "-"
        default_end_date += str(current_time.month) + "-" if len(str(current_time.month)) == 2 else "0" + str(current_time.month) + "-"
        default_end_date += str(int(current_time.day)+1) if len(str(int(current_time.day)+1)) == 2 else "0" + str(int(current_time.day)+1)

        return default_date, "00:00", default_end_date, "00:00"
    # ====================================================
    # ====================================================


    # utils function
    # ====================================================
    def read_excel_file(self, file_path):
        print("read_excel")
        df = pd.read_excel(file_path)
        write_data = df.to_dict('records')
        print("write_data")
        return_dict = {}
        for row in write_data:
            for columns in row.keys():
                try:
                    return_dict[columns].append(row[columns])
                except:
                    return_dict[columns] = [row[columns]]

        return return_dict

    def change_table_info_to_dict(self):
        return_dict = {}
        for row in self.table_info:
            for columns in row.keys():
                try:
                    return_dict[columns].append(row[columns])
                except:
                    return_dict[columns] = [row[columns]]

        return return_dict

    def make_time_readable(self,data,columns_name,columns_mapping):
        """
        Use to make time friendly to read
        """
        for row in data:
            for column in columns_name:
                if len(row[column]) == 15:
                    row[columns_mapping[column]] = str(row[column][:2]+"年 "+row[column][2:4]+"月"+row[column][4:6]+"日 "+row[column][6:8]+":"+row[column][8:10]+":"+row[column][10:12])
                if len(row[column]) == 12:
                    row[columns_mapping[column]] = str(row[column][:2]+"年 "+row[column][2:4]+"月"+row[column][4:6]+"日 "+row[column][6:8]+":"+row[column][8:10]+":"+row[column][10:12])

        return data

    def Lg_transform(self,group,name,language="CH",reverse=False):
        """
        This function transform the information to the specific language
        Input   
            - group: Need to be ALL CAPITAL WORDS
            - name: the name you would like to translate
            - language: The language you would like to use
            - * reverse: if True 
        Output
            - string 
        Ex. file
            SEASON_CHOICE:
                season: {"CH": "月票","EN": "Monthly pass"}
                dailyseason: {"CH": "早上優惠票","EN": "Morning pass"}
            SEASON_DATABASE:
                season: {"CH": "月票資料庫","EN": "season database"}
                daily:  {"CH": "月票資料庫"}
        Usage:
            1. Lg_transform("SEASON_CHOICE","season","CH") -> "月票"
            2. Lg_transform("SEASON_CHOICE","dailyseason","EN") -> "Morning pass"
            3. Lg_transform("SEASON_DATABASE","season","EN") -> "season database"
            4. Lg_transform("SEASON_CHOICE","月票","CH",True) -> "season"
        Error Usage:
            In most of case, will return the origin name value to avoid fatal crash.
            However, when reverse=True and the name points to different value will raise error.
            1. Lg_transform("SEASON_DATABASE","月票資料庫","CH",True) -> raise error
        """
        language_yaml = read_config_yaml(os.path.expanduser("~/.local/share/famcy/pms/console/Lg_transform.yaml"))

        if reverse:
            if group not in language_yaml.keys():
                raise ValueError("group spelling fail")
            else:
                return_name_list = []
                for i in language_yaml[group].keys():
                    try:
                        if language_yaml[group][i][language] == name:
                            return_name_list.append(i)
                    except:
                        pass
                if len(return_name_list) == 0:
                    raise ValueError("Could not find the specific name for reference")
                elif len(return_name_list) >= 2:
                    raise ValueError("Duplicate Return")
                else:
                    return_name = return_name_list[0]
        else:
            try:
                return_name = language_yaml[group][name][language]
            except:
                return_name = name

        return return_name

    def get_carpark_id(self):
        send_dict = {
            "service": "pms",
            "operation": "get_carpark_id"
        }
        try:
            res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
            res_msg = json.loads(res_msg)
            if res_msg['indicator']:
                self.carpark_id_ = res_msg['message']
                self.carpark_id = res_msg['message']
                config = Famcy.FManager["ConsoleConfig"]
                if "carpark_id" not in config.keys():
                    config['carpark_id'] = res_msg['message']
                    # write_yaml(os.path.expanduser("~")+"/.local/share/famcy/pms/console/famcy.yaml",config)
            else:
                config = Famcy.FManager["ConsoleConfig"]
                self.carpark_id = config['carpark_id']
                self.carpark_id_ = config['carpark_id']

        except Exception as e:
        
            raise ValueError("could not find carpark_id")   

# page = SeasonPage()
SeasonPage.register("/season", Famcy.ClassicStyle(), permission_level=1, background_thread=False)