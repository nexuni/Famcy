import json
import Famcy
from flask import current_app

class line_chart(Famcy.FamcyBlock):
    """
    Represents the block to display
    line_chart. 
    """
    def __init__(self, **kwargs):
        super(line_chart, self).__init__(**kwargs)

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
                "x": [1, 2, 3, 4],
                "y": [12, 9, 15, 12],
                "mode": "lines+markers",
                "color": "rgb(128, 0, 128)",
                "marker_size": 8,
                "line_width": 1
            },
            {
                "x": [1, 2, 3, 4],
                "y": [2, 9, 1, 3],
                "mode": "lines",
                "color": "rgb(2, 0, 128)",
                "marker_size": 8,
                "line_width": 3
            },
            {
                "x": [1, 2, 3, 4],
                "y": [4, 3, 7, 13],
                "mode": "markers",
                "color": "rgb(128, 0, 2)",
                "marker_size": 12,
                "line_width": 1
            }],
            "labels": ["line1", "line2", "line3"],
            "title": "line_chart",
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):
        """
        context = {
            "values": [{
                "x": [1, 2, 3, 4],
                "y": [12, 9, 15, 12],
                "mode": "lines+markers" (or "lines", "markers"),
                "color": "rgb(128, 0, 128)",
                "marker_size": 8,
                "line_width": 1
            }],
            "labels": ["line1"],
            "title": "line_chart"
        }
        """

        for action in context["before_function"]:
            action(context, **configs)

        data = []
        for dict, label in zip(context["values"], context["labels"]):
            
            temp = {}
            temp["x"] = dict["x"]
            temp["y"] = dict["y"]
            temp["mode"] = dict["mode"]
            temp["name"] = label

            if dict["mode"] == "lines+markers":
                temp["line"] = {
                    "color": dict["color"],
                    "width": dict["line_width"]
                }
                temp["marker"] = {
                    "color": dict["color"],
                    "size": dict["marker_size"]
                }

            elif dict["mode"] == "lines":
                temp["line"] = {
                    "color": dict["color"],
                    "width": dict["line_width"]
                }

            elif dict["mode"] == "markers":
                temp["marker"] = {
                    "color": dict["color"],
                    "size": dict["marker_size"]
                }

            data.append(temp)

        json_line_dict_values = json.dumps(data)
        json_line_dict_title = json.dumps(context["title"])

        return"""<div id="%s"></div><script>generateLineChart("%s", %s, %s)</script><script>%s('%s', %s)</script>""" % (context["id"], context["id"], json_line_dict_values, json_line_dict_title, context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return"""<script src="%s/static/js/line_chart.js"></script>%s""" % (current_app.config.get("main_url", ""), header_script)