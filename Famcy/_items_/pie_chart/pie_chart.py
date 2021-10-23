import json
import Famcy
from flask import current_app

import dash
import dash_core_components as dcc
import dash_html_components as html

class pie_chart(Famcy.FamcyBlock):
    """
    Represents the block to display
    pie_chart. 
    """
    def __init__(self, **kwargs):
        super(pie_chart, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "values": [
                {
                    "number":1
                }, 
                {  
                    "number":1
                }, 
                {
                    "number":2
                }, 
                {   
                    "number":3
                }
            ],
            "labels": ["pie1", "pie2", "pie3", "pie4"],
            "size": [700, 700], # width, height
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        pie_values = []
        for num in context["values"]:
            pie_values.append(num["number"])
            
        json_pie_dict_values = json.dumps(pie_values)
        json_pie_dict_labels = json.dumps(context["labels"])
        json_pie_dict_size = json.dumps(context["size"])

        inner_html = """<div id="%s"></div><script>generatePieChart("%s", %s, %s, %s)</script><script>%s('%s', %s)</script>""" % (self.context["id"], self.context["id"], json_pie_dict_values, json_pie_dict_labels, json_pie_dict_size, context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

        return'<turbo-frame style="width: 100%;" id="t_' + self.context["id"] + '">' + inner_html + '</turbo-frame>'

    def extra_script(self, header_script, **configs):
        return"""<script src="%s/static/js/pie_chart.js"></script>%s""" % (current_app.config.get("main_url", ""), header_script)