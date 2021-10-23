import json
import Famcy
from flask import current_app
import urllib
import time

class VideoCamera(object):
    def __init__(self, rtsp_address, timeout=15):
        # 通過opencv獲取實時視頻流
        import cv2
        self.cv_module = cv2
        self.video = self.cv_module.VideoCapture(rtsp_address) 
        self.start_time = time.time()
        self.stop_time  = self.start_time + int(timeout)
        self.is_decoded = False
        self.timeout = int(timeout)
    
    def __del__(self):
        self.video.release()

    @classmethod
    def create_camera_response(cls, rtsp_address, timeout):
        return cls.gen(cls(rtsp_address, timeout), timeout)

    @classmethod
    def gen(cls, camera, timeout):
        camera.start_time = time.time()
        camera.stop_time = camera.start_time + int(timeout)

        while True:
            frame, is_decoded = camera.get_frame()
            # 使用generator函式輸出視頻流， 每次請求輸出的content型別是image/jpeg
            if is_decoded:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    def get_frame(self):
        success, image = self.video.read()
        # 因為opencv讀取的圖片并非jpeg格式，因此要用motion JPEG模式需要先將圖片轉碼成jpg格式圖片
        ret, jpeg = self.cv_module.imencode('.jpg', image)

        is_decoded = (time.time() >= self.stop_time)

        return jpeg.tobytes(), (self.is_decoded or is_decoded)

class video_stream(Famcy.FamcyBlock):
    """
    Represents the block to display
    video_stream. 
    """
    def __init__(self, **kwargs):
        super(video_stream, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "refreash_stream": "刷新",
            "stop_stream": "停止",
            "title": "videoStream",
            "desc": "sdfasdfsadf",
            "rtsp_address": ["", "", ""],
            "video_timeout": [5, 5, 5],
            "holder_width": ["50%", "50%", "50%"],
            "holder_height": ["300px", "300px", "300px"],
            "loader": False,
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        index = 0
        temp = ""
        inner_html = ""
        for w, h, address, timeout in zip(context["holder_width"], context["holder_height"], context["rtsp_address"], context["video_timeout"]):
            
            temp_script = """
            <script type="text/javascript">
                $('#mbr' + '%s_' + '%s').bind('click', (e) => {
                    e.target.parentElement.previousElementSibling.classList.remove("video_placeholder");
                    e.target.parentElement.previousElementSibling.setAttribute("src", "")
                    e.target.parentElement.previousElementSibling.setAttribute("src", "%s&datetime=" + new Date().getTime())
                });
                $('#mbd' + '%s_' + '%s').bind('click', (e) => {
                    e.target.parentElement.previousElementSibling.classList.add("video_placeholder");
                    e.target.parentElement.previousElementSibling.setAttribute("src", "%s/static/image/transparent.png")
                });
            </script>
            """ % (index, context["id"], '/video_feed_' + str(index) + '?' + urllib.parse.urlencode({"address": address, "timeout": timeout}), index, context["id"], current_app.config.get("main_url", ""))

            temp += '<div style="width:' + w + ';" class="video_holder"><img id="' + context["id"] + '" style="height:' + h + ';" src="/video_feed_' + str(index) + '?' + urllib.parse.urlencode({"address": address, "timeout": timeout, "datetime": time.time()}) + '"><div><button id="mbr' + str(index) + "_" + context["id"] +'" class="video_submit_btn">' + context["refreash_stream"] + '</button><button id="mbd' + str(index) + "_" + context["id"] +'" class="video_submit_btn">' + context["stop_stream"] + '</button></div></div>' + temp_script
            index += 1

        inner_html += '<div class="videoStream"><h3>' + context["title"] + '</h3><p>' + context["desc"] + '</p><div>' + temp + '</div></div>'
        return inner_html + '<script>' + context["js_after_func_name"] + '("' + context["id"] + '", ' + json.dumps(context["js_after_func_dict"]) + ')</script>'

    def extra_script(self, header_script, **configs):
        return header_script