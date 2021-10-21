import json
import Famcy
from flask import current_app

class doday_shop(Famcy.FamcyBlock):
    """
    Represents the block to display
    doday_shop. 
    """
    def __init__(self, **kwargs):
        super(doday_shop, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "shop_item": [],
            "submit_type": "update_alert",

            
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        inner_html = ""
        i = 0
        for item in context["shop_item"]:
            inner_html += """
                <button type="submit" id="si_%s_%s" class="shop_item_holder">
                    <div class="shop_content">
                        <div class="shop_img_holder">
                            <img src="%s" />
                        </div>
                        <h3>%s</h3>
                        <h6>NT$ %s / %s 點</h6>
                    </div>
                </button>
            """ % (str(i), context["id"], item["img"], item["title"], item["price"], item["point"])
            i += 1

        return"""
            <form id="%s" method="%s" action="/dashboard%s" onsubmit="return false;">
                <div class="doday_shop_holder">
                    %s
                </div>
            </form>
            <script type="text/javascript">
                for (var i=0; i < %s; i++) {
                    $('#si_' + i + '_%s').bind('click', (e) => {
                        var response_dict = {}
                        response_dict[e.currentTarget.id] = [e.currentTarget.children[0].children[1].innerText]
                        Sijax.request('update_page', ["%s", "%s", "%s", response_dict]);
                    });
                }
            </script>
            
            <script>%s('%s', %s)</script>""" % (context["id"], context["method"], context["action"], inner_html, str(i), context["id"], context["id"], context["action"], context["target_id"], context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return """<link href='%s/static/user_css/doday_shop.css' rel='stylesheet' />%s""" % (current_app.config.get("main_url", ""), header_script)