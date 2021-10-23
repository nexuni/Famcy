import json
import Famcy
from flask import current_app

class bar_chart(Famcy.FamcyBlock):
    """
    Represents the block to display
    bar_chart. 
    """
    def __init__(self, **kwargs):
        super(bar_chart, self).__init__(**kwargs)
        self.header_script = """<script src="%s/static/js/bar_chart.js"></script>%s""" % (current_app.config.get("main_url", ""), header_script)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "values": [{
                "x": [1995, 1996, 1997, 1998, 1999, 2000],
                "y": [219, 146, 112, 127, 124, 180],
                "color": "rgb(55, 83, 109)"
            },
            {
                "x": [1995, 1996, 1997, 1998, 1999, 2000],
                "y": [200, 246, 132, 120, 198, 110],
                "color": "rgb(55, 83, 109)"
            }],
            "labels": ["bar1", "bar2", "bar3"],
            "title": "bar_chart",
            "xy_axis_title": ["x_title", "y_title"],
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_inner(self):
        """
        context = {
            "values": [{
                "x": [1995, 1996, 1997, 1998, 1999, 2000],
                "y": [219, 146, 112, 127, 124, 180],
                "color": "rgb(55, 83, 109)"
            },
            {
                "x": [1995, 1996, 1997, 1998, 1999, 2000],
                "y": [200, 246, 132, 120, 198, 110],
                "color": "rgb(55, 83, 109)"
            }],
            "labels": ["bar1", "bar2", "bar3"],
            "title": "bar_chart",
            "xy_axis_title": ["x_title", "y_title"]
        }
        """

        for action in context["before_function"]:
            action(context, **configs)

        data = []
        for dict, label in zip(context["values"], context["labels"]):
            temp = {}
            temp["x"] = dict["x"]
            temp["y"] = dict["y"]
            temp["type"] = "bar"
            temp["marker"] = {"color": dict["color"]}
            temp["name"] = label

            data.append(temp)

        json_line_dict_values = json.dumps(data)
        json_line_dict_title = json.dumps(context["title"])
        json_line_dict_xy_title = json.dumps(context["xy_axis_title"])
        
        return"""<div id="%s"></div><script>generateBarChart("%s", %s, %s, %s)</script><script>%s('%s', %s)</script>""" % (context["id"], context["id"], json_line_dict_values, json_line_dict_title, json_line_dict_xy_title, context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return """<script src="%s/static/js/bar_chart.js"></script>%s""" % (current_app.config.get("main_url", ""), header_script)