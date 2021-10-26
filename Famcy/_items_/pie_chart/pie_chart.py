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
        self.value = pie_chart.generate_template_content()
        super(pie_chart, self).__init__(**kwargs)

        self.header_script += '<script src="/static/js/pie_chart.js"></script>'

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
            "size": [400, 400], # width, height
        }

    def render_inner(self):
        pie_values = []
        for num in self.value["values"]:
            pie_values.append(num["number"])
            
        json_pie_dict_values = json.dumps(pie_values)
        json_pie_dict_labels = json.dumps(self.value["labels"])
        json_pie_dict_size = json.dumps(self.value["size"])

        return """<div id="%s"></div><script>generatePieChart("%s", %s, %s, %s)</script>""" % (self.id, self.id, json_pie_dict_values, json_pie_dict_labels, json_pie_dict_size)

        