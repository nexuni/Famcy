# import json
# import Famcy
# from flask import current_app
# import urllib
# import time
# from threading import Thread
# import cv2
# import base64

# class video_stream(Famcy.FamcyBlock):
#     """
#     Represents the block to display
#     video_stream. 
#     """
#     def __init__(self, **kwargs):
#         self.uniq_channal = "video"+str(id(self))
#         self.del_thread()
#         self.value = video_stream.generate_template_content()

#         super(video_stream, self).__init__(**kwargs)

#         self.init_block()
#         self.is_alive = False
#         self.end_thread = False
#         self.is_prompt_card = False


#     def del_thread(self):
#         if self.get_cookie("uniq_channal") and Famcy.FManager[self.get_cookie("uniq_channal")]:
#             Famcy.FManager[self.get_cookie("uniq_channal")] = False
#         self.set_cookie("uniq_channal", self.uniq_channal)

#     @classmethod
#     def generate_template_content(cls, fblock_type=None):
#         """
#         This is the function that
#         returns the template content 
#         for the given fblock. 
#         - Return a content dictionary
#         """
#         return {
#             "video_link": 'rtsp://rtsp.stream/pattern',
#             "stream_flag": True,
#             "delay": 1,
#             "route_name": "/",
#             "snap": False,
#             "size": None,   # [100,60]
#         }

#     def init_block(self):
#         self.body = Famcy.div()
#         self.body["id"] = self.id

#         _s = Famcy.script()
#         _s.innerHTML = '''
#             var source = new EventSource("/event_source?channel=event_source.%s");
#             source.addEventListener('publish', function(event) {
#                 var data = JSON.parse(event.data);
#                 update_event_source_target(data)
#             }, false);
#             source.addEventListener('error', function(event) {
#                 console.log("Error"+ event)
#             }, false);
#             ''' % (self.uniq_channal)

#         self.body.addStaticScript(_s)

#     def send_frame(self):
#         print("1:", self.is_alive)
#         with Famcy.app.app_context():
#             print("2-1:", self.is_alive)
#             capture = cv2.VideoCapture(self.value["video_link"])
#             print("2:", self.is_alive)
#             while self.value["stream_flag"] and self.is_alive and Famcy.FManager[self.uniq_channal]:
#                 print("3:", self.is_alive, Famcy.FManager[self.uniq_channal])
#                 time.sleep(self.value["delay"])
#                 frame = capture.read()[1]
#                 if self.value["size"]:
#                     frame = cv2.resize(frame, (self.value["size"][0], self.value["size"][1])) 
#                 cnt = cv2.imencode('.jpg',frame)[1]
#                 b64 = base64.b64encode(cnt).decode("utf-8")
#                 html = "<img src='data:image/jpeg;base64,"+str(b64) +"'>"
#                 Famcy.sse.publish({"indicator": True, "message": {"target_id": self.id, "target_innerHTML": html, "target_attribute": {}}}, type='publish', channel='event_source.'+self.uniq_channal)
            
#             # set end thread flag True when the thread is dead
#             self.end_thread = True

#     def send_a_frame(self):
#         capture = cv2.VideoCapture(self.value["video_link"])
#         frame = capture.read()[1]
#         if self.value["size"]:
#             frame = cv2.resize(frame, (self.value["size"][0], self.value["size"][1])) 
#         cnt = cv2.imencode('.jpg',frame)[1]
#         b64 = base64.b64encode(cnt).decode("utf-8")
#         return "data:image/jpeg;base64,"+str(b64)

#     def start_thread(self):
#         print("start_thread")
#         self.is_alive = True
#         t1 = Thread(target=self.send_frame)
#         t1.start()

#     def render_inner(self):
#         if not self.value["snap"]:
#             print("render_inner")
#             # create new threads
#             if not self.is_alive:
#                 print("render_inner 1")
#                 self.is_alive = True

#                 if not self.is_prompt_card:
#                     self.start_thread()

#             else:
#                 print("render_inner 2")
#                 self.is_alive = False
#                 Famcy.FManager[self.uniq_channal] = False
#                 time.sleep(0.5)
#                 print("render_inner 2", self.is_alive, self.end_thread, Famcy.FManager[self.uniq_channal])
#                 # while not self.end_thread:
#                 #     pass
#                 print("render_inner 2", self.__dict__, self.is_alive, self.end_thread)
#                 print("render_inner 3")
#                 self.end_thread = False
#                 self.is_alive = True
#                 print("is_prompt_card")
#                 if not self.is_prompt_card:
#                     print("is_prompt_card in")
#                     self.start_thread()

#             Famcy.FManager[self.uniq_channal] = self.is_alive
                
#         else:
#             self.body.children = []
#             _i = Famcy.img()
#             _i["src"] = self.send_a_frame()
#             self.body.addElement(_i)

#         return self.body

import json
import Famcy
import time
import subprocess

class video_stream(Famcy.FamcyBlock):
    """
    Represents the block to display
    video_stream. 
    """
    def __init__(self, **kwargs):
        self.value = video_stream.generate_template_content()
        super(video_stream, self).__init__(**kwargs)
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
        }

    # @staticmethod
    # def start_rtsp_hls():
    #     list_dir = subprocess.run(["E:\\nexuni\\Famcy\\Famcy\\_CONSOLE_FOLDER_\\_static_\\video\\setup_ffmpeg.sh"])
    #     list_dir.poll()

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id

        _v = Famcy.video()
        _v["id"] = "hls_"+self.id
        _v["className"] = "video-js"
        _v["className"] = "vjs-fluid"
        _v["className"] = "vjs-default-skin"
        _v["controls"] = "controls"
        _v["preload"] = "auto"
        _v["data-setup"] = "{}"

        _src = Famcy.source()
        _src["src"] = "/asset/video/stream.m3u8"
        _src["type"] = "application/x-mpegURL"

        _s = Famcy.script()
        _s.innerHTML = '''
        var player = videojs('%s');
        player.play();
        ''' % ("hls_"+self.id)

        _v.addElement(_src)
        self.body.addElement(_v)
        self.body.addElement(_s)

        _l = Famcy.link()
        _l["href"] = "https://unpkg.com/video.js/dist/video-js.css"
        _l["rel"] = "stylesheet"
        self.body.addStaticScript(_l, position="head")

        _s1 = Famcy.script()
        _s1["src"] = "https://unpkg.com/video.js/dist/video.js"
        self.body.addStaticScript(_s1, position="head")

        _s2 = Famcy.script()
        _s2["src"] = "https://unpkg.com/videojs-contrib-hls/dist/videojs-contrib-hls.js"
        self.body.addStaticScript(_s2, position="head")

    def render_inner(self):
        return self.body