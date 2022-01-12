import Famcy
import os
import io
import json
import requests
import datetime
import boto3
import pandas as pd
import xlsxwriter
from gadgethiServerUtils.file_basics import read_config_yaml,write_yaml


class FinancePage(Famcy.FamcyPage):
    def __init__(self):
        # super(FinancePage, self).__init__("/finance", Famcy.ClassicSideStyle(), background_thread=False)
        super(FinancePage, self).__init__()

        self.get_carpark_id() # init carpark_id 

        #self.carpark_id = "park1"
        self.entry_station = "E1"

        self.p_date_card = self.prompt_card_date()
        self.card4_upload_table = self.p_card_upload_table()

        self.layout.addStaticWidget(self.card4_upload_table)
        self.layout.addStaticWidget(self.p_date_card)

        self.pie_graph = Famcy.pie_chart()
        self.bar_graph = Famcy.bar_chart()
        self.pie_graph_card2 = Famcy.pie_chart()
        self.bar_graph_card3 = Famcy.bar_chart()
        self.bar_graph_card4 = Famcy.bar_chart()
        self.layout.addStaticWidget(self.pie_graph)
        self.layout.addStaticWidget(self.bar_graph)
        self.layout.addStaticWidget(self.pie_graph_card2)
        self.layout.addStaticWidget(self.bar_graph_card3)
        self.layout.addStaticWidget(self.bar_graph_card4)


        self.card_1_graph_data = []
        # self.card_2_graph_data = []
        # self.card_3_graph_data = []

        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()
        self.card_4 = self.card4()
        self.card_5 = self.card5()

        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 1, 0)
        self.layout.addWidget(self.card_3, 2, 0)
        self.layout.addWidget(self.card_4, 3, 0)
        self.layout.addWidget(self.card_5, 4, 0)





    # card
    # ====================================================
    def card1(self):
        card1 = Famcy.FamcyCard()
        card1.title = "收入資料"

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": "00:00"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time", "defaultValue": "23:59"})

        search_type = Famcy.inputList()
        search_type.update({
                "title": "選擇查詢種類",
                "value": ["season", "hourly", "all"]
            })

        chart_type = Famcy.inputList()
        chart_type.update({
                "title": "選擇圖表種類",
                "value": ["pie", "bar"]
            })

        time_range = Famcy.pureInput()
        time_range.update({"title": "輸入時間區段", "input_type": "number"})

        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.generate_chart, target=card1)

        download_btn = Famcy.submitBtn()
        download_btn.update({"title": "下載原始收入資料"})
        download_btn.connect(self.download_graph, target=card1)

        download_link = Famcy.downloadFile()
        download_link.update({"title": "","file_path": 'http://127.0.0.1:5000/robots.xlsx',"file_name": 'download'})
        download_link.body.children[0]["style"] = "visibility: hidden;"

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        input_form.layout.addWidget(search_type, 1, 0, 2, 1)
        input_form.layout.addWidget(chart_type, 1, 1, 2, 1)
        input_form.layout.addWidget(time_range, 1, 2, 2, 1)        
        input_form.layout.addWidget(search_btn, 1, 3)
        input_form.layout.addWidget(download_btn, 2, 3)

        input_form.layout.addWidget(download_link, 3, 0)

        card1.layout.addWidget(input_form, 0, 0)

        graph = Famcy.FamcyCard()
        card1.layout.addWidget(graph, 1, 0)

        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()
        card2.title = "收入來源分析"

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": "00:00"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time", "defaultValue": "23:59"})

        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.generate_revenue_source_chart, target=card2)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        input_form.layout.addWidget(search_btn, 0, 4)

        card2.layout.addWidget(input_form, 0, 0)

        graph = Famcy.FamcyCard()
        card2.layout.addWidget(graph, 1, 0)

        return card2

    def card3(self):
        card3 = Famcy.FamcyCard()
        card3.title = "車格佔用分析"

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": "00:00"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time", "defaultValue": "23:59"})

        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.generate_available_lot_anaylze_chart, target=card3)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        
        input_form.layout.addWidget(search_btn, 0, 4)

        card3.layout.addWidget(input_form, 0, 0)

        graph = Famcy.FamcyCard()
        card3.layout.addWidget(graph, 1, 0)

        return card3

    def card4(self):
        card4 = Famcy.FamcyCard()
        card4.title = "發票比對"


        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_date2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})



        upload_btn = Famcy.submitBtn()
        upload_btn.update({"title": "前往上傳國稅局發票資訊"})
        upload_btn.connect(self.prompt_submit_input, target=self.card4_upload_table)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_date2, 0, 1)
        input_form.layout.addWidget(upload_btn,  1, 0)


        # upload_file = Famcy.uploadFile()
        # upload_file.update({
        #         "title": "檔案上傳",
        #         "file_num": "single",
        #         "accept_type": ["xls", "xlsx"],
        #         "file_path": os.path.expanduser('~')+"/.local/share/famcy/famcy/console/_static_/",
        #     })

        # submit_btn = Famcy.submitBtn()
        # submit_btn.update({"title": "送出檔案"})
        # submit_btn.connect(self.send_file_path_to_server,target=self.p_date_card)

        # _submit_btn = Famcy.submitBtn()
        # _submit_btn.update({"title": "送出檔案"})
        # _submit_btn.connect(self.test , target=self.p_date_card)

        # upload_form.layout.addWidget(upload_file, 0, 0)
        # upload_form.layout.addWidget(submit_btn, 1, 0)
        # upload_form.layout.addWidget(_submit_btn, 2, 0)

        # download_btn = Famcy.downloadFile()
        # download_btn.update({"title": "下載檔案","file_path": 'http://127.0.0.1:5000/static/image/login.png',"file_name": 'login.png'})

        card4.layout.addWidget(input_form, 0, 0)
        # card4.layout.addWidget(download_btn, 2, 0)

        return card4

    def card5(self):
        card5 = Famcy.FamcyCard()
        card5.title = "進出車輛分析"

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time", "defaultValue": "00:00"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time", "defaultValue": "23:59"})

        search_type = Famcy.inputList()
        search_type.update({
                "title": "選擇查詢種類",
                "value": ["season", "hourly", "all"]
            })

        search_btn = Famcy.submitBtn()
        search_btn.update({"title": "查詢"})
        search_btn.connect(self.generate_chart_2, target=card5)


        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        input_form.layout.addWidget(search_type, 1, 0, 2, 1)
        input_form.layout.addWidget(search_btn, 1, 3)

        card5.layout.addWidget(input_form, 0, 0)

        graph = Famcy.FamcyCard()
        card5.layout.addWidget(graph, 1, 0)

        return card5

    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def prompt_card_date(self):
        p_card = Famcy.FamcyPromptCard()

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_date2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.send_file_path_to_server, target=p_card)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_date2, 0, 1)
        input_form.layout.addWidget(cancel_btn, 1, 0)
        input_form.layout.addWidget(submit_btn, 1, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card

    def p_card_upload_table(self):
        p_card = Famcy.FamcyPromptCard()

        upload_form = Famcy.upload_form()

        upload_file = Famcy.uploadFile()
        upload_file.update({
                "title": "檔案上傳",
                "file_num": "single",
                "accept_type": ["xls", "xlsx"],
                "file_path": os.path.expanduser("~")+"/Downloads/",
            })

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title":"確認"})
        submit_btn.connect(self.send_file_path_to_server, target=p_card)

        upload_form.layout.addWidget(upload_file, 0, 0)
        upload_form.layout.addWidget(submit_btn, 0, 1)

        input_form = Famcy.input_form()

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        # input_form.layout.addWidget(upload_form, 0, 0)
        input_form.layout.addWidget(cancel_btn, 1, 0)

        p_card.layout.addWidget(upload_form, 0, 0)
        p_card.layout.addWidget(input_form, 1, 0)

        return p_card
        
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


    def submit_file(self, submission_obj, info_list):
        print("info_list: ", info_list)
        msg = "檔案上傳失敗，請重新再試"
        if info_list[0][0]["indicator"]:
            self.p_date_card["file_name"] = info_list[0][0]["message"]
            msg = "成功上傳檔案"

            return Famcy.UpdatePrompt()
        return Famcy.UpdateAlert(alert_message=msg, target=self.card_2)

    def send_file_path_to_server(self, submission_obj, info_list):
        msg = "檔案上傳失敗，請重新再試"
        Julia = "console.log('IN SEND FILE PATH')"

        print("info_list,==========",info_list)
        print(self.card_4.layout.content[0][0])
        print("====================a")
        if len(info_list[0]) > 0 and len(info_list[1]) > 0:
            print("====================b")
            start_time = "".join(info_list[0][0].split("-"))[2:] + "000000000"
            end_time = "".join(info_list[0][1].split("-"))[2:] + "235959999"

            if self.get_receipt_match(start_time, end_time, self.p_date_card["file_name"]):
                print("====================c")
                msg = "成功上傳檔案"
                self.card_4.layout.content[1][0].layout.content[1][0].update({"file_path": 'https://gadgethi-css.s3.amazonaws.com/pms_download/'+file_name})
                extra_script = "document.getElementById('" + self.card_4.layout.content[1][0].layout.content[1][0].id + "_input').click();"

            return [Famcy.UpdateBlockHtml(target=self.card_4.layout.content[1][0].layout.content[1][0]), Famcy.UpdateAlert(alert_message=msg, extra_script=extra_script)]
        return Famcy.UpdateAlert(alert_message=msg,extra_script=Julia)

    def generate_chart(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][2:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            search_type = str(info_list[4][0])
            chart_type = str(info_list[5][0])
            time_range = str(info_list[6][0])

            if self.get_chart_info(start_time, end_time, chart_type=chart_type, search_type=search_type, time_range=time_range):
                msg = "成功修改資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_1.layout.content[1][0])]

    def generate_chart_2(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][2:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            search_type = str(info_list[4][0])

            if self.get_lot_turnover(start_time, end_time, search_type=search_type):
                msg = "成功查詢"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_5.layout.content[1][0])]


    def generate_revenue_source_chart(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][2:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            
            if self.get_revenue_source(start_time, end_time):
                msg = "成功修改資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_2.layout.content[1][0])]

    def generate_available_lot_anaylze_chart(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][2:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            
            if self.get_available_lot_anaylze(start_time, end_time):
                msg = "成功修改資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_3.layout.content[1][0])]

    def download_graph(self, submission_obj, info_list):
        msg = "資料填寫有誤"
        extra_script = ""
        flag = True
        for _ in info_list:
            if not len(_) > 0:
                flag = False
                break
        if flag:
            start_time = info_list[0][0][2:4] + info_list[0][0][5:7] + info_list[0][0][8:10] + info_list[1][0][:2] + info_list[1][0][3:] + "00000"
            end_time = info_list[2][0][2:4] + info_list[2][0][5:7] + info_list[2][0][8:10] + info_list[3][0][:2] + info_list[3][0][3:] + "00000"
            search_type = str(info_list[4][0])
            chart_type = str(info_list[5][0])
            time_range = str(info_list[6][0])

            if self.get_chart_info(start_time, end_time, chart_type=chart_type, search_type=search_type, time_range=time_range):
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

                    self.card_1.layout.content[0][0].layout.content[9][0].update({"file_path": 'https://gadgethi-css.s3.amazonaws.com/pms_download/'+file_name})
                    extra_script = "document.getElementById('" + self.card_1.layout.content[0][0].layout.content[9][0].id + "_input').click();"

                    msg = "成功加入資料"
                except Exception as e:
                    msg=str(e)
            else:
                msg="請選擇正確時間區間"
        return [Famcy.UpdateBlockHtml(target=self.card_1.layout.content[0][0].layout.content[9][0]), Famcy.UpdateAlert(alert_message=msg, extra_script=extra_script)]
    # ====================================================
    # ====================================================


    # http request function
    # ====================================================
    def get_revenue_source(self, start_time, end_time):
        send_dict = {
            "service": "pms",
            "operation": "get_revenue_source",
            "start_time": start_time, 
            "end_time": end_time
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_ind = json.loads(res_msg)["indicator"]
        res_msg = json.loads(res_msg)["message"]

        if res_ind:
            values = res_msg["values"]
            self.card_2.layout.content[1][0].layout.removeWidget(0, 0)
            self.pie_graph_card2.update({
                    "values": values,
                    "labels": res_msg["labels"],
                    "size": [1000, 500], # width, height
                })
            self.card_2.layout.content[1][0].layout.addWidget(self.pie_graph_card2, 0, 0)

        return res_ind

    def get_available_lot_anaylze(self, start_time, end_time):
        send_dict = {
            "service": "pms",
            "operation": "get_available_lot_anaylze",
            "start_time": start_time, 
            "end_time": end_time
        }
        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_ind = json.loads(res_msg)["indicator"]
        res_msg = json.loads(res_msg)["message"]

        if res_ind:
            values = res_msg["values"]
            self.card_3.layout.content[1][0].layout.removeWidget(0, 0)
            for val in values:
                val["color"] = "rgb(164, 99, 230)"
            self.bar_graph_card3.update({
                    "values": values,
                    "labels": ["bar1"],
                    "size": [1000, 600], # width, height
                    "title": "車格佔用分析",
                    "xy_axis_title": ["","佔用車格"]

                })
            self.card_3.layout.content[1][0].layout.addWidget(self.bar_graph_card3, 0, 0)

        return res_ind

    def get_chart_info(self, start_time, end_time, chart_type=None, search_type=None, time_range=None):
        send_dict = {
            "service": "pms",
            "operation": "get_revenue",
            "start_time": start_time, 
            "end_time": end_time
        }
        if chart_type in ["pie", "bar"]:
            send_dict["chart_type"] = chart_type
        else:
            send_dict["chart_type"] = "bar"

        if search_type:
            send_dict["revenue_type"] = search_type
        if time_range:
            send_dict["time_days"] = time_range

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_ind = json.loads(res_msg)["indicator"]
        res_raw = json.loads(res_msg)["raw_data"]
        res_msg = json.loads(res_msg)["message"]

        if res_ind:
            self.card_1_graph_data = res_raw
            values = res_msg["values"]
            self.card_1.layout.content[1][0].layout.removeWidget(0, 0)
            if chart_type == "pie":
                self.pie_graph.update({
                        "values": values,
                        "labels": res_msg["labels"],
                        "size": [1000, 500], # width, height
                    })
                self.card_1.layout.content[1][0].layout.addWidget(self.pie_graph, 0, 0)

            else:
                for val in values:
                    val["color"] = "rgb(164, 99, 230)"
                self.bar_graph.update({
                        "values": values,
                        "labels": ["bar1"],
                        "size": [1000, 500], # width, height
                        "title": "收入比較表",
                        "xy_axis_title": ["","收入"]
                    })
                self.card_1.layout.content[1][0].layout.addWidget(self.bar_graph, 0, 0)
        else:
            self.card_1_graph_data = []

        return res_ind

    def get_receipt_match(self, start_time, end_time, file_name):
        send_dict = {
            "service": "pms",
            "operation": "receipt_match",
            "start_time": start_time, 
            "end_time": end_time,
            "excel_location": self.card_4.layout.content[1][0].layout.content[0][0].value["file_path"]+file_name
        }

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]
    def get_lot_turnover(self, start_time, end_time,search_type=None):
        send_dict = {
            "service": "pms",
            "operation": "get_lot_turnover",
            "start_time": start_time, 
            "end_time": end_time,
            "revenue_type":search_type
        }

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_ind = json.loads(res_msg)["indicator"]
        res_msg = json.loads(res_msg)["message"]

        if res_ind:
            # values = res_msg["values"]
            self.card_5.layout.content[1][0].layout.removeWidget(0, 0)
            # for val in values:
            #     val["color"] = "rgb(164, 99, 230)"
            self.bar_graph_card4.update({
                    "values": res_msg,
                    "labels": ["進車","出車"],
                    "size": [1000, 500], # width, height
                    "title": "車輛進出表",
                    "xy_axis_title": ["時間","車輛進出"]
                })
            self.card_5.layout.content[1][0].layout.addWidget(self.bar_graph_card4, 0, 0)

        return res_ind
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def change_table_info_to_dict(self):
        return_dict = {}
        for row in self.card_1_graph_data:
            for columns in row.keys():
                try:
                    return_dict[columns].append(row[columns])
                except:
                    return_dict[columns] = [row[columns]]

        return return_dict
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
                config = read_config_yaml(os.path.expanduser("~")+"/.local/share/famcy/pms/console/famcy.yaml")
                if "carpark_id" not in config.keys():
                    config['carpark_id'] = res_msg['message']
                    write_yaml(os.path.expanduser("~")+"/.local/share/famcy/pms/console/famcy.yaml",config)
            else:
                config = read_config_yaml(os.path.expanduser("~")+"/.local/share/famcy/pms/console/famcy.yaml")
                self.carpark_id = config['carpark_id']
                self.carpark_id_ = config['carpark_id']

        except Exception as e:
        
            raise ValueError("could not find carpark_id") 
    # ====================================================
    # ====================================================

   

# page = FinancePage()
FinancePage.register("/finance", Famcy.ClassicStyle(), permission_level=1, background_thread=False)