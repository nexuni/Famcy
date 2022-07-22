import Famcy
import math
import numpy as np
import copy
from .gmap_block import *
from .canvas_block import *
from .joyStick import *
from .timePicker import *
# from .video_example import *


import json
from flask import current_app
import urllib
import time
from threading import Thread
import cv2
import base64

ROS_DATA_A = [21.661754608154297, 20.893672943115234, 3.3902435302734375, -12.318791389465332, -5.298501968383789, -16.059478759765625, -22.065702438354492, -15.99377727508545, -31.821977615356445, -10.552935600280762, 0.2519207000732422, 61.06772232055664, 12.825460433959961, 61.705596923828125, 23.228116989135742, 56.6130485534668, 25.614919662475586, 46.3193244934082, 28.461362838745117, 32.952735900878906, 22.679168701171875, 20.540454864501953]
K_coefficient = 1
DX_coefficient = 0
DY_coefficient = 0

def T_coefficient(data):
    """
    data: [10, 20, 30, 40, 50, 60]
    """
    x_list = [data[i] for i in range(len(data)) if i % 2 == 0]
    y_list = [data[i] for i in range(len(data)) if i % 2 == 1]

    dx = min(x_list) if min(x_list) < 0 else 0
    dy = min(y_list) if min(y_list) < 0 else 0

    x_len = max(x_list)-min(x_list)

    return (CANVAS_W / x_len) / 2, dx, dy

def TA_action(A_data):
    global K_coefficient, DX_coefficient, DY_coefficient
    K_coefficient, DX_coefficient, DY_coefficient = T_coefficient(A_data)

    b_list = []
    for x, y in zip(*[iter(A_data)]*2):
        b_list.append(K_coefficient*(y - DY_coefficient))
        b_list.append(K_coefficient*(x - DX_coefficient))

    return b_list


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


# class video_eventsourceApi(Famcy.FamcyPage):
#     def __init__(self):
#         super(video_eventsourceApi, self).__init__()

#         self.id = "famcy_video1"

#         t1 = Thread(target=self.send_frame)
#         t1.start()

#     def send_frame(self):
#         capture = cv2.VideoCapture("rtsp://demo:demo@ipvmdemo.dyndns.org:5541/onvif-media/media.amp?profile=profile_1_h264&sessiontimeout=60&streamtype=unicast")
#         with Famcy.app.app_context():
#             while True:
#                 try:
#                     time.sleep(0.01)

#                     success, frame = capture.read()
                    
#                     if not success:
#                         pass
#                     else:
#                         ret, buffer = cv2.imencode('.jpg', frame)
#                         frame = buffer.tobytes()
#                         b64 = base64.b64encode(buffer).decode("utf-8")

#                         html = "<img src='data:image/jpeg;base64,"+str(b64) +"'>"
                        
#                         Famcy.sse.publish({"video": True, "indicator": True, "message": {"target_id": self.id, "target_innerHTML": html, "target_attribute": {}}}, type='video')

#                 except Exception as e:
#                     print("error: ", e)
            

#     # def callback(self):
#     #     if self.get_request_args("edit_day") and self.get_request_args("start_time") and self.get_request_args("end_time"):
#     #         self.style.setReturnValue(indicator=True, message="Succeed")
#     #     else:
#     #         self.style.setReturnValue(indicator=False, message="Something wrong")

# video_eventsourceROUTE = "/video_eventsource"
# video_eventsourceapi = video_eventsourceApi()
# video_eventsourceApi.register(video_eventsourceROUTE, Famcy.APIStyle(), init_cls=video_eventsourceapi)
# # video_eventsourceapi.style.setAction(video_eventsourceapi.callback)


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
        # self.card_1 = self.card1()
        # self.card_2 = self.card2()
        # ===============

        self.layout.addWidget(self.card_0, 0, 0)
        # self.layout.addWidget(self.card_1, 1, 0)
        # self.layout.addWidget(self.card_2, 2, 0)

        self.p_card_1 = self.p_card1()
        # self.p_card_2 = self.p_card2()
        self.layout.addStaticWidget(self.p_card_1)
        # self.layout.addStaticWidget(self.p_card_2)

        # self.thread_update_msg = Famcy.FamcyBackgroundTask(self)
        
    # background task function 
    # ====================================================
    # def background_thread_inner(self):
    #     # self.thread_update_msg.associate(self.test,info_dict={},target=self._d)
    #     # Famcy.FamcyBackgroundQueue.add(self.thread_update_msg,Famcy.FamcyPriority.Standard)
    #     pass

    # def test(self):
    #     print("test")
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        _card = Famcy.FamcyCard()

        # self._d = Famcy.table_block()



        _v = cv2_video()
        _v.update({
            "video_link": 'rtsp://10.0.1.202'
            })

        _card.layout.addWidget(_v, 0, 0)



        
        # _card.layout.addWidget(self.g_map, 0, 0)
        # _card.layout.addWidget(self._d, 1, 0)

        return _card

    def card1(self):
        _card = Famcy.FamcyCard()

        # _joy = joyStick(permission=0)
        _v = cv2_video()
        _v.update({
            "video_link": 'rtsp://10.0.1.202'
            })

        _card.layout.addWidget(_v, 0, 0)

        return _card

    def card2(self):
        _card = Famcy.FamcyCard()

        _input_form = Famcy.input_form()

        _sb = Famcy.submitBtn()
        _sb.connect(self.joy_start)

        _input_form.layout.addWidget(_sb, 0, 0)

        _card.layout.addWidget(_input_form, 0, 0)

        return _card
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def p_card1(self):
        _card = Famcy.FamcyCard()

        _joy = joyStick(permission=0)
        _card.layout.addWidget(_joy, 0, 0)

        _input_form = Famcy.input_form()

        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "submit"
            })
        sb_btn.connect(self.joy_close)

        _input_form.layout.addWidget(sb_btn, 0, 0)

        _card.layout.addWidget(_input_form, 1, 0)

        return _card

    def p_card2(self):
        _card = Famcy.FamcyCard()

        _input_form = Famcy.input_form()

        self.streaming = Famcy.video_stream()
        self.streaming.is_prompt_card = True
        self.streaming.update({
                "delay": 0.01,
                "route_name": "/map",
                "video_link": "rtsp://rtsp.stream/pattern", # robot_data[0][ROBOT_STREAM_URL],
                "stream_flag": True,
                "snap": False,
                "size": [200,160]

            })
        sb_btn = Famcy.submitBtn()
        sb_btn.update({
                "title": "submit"
            })
        sb_btn.connect(self.video_close)

        _input_form.layout.addWidget(sb_btn, 0, 0)

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
                "points": TA_action(ROS_DATA_A),
                "pos": {"x": 0, "y": 0},
                "more_info": {"width": 5, "color": "blue"}
            }],
        })
        self.card_0.layout.removeWidget(self.g_map)
        self.card_0.layout.addWidget(self.g_canvas, 0 ,0)
        Famcy.FManager["google_map"] = False
        # return Famcy.UpdateBlockHtml(target=self.card_0)

    def Prompt_info(self, submission_obj, info):
        if info.raw_data == {}:
            return Famcy.UpdatePrompt(target=self.p_card_1)
        else:
            for kname in info.raw_data.keys():
                if kname != "origin":
                    b_list = info.raw_data[kname]["p1"][::-1] + info.raw_data[kname]["p2"][::-1] + info.raw_data[kname]["p3"][::-1] + info.raw_data[kname]["p4"][::-1]
                    a_list = self.B_rotation(self.B_scale(self.minus_Z_action(b_list, info.raw_data["origin"]["x"], info.raw_data["origin"]["y"]), info.raw_data["origin"]["scaleX"], info.raw_data["origin"]["scaleY"]), info.raw_data["origin"]["rotation"])
                    result = self.A_divide_k(a_list)

                    print("result: ", b_list)
                    print(result)
            return Famcy.UpdateNothing()

    def Prompt_close(self, submission_obj, info):
        name = info["name"]
        color = info["color"]
        _extra_script = "c_showRect('" + name + "', '" + color + "')"
        return Famcy.UpdateRemoveElement(target=self.p_card_1, prompt_flag=True, extra_script=_extra_script)

    def video_start(self, submission_obj, info):
        self.streaming.update({
                "stream_flag": True,
            })
        self.streaming.end_thread = True
        self.streaming.postload = self.streaming.start_thread()
        return [Famcy.UpdatePrompt(target=self.p_card_2)]

    def video_close(self, submission_obj, info):
        print("video_close")
        self.streaming.update({
                "stream_flag": False,
            })
        # self.streaming.end_thread = True
        # self.streaming.is_alive = False
        return [Famcy.UpdateBlockHtml(target=self.streaming), Famcy.UpdateRemoveElement(prompt_flag=True)]

    def joy_start(self, submission_obj, info):
        return [Famcy.UpdatePrompt(target=self.p_card_1)]

    def joy_close(self, submission_obj, info):
        return Famcy.UpdateRemoveElement(prompt_flag=True)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    

    def minus_Z_action(self, B_data, dx, dy):
        ta_list = []
        for x, y in zip(*[iter(B_data)]*2):
            ta_list.append(x-dx)
            ta_list.append(y-dy)

        return ta_list

    def B_scale(self, B_data, scaleX, scaleY):
        s_inverse_b_list = []
        for x, y in zip(*[iter(B_data)]*2):
            s_inverse_b_list.append(x/scaleX)
            s_inverse_b_list.append(y/scaleY)

        return s_inverse_b_list

    def B_rotation(self, B_data, rad):
        a_list = []
        for x, y in zip(*[iter(B_data)]*2):
            a_list.append(math.cos(rad)*x-math.sin(rad)*y)
            a_list.append(math.sin(rad)*x+math.cos(rad)*y)

        return a_list

    def A_divide_k(self, a_list):
        result = []
        for x, y in zip(*[iter(a_list)]*2):
            result.append(x/K_coefficient + DX_coefficient)
            result.append(y/K_coefficient + DY_coefficient)

        return result
    


    # ====================================================
    # ====================================================

   
testPage.register("/test", Famcy.ClassicStyle(), permission_level=0, background_thread=False, event_source_flag=True)





class cv2_video(Famcy.FamcyBlock):
    """
    Represents the block to display
    cv2_video. 
    """
    def __init__(self, **kwargs):
        self.uniq_channal = "video"+str(id(self))
        # self.del_thread()
        self.value = cv2_video.generate_template_content()

        super(cv2_video, self).__init__(**kwargs)

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
            "video_link": ''
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = "famcy_video1"

        _s = Famcy.script()
        _s.innerHTML = '''
            source.addEventListener('video', function(event) {
                console.log("video")
                var data = JSON.parse(event.data);
                update_event_source_target(data)
            }, false);
            '''

        self.body.addStaticScript(_s)

    # def send_frame(self):
    #     with Famcy.app.app_context():
    #         # capture = cv2.VideoCapture("rtspsrc location="+self.value["video_link"]+" user-id=admin user-pw=@minc135246 is-live=true protocols=tcp ! rtph265depay ! h265parse ! nvv4l2decoder ! nvvidconv ! videoconvert ! appsink drop=true sync=false", cv2.CAP_GSTREAMER)
    #         capture = cv2.VideoCapture(self.value["video_link"])
    #         while True:
    #             # time.sleep(self.value["delay"])
    #             time.sleep(0.1)
    #             # frame = capture.read()[1]
    #             success, frame = capture.read()
    #             print("video: ", success)
    #             if not success:
    #                 pass
    #             else:
    #                 ret, buffer = cv2.imencode('.jpg', frame)
    #                 frame = buffer.tobytes()
    #                 b64 = base64.b64encode(buffer).decode("utf-8")

    #                 html = "<img src='data:image/jpeg;base64,"+str(b64) +"'>"
    #                 print("Famcy.sse: ==============>")
    #                 Famcy.sse.publish({"video": True, "indicator": True, "message": {"target_id": self.id, "target_innerHTML": html, "target_attribute": {}}}, type='video')

    def render_inner(self):
        # t1 = Thread(target=self.send_frame)
        # t1.start()
        return self.body