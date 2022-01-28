import Famcy
import io
import os
import json
import datetime
import requests
import boto3
import pandas as pd
import xlsxwriter

PGM_PATH = os.path.abspath(__file__)
PGM_PATH = PGM_PATH.replace("page.py", "_amr_gui_doc")+"/sg-office-ros.pgm"
MAP_INFO_PATH = Famcy.FManager.console+"/pgm/_amr_gui_doc/sg-office-ros.yaml"
POSITION_LIST = [Famcy.FManager.console+"/pgm/_amr_gui_doc/pose.yaml", Famcy.FManager.console+"/pgm/_amr_gui_doc/traj.yaml"]
COLOR_LIST = ["#FF0000", "#FF00FF"]

class PgmPage(Famcy.FamcyPage):
    def __init__(self):
        super(PgmPage, self).__init__()
        self.card_1 = self.card1()
        self.layout.addWidget(self.card_1, 0, 0)

    # card
    # ====================================================
    def card1(self):
        card1 = Famcy.FamcyCard()

        pgm_v = Famcy.pgm_viewer()
        pgm_v.update({
            "pgm_file_path": PGM_PATH,
            "map_info_path": MAP_INFO_PATH,
            "position_files": POSITION_LIST,
            "color_list": COLOR_LIST
        })

        card1.layout.addWidget(pgm_v, 0, 0)

        return card1

    
PgmPage.register("/pgm", Famcy.ClassicStyle(), permission_level=0, background_thread=False)