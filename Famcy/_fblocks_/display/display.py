import markdown
import Famcy
from flask import current_app
import json

class display(Famcy.FamcyBlock):
    """
    Represents the block to display
    normal frontend. 
    """
    def __init__(self, **kwargs):
        super(display, self).__init__(**kwargs)

    @classmethod
    def get_fblock_types(cls):
        """
        This is the class method
        that gets all different types
        of display that it possess
        """
        return ["displayParagraph", "displayTag", "displayImage", "displayLight", "displayStepLoader"]

    @classmethod
    def generate_values_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        if fblock_type:
            # Check whether the type is valid
            assert fblock_type in cls.get_fblock_types()

            if fblock_type == "displayParagraph":
                return {
                "type": "displayParagraph",
                "title": "",
                "content": '''
**Nexuni 会社ウェブサイトの案内** 

    1. 希望能讓來到Nexuni的新朋友都能夠快速地學習並瞭解我們工作時會使用到的軟體、程式語言、工具等等。
    2. 作為能力考核的依據
    3. 整合所有公司內部的管理工具，如發票上傳、PO申請、報帳工具、打卡記錄等

快速入門:

    * 點擊總覽 -> 訓練網介紹（可以看到本網頁的所有的內容簡介
    * 點擊相關訓練內容 -> 開始練習
    * 點擊總覽 -> 學習進度裡面的進度報告（可以看到練習的成果）

（網頁內容的版權皆為Nexuni Co. 擁有）
'''
        }

            elif fblock_type == "displayTag":
                return {
                    "type": "displayTag",
                    "title": "測試不知道這是用來幹嘛的Layout",
                    "content": "到底Display Tag有什麼不一樣？",
                }

            elif fblock_type == "displayImage":
                return {
                    "type": "displayImage",
                    "title": "下面這個解析度也太糟糕了吧",
                    "img_name": [current_app.config.get("main_url", "") + "/static/image/test.jpg", current_app.config.get("main_url", "") + "/static/image/test.jpg", current_app.config.get("main_url", "") + "/static/image/test.jpg"], # This is gathered from static folder or _images_ user folder
                    "img_size": ["50%", "50%", "50%"]
                }

            elif fblock_type == "displayLight":
                return {
                    "type": "displayLight",
                    "title": "Traffic light",
                    "status": {"red": "bulb_red", "yellow": "", "green": ""}, 
                    "light_size": "30%",
                }

            elif fblock_type == "displayStepLoader":
                return {
                    "type": "displayStepLoader",
                    "title": "displayStepLoader1",
                    "steps": ["step1", "step2", "step3"],
                    "steps_status": ["complete", "active", ""]                 # ("" / "complete" / "active")
                }

    @classmethod
    def generate_template_content(cls, fblock_values=None):
        return {
            "values": fblock_values,
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        inner_html = ""
        for value in context["values"]:
            if value["type"] == "displayTag":
                inner_html += '<div class="displayTag"><h3>' + value["title"] + '</h3><h4>' + value["content"] + '</h4></div>'

            elif value["type"] == "displayParagraph":
                inner_html += '<div class="displayParagraph"><h3>' + value["title"] + '</h3><h4>' + markdown.markdown(value["content"]) + '</h4></div>'
                
            elif value["type"] == "displayImage":
                temp = ""
                for img_name, img_size in zip(value["img_name"], value["img_size"]):
                    temp += '<img style="width:' + img_size + ';" src="' + img_name + '">'
                inner_html += '<div class="displayImage"><h3>' + value["title"] + '</h3><div>' + temp + '</div></div>'

            elif value["type"] == "displayLight": 
                inner_html += '<div class="displayLight"><div class="bulb_holder" style="width: ' + value["light_size"] + ';"><div class="bulb ' + value["status"]["red"] + '"></div><div class="bulb ' + value["status"]["yellow"] + '"></div><div class="bulb ' + value["status"]["green"] + '"></div></div></div>'
                
            elif value["type"] == "displayStepLoader":
                temp = ""
                for step_title, step_status in zip(value["steps"], value["steps_status"]):
                    temp += '<li class="is-' + step_status + '"><span>' + step_title + '</span></li>'
                inner_html += '<div class="displayStepLoader"><h3>' + value["title"] + '</h3><ol class="_progress-bar">' + temp + '</ol></div>'
                
        # return inner_html
        return inner_html + '<script>' + context["js_after_func_name"] + '("' + context["id"] + '", ' + json.dumps(context["js_after_func_dict"]) + ')</script>'

    def extra_script(self, header_script, **configs):
        return header_script