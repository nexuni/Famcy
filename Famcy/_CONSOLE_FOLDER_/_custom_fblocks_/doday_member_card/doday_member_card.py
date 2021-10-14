import json
import Famcy
from flask import current_app

class doday_member_card(Famcy.FamcyBlock):
    """
    Represents the block to display
    doday_member_card. 
    """
    def __init__(self, **kwargs):
        super(doday_member_card, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "title": "doday VIP",
            "main_status": "豆粉",
            "sub_title": "20210922",
            "icon_pic": "/static/user_image/doday_icon.png",
            "member_point": "0",
            "accumulated_point": "0",
            "accumulated_money": "0",
            "target_point": {"豆粉": "50", "豆友": "25"},
            "target_money": {"豆粉": "3000", "豆友": "1500"},

            
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        extra_class = "dofan_card" if context["main_status"] == "豆粉" else "doyo_card"

        result_p = "0" if int(context["target_point"][context["main_status"]]) - int(context["accumulated_point"]) < 0 else str(int(context["target_point"][context["main_status"]]) - int(context["accumulated_point"]))
        result_m = "0" if int(context["target_money"][context["main_status"]]) - int(context["accumulated_money"]) < 0 else str(int(context["target_money"][context["main_status"]]) - int(context["accumulated_money"]))
        

        return"""
            <div id="%s" class="doday_holder">
                <div class="doday_card_holder %s">
                    <div class="card_content">
                        <h5 class="card_title">%s</h5>
                        <h1 class="card_main_status">%s</h1>
                        <img src="%s" class="card_icon"/>
                        <h6 class="card_date">%s</h6>
                    </div>
                </div>
                <div class="doday_card_info_holder">
                    <div class="card_content">
                        <div class="card_info_holder">
                            <h4>目前會員點數: </h4>
                            <h6>%s點</h6>
                        </div>
                        <div class="card_info_holder">
                            <h4>會員累積點數: </h4>
                            <h6>%s點/%s點</h6>
                        </div>
                        <div class="card_info_holder">
                            <h4>會員累積消費金額: </h4>
                            <h6>$%s/$%s</h6>
                        </div>
                        <h5>再消費%s點或%s元即可升級!</h5>
                    </div>
                </div>
            </div>
            <script>%s('%s', %s)</script>""" % (context["id"], extra_class, context["title"], context["main_status"], current_app.config.get("main_url", "") + context["icon_pic"], context["sub_title"], context["member_point"], context["accumulated_point"], context["target_point"][context["main_status"]], context["accumulated_money"], context["target_money"][context["main_status"]], result_p, result_m, context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return """<link href='%s/static/user_css/doday_member_card.css' rel='stylesheet' />%s""" % (current_app.config.get("main_url", ""), header_script)