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
        self.init_block()

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
            "labels": ["bar1", "bar2"],
            "title": "bar_chart",
            "xy_axis_title": ["x_title", "y_title"],
            "size": [500, 500]
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id

        div_temp = Famcy.div()
        script = Famcy.script()

        self.body.addElement(div_temp)
        self.body.addElement(script)

        static_script = Famcy.script()
        static_script["src"] = "/static/js/bar_chart.js"
        self.body.addStaticScript(static_script)

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
        json_size = json.dumps(self.value["size"])

        self.body.children[1].innerHTML = 'generateBarChart("%s", %s, %s, %s, %s)' % (self.id, json_line_dict_values, json_line_dict_title, json_line_dict_xy_title, json_size)
        
        return self.body
