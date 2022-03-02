import Famcy
import os
import json
import requests
import urllib
import time

class GraphPage(Famcy.FamcyPage):
    def __init__(self):
        super(GraphPage, self).__init__()

        # for declaration
        # ===============
        self.card_0 = self.card0()
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()

        self.layout.addWidget(self.card_0, 0, 0, 1, 2)
        self.layout.addWidget(self.card_1, 1, 0)
        self.layout.addWidget(self.card_3, 1, 1)
        self.layout.addWidget(self.card_2, 2, 0, 1, 2)
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        card0 = Famcy.FamcyCard()
        card0.title = "Documentation of display fblocks:"

        _displayParagraph0 = Famcy.displayParagraph()
        _displayParagraph0.update({
                "title": "",
                "content":  '''
###Feature###
---
    Extra function of fblock:
    * generate_png_file(img_name="<Name of png file>")

    Usage:
    * pip3 install plotly, pandas, kaleido

    Troubleshooting:
    * Missing orca when using generate_png_file: https://stackoverflow.com/questions/58473837/plotly-missing-orca

'''
            })

        _displayParagraph1 = Famcy.displayParagraph()
        _displayParagraph1.update({
                "title": "",
                "content":  '''
###bar_chart###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * values: [{"x": [<Graph data>], "y": [<Graph data>], "color": "Color of line"}] <type: list [<type: dict {"x": <type: list [<type: int]>, "y": <type: list [<type: int]>, "color": <type: str>}>]>
    * labels: ["List of bar names"] <type: list [<type: str>]>
    * xy_axis_title: ["Title of X axis", "Title of Y axis"] <type: list [<type: str>]>
    * size: [<Value of bar width>, <Value of bar height>] <type: list [<type: int>]>
'''
            })
        _displayParagraph2 = Famcy.displayParagraph()
        _displayParagraph2.update({
                "title": "",
                "content":  '''
###line_chart###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * labels: ["List of line names"] <type: list [<type: str>]>
    * values: [{"x": [<Graph data>], "y": [<Graph data>], "color": "Color of line", "mode": "Type of line", "marker_size": "Size of marker", "line_width": <Width of line>}] <type: list [<type: dict {"x": <type: list [<type: int]>, "y": <type: list [<type: int]>, "color": <type: str>, "mode": <type: str ("lines+markers" | "lines" | "markers")>, "marker_size": <type: int>, "line_width": <type: int>}>]>
'''
            })
        _displayParagraph3 = Famcy.displayParagraph()
        _displayParagraph3.update({
                "title": "",
                "content":  '''
###pie_chart###
---
    Values of fblock:
    * values: [{"number": <Value>}] <type: list [<type: dict {"number": <type: int>}>]>
    * labels: ["List of pie labals"] <type: list [<type: str>]>
    * size: [<Value of bar width>, <Value of bar height>] <type: list [<type: int>]>
'''
            })
        
        card0.layout.addWidget(_displayParagraph0, 0, 0, 1, 3)
        card0.layout.addWidget(_displayParagraph1, 1, 0)
        card0.layout.addWidget(_displayParagraph2, 1, 1)
        card0.layout.addWidget(_displayParagraph3, 1, 2)


        return card0

    def card1(self):
        card1 = Famcy.FamcyCard()

        _pie_chart = Famcy.pie_chart()
        _pie_chart.update({
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
	            "labels": ["Pie1", "Pie2", "Pie3", "Pie4"],
	            "size": [500, 500], # width, height
	        })

        card1.layout.addWidget(_pie_chart, 0, 0)
        return card1 

    def card2(self):
        card2 = Famcy.FamcyCard()

        _line_chart = Famcy.line_chart()
        _line_chart.update({
                "title": "Title of line_chart",
                "labels": ["Line1", "Line2", "Line3"],
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
                }]
            })

        card2.layout.addWidget(_line_chart, 0, 0)
        return card2
    

    def card3(self):
        card3 = Famcy.FamcyCard()

        _bar_chart = Famcy.bar_chart()
        _bar_chart.update({
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
	            "labels": ["Bar1", "Bar2"],
	            "title": "Title of bar_chart",
	            "xy_axis_title": ["Title of X axis", "Title of Y axis"],
	            "size": [500, 500]
	        })

        card3.layout.addWidget(_bar_chart, 0, 0)
        return card3
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
GraphPage.register("/graphExample", Famcy.ClassicStyle(), permission_level=0, background_thread=False)