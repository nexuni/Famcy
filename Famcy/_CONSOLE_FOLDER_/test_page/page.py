import Famcy
from .gmap_block import *
from .canvas_block import *
from .joyStick import *

class revenueGetApi(Famcy.FamcyPage):
    def __init__(self):
        super(revenueGetApi, self).__init__()

    def callback(self):
        res_dict = {
            "day": {"data": {"x": ["12:00", "13:00", "14:00", "15:00"], "y": [200,300,400,500]}},
            "week": {"data": {"x": ["星期一", "星期二", "星期三", "星期四"],  "y": [200,300,400,500]}},
            "month": {"data": {"x": ["1/1", "1/2", "1/3", "1/4"], "y": [200,300,400,500]}},
            "item": {"data": {"x": ["絕配一", "絕配二", "絕配三", "絕配四", "絕配五", "絕配六"],  "y": [219, 146, 112, 127, 124, 180]}}
        }

        if self.get_request_args("date"):
            self.style.setReturnValue(indicator=True, message=res_dict)
        else:
            self.style.setReturnValue(indicator=False, message="Something wrong")

revenue_ROUTE = "/revenue"
revenue_api = revenueGetApi()
revenueGetApi.register(revenue_ROUTE, Famcy.APIStyle(), init_cls=revenue_api)
revenue_api.style.setAction(revenue_api.callback)

class store_openGetApi(Famcy.FamcyPage):
    def __init__(self):
        super(store_openGetApi, self).__init__()

    def callback(self):
        if self.get_request_args("edit_day") and self.get_request_args("start_time") and self.get_request_args("end_time"):
            self.style.setReturnValue(indicator=True, message="Succeed")
        else:
            self.style.setReturnValue(indicator=False, message="Something wrong")

store_open_ROUTE = "/store_open"
store_open_api = store_openGetApi()
store_openGetApi.register(store_open_ROUTE, Famcy.APIStyle(), init_cls=store_open_api)
store_open_api.style.setAction(store_open_api.callback)



class testPage(Famcy.FamcyPage):
    def __init__(self):
        super(testPage, self).__init__()

        self.g_map = google_map()
        self.g_map.connect(self.Snapshot_gmap)
        self.g_map.clickable = False
        self.layout.addStaticWidget(self.g_map)

        self.g_canvas = canvas_block()
        self.g_canvas.connect(self.Prompt_info)
        self.g_canvas.clickable = False
        self.layout.addStaticWidget(self.g_canvas)

        # for declaration
        # ===============
        self.card_0 = self.card0()
        self.card_1 = self.card1()
        # ===============

        self.layout.addWidget(self.card_0, 0, 0)
        self.layout.addWidget(self.card_1, 1, 0)

        self.p_card_1 = self.p_card1()
        self.layout.addStaticWidget(self.p_card_1)
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        _card = Famcy.FamcyCard()

        _card.layout.addWidget(self.g_map, 0, 0)

        return _card

    def card1(self):
        _card = Famcy.FamcyCard()

        _joy = joyStick()

        _card.layout.addWidget(_joy, 0, 0)

        return _card
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def p_card1(self):
        _card = Famcy.FamcyCard()

        _input_form = Famcy.input_form()

        area_name = Famcy.pureInput()
        area_name.set_submit_value_name("name")
        area_name.update({
                "title": "name",
                "desc": ".",

            })
        area_color = Famcy.pureInput()
        area_color.set_submit_value_name("color")
        area_color.update({
                "title": "color",
                "desc": ".",
            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "submit"
            })
        sb_btn.connect(self.Prompt_close)

        _input_form.layout.addWidget(area_name, 0, 0)
        _input_form.layout.addWidget(area_color, 0, 1)
        _input_form.layout.addWidget(sb_btn, 1, 0, 1, 2)

        _card.layout.addWidget(_input_form, 0, 0)

        return _card
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def Snapshot_gmap(self, submission_obj, info):
        self.g_canvas.update({
            "route": [{
                "key_name": "route_1",
                "points": [10, 20, 30, 40, 50, 60],
                "pos": {"x": 0, "y": 0},
                "more_info": {"width": 5, "color": "blue"}
            }],
        })
        self.card_0.layout.removeWidget(self.g_map)
        self.card_0.layout.addWidget(self.g_canvas, 0 ,0)
        Famcy.FManager["google_map"] = False
        return Famcy.UpdateBlockHtml(target=self.card_0)

    def Prompt_info(self, submission_obj, info):
        if info.raw_data == {}:
            return Famcy.UpdatePrompt(target=self.p_card_1)
        else:
            for kname in info.raw_data.keys():
                print(info.raw_data[kname]["p1"], info.raw_data[kname]["p2"], info.raw_data[kname]["p3"], info.raw_data[kname]["p4"])
            return Famcy.UpdateNothing()

    def Prompt_close(self, submission_obj, info):
        name = info["name"]
        color = info["color"]
        _extra_script = "c_showRect('" + name + "', '" + color + "')"
        return Famcy.UpdateRemoveElement(target=self.p_card_1, prompt_flag=True, extra_script=_extra_script)
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

   
testPage.register("/test", Famcy.ClassicStyle(), permission_level=0, background_thread=False)