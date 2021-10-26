import json
import Famcy
from flask import current_app

class bar_chart(Famcy.FamcyBlock):
    """
    Represents the block to display
    bar_chart. 
    """
    def __init__(self, **kwargs):
        self.value = bar_chart.generate_template_content()
        super(bar_chart, self).__init__(**kwargs)

        self.header_script += '<script src="/static/js/bar_chart.js"></script>'

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
            "xy_axis_title": ["x_title", "y_title"]
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

        data = []
        for dict, label in zip(self.value["values"], self.value["labels"]):
            temp = {}
            temp["x"] = dict["x"]
            temp["y"] = dict["y"]
            temp["type"] = "bar"
            temp["marker"] = {"color": dict["color"]}
            temp["name"] = label

            data.append(temp)

        json_line_dict_values = json.dumps(data)
        json_line_dict_title = json.dumps(self.value["title"])
        json_line_dict_xy_title = json.dumps(self.value["xy_axis_title"])
        
        return"""<div id="%s"></div><script>generateBarChart("%s", %s, %s, %s)</script>""" % (self.id, self.id, json_line_dict_values, json_line_dict_title, json_line_dict_xy_title)
