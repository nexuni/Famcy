import Famcy
import os
import json
import requests
import datetime

class FinancePage(Famcy.FamcyPage):
    def __init__(self):
        super(FinancePage, self).__init__("/finance", Famcy.ClassicSideStyle(), background_thread=False)

        self.carpark_id = "park1"
        self.entry_station = "E1"

        self.p_date_card = self.prompt_card_date()

        self.card_1 = self.card1()
        self.card_2 = self.card2()

        self.layout.addWidget(self.card_1, 0, 0)
        self.layout.addWidget(self.card_2, 1, 0)

    # card
    # ====================================================
    def card1(self):
        card1 = Famcy.FamcyCard()
        card1.title = "Revenue"

        input_form = Famcy.input_form()

        input_date = Famcy.pureInput()
        input_time = Famcy.pureInput()
        input_date2 = Famcy.pureInput()
        input_time2 = Famcy.pureInput()

        input_date.update({"title": "輸入起始日期", "input_type": "date"})
        input_time.update({"title": "輸入起始時間", "input_type": "time"})
        input_date2.update({"title": "輸入結束日期", "input_type": "date"})
        input_time2.update({"title": "輸入結束時間", "input_type": "time"})

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

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_time, 0, 1)
        input_form.layout.addWidget(input_date2, 0, 2)
        input_form.layout.addWidget(input_time2, 0, 3)
        input_form.layout.addWidget(search_type, 1, 0)
        input_form.layout.addWidget(chart_type, 1, 1)
        input_form.layout.addWidget(time_range, 1, 2)
        
        input_form.layout.addWidget(search_btn, 1, 3)

        card1.layout.addWidget(input_form, 0, 0)

        return card1

    def card2(self):
        card2 = Famcy.FamcyCard()
        card2.title = "Receipt"

        upload_form = Famcy.upload_form()

        upload_file = Famcy.uploadFile()
        upload_file.update({
                "title": "檔案上傳",
                "file_num": "single",
                "accept_type": ["xls", "xlsx"],
                "file_path": 'C:/Users/user/FamcyDownload/',
            })

        submit_btn = Famcy.submitBtn()
        submit_btn.update({"title": "送出檔案"})
        submit_btn.connect(self.submit_file , target=card2)

        upload_form.layout.addWidget(upload_file, 0, 0)
        upload_form.layout.addWidget(submit_btn, 1, 0)


        input_form = Famcy.input_form()

        download_btn = Famcy.submitBtn()
        download_btn.update({"title": "下載檔案"})

        input_form.layout.addWidget(download_btn, 0, 0)

        card2.layout.addWidget(upload_form, 0, 0)
        card2.layout.addWidget(input_form, 1, 0)

        return card2
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
        submit_btn.connect(self.send_file_path_to_server)

        cancel_btn = Famcy.submitBtn()
        cancel_btn.update({"title":"返回"})
        cancel_btn.connect(self.prompt_remove_input)

        input_form.layout.addWidget(input_date, 0, 0)
        input_form.layout.addWidget(input_date2, 0, 1)
        input_form.layout.addWidget(cancel_btn, 1, 0)
        input_form.layout.addWidget(submit_btn, 1, 1)

        p_card.layout.addWidget(input_form, 0, 0)

        return p_card
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def prompt_remove_input(self, submission_obj, info_list):
        return Famcy.UpdateRemoveElement(prompt_flag=True)

    def submit_file(self, submission_obj, info_list):
        print("info_list: ", info_list)
        msg = "檔案上傳失敗，請重新再試"
        if info_list[0][0]["indicator"]:
            self.p_date_card["file_name"] = info_list[0][0]["message"]
            return Famcy.UpdatePrompt(target=self.p_date_card)
        return Famcy.UpdateAlert(alert_message=msg)

    def send_file_path_to_server(self, submission_obj, info_list):
        msg = "檔案上傳失敗，請重新再試"
        if len(info_list[0]) > 0 and len(info_list[1]) > 0:
            start_time = "".join(info_list[0][0].split("-"))[2:] + "000000000"
            end_time = "".join(info_list[1][0].split("-"))[2:] + "235959000"

            if self.get_receipt_match(start_time, end_time, self.p_date_card["file_name"]):
                msg = "成功上傳檔案"
                return [Famcy.UpdateRemoveElement(prompt_flag=True), Famcy.UpdateAlert(alert_message=msg, target=self.card_2)]
        return Famcy.UpdateAlert(alert_message=msg)

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

            if self.get_chart_info(start_time, end_time, chart_type=chart_type):
                msg = "成功修改資料"

        return [Famcy.UpdateAlert(alert_message=msg), Famcy.UpdateBlockHtml(target=self.card_1)]
    # ====================================================
    # ====================================================


    # http request function
    # ====================================================
    def get_chart_info(self, start_time, end_time, chart_type=None):
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

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        res_ind = json.loads(res_msg)["indicator"]
        res_msg = json.loads(res_msg)["message"]

        if res_ind:
            values = res_msg["values"]
            self.card_1.layout.content[0][0].layout.removeWidget(2, 0)
            if chart_type == "pie":
                pie_graph = Famcy.pie_chart()
                pie_graph.update({
                        "values": values,
                        "labels": res_msg["labels"],
                        "size": [1000, 500], # width, height
                    })
                self.card_1.layout.content[0][0].layout.addWidget(pie_graph, 2, 0, 1, 4)

            else:
                for val in values:
                    val["color"] = "rgb(164, 99, 230)"
                bar_graph = Famcy.bar_chart()
                bar_graph.update({
                        "values": values,
                        "labels": ["bar1"],
                        "size": [1000, 500], # width, height
                    })
                self.card_1.layout.content[0][0].layout.addWidget(bar_graph, 2, 0, 1, 4)

        return res_ind

    def get_receipt_match(self, start_time, end_time, file_name):
        send_dict = {
            "service": "pms",
            "operation": "receipt_match",
            "start_time": start_time, 
            "end_time": end_time,
            "excel_location": self.card_2.layout.content[0][0].layout.content[0][0].value["file_path"]+file_name
        }

        res_msg = Famcy.FManager.http_client.client_get("main_http_url", send_dict)
        return json.loads(res_msg)["indicator"]
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   

page = FinancePage()
page.register()