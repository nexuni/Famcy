import json
import Famcy
from flask import current_app
import urllib
import time

class video_stream(Famcy.FamcyBlock):
    """
    Represents the block to display
    video_stream. 
    """
    def __init__(self, **kwargs):
        self.value = video_stream.generate_template_content()
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
            "desc": "",
            "rtsp_address": ["", "", ""],
            "video_timeout": [5, 5, 5],
            "holder_width": ["50%", "50%", "50%"],
            "holder_height": ["300px", "300px", "300px"],
            "img_path": ["/video_1", "/video_2", "/video_3"]
        }

    def render_inner(self):

        index = 0
        temp = ""
        inner_html = ""
        for w, h, address, timeout, path in zip(self.value["holder_width"], self.value["holder_height"], self.value["rtsp_address"], self.value["video_timeout"], self.value["img_path"]):
            
            temp_script = """
            <script type="text/javascript">
                $('#mbr' + '%s_' + '%s').bind('click', (e) => {
                    e.target.parentElement.previousElementSibling.classList.remove("video_placeholder");
                    e.target.parentElement.previousElementSibling.setAttribute("src", "")
                    e.target.parentElement.previousElementSibling.setAttribute("src", "%s&datetime=" + new Date().getTime())
                });
                $('#mbd' + '%s_' + '%s').bind('click', (e) => {
                    e.target.parentElement.previousElementSibling.classList.add("video_placeholder");
                    e.target.parentElement.previousElementSibling.setAttribute("src", "/static/image/transparent.png")
                });
            </script>
            """ % (index, self.id, path + '?' + urllib.parse.urlencode({"address": address, "timeout": timeout}), index, self.id)

            temp += '<div style="width:' + w + ';" class="video_holder"><img id="' + self.id + '" style="height:' + h + ';" src="' + path + '?' + urllib.parse.urlencode({"address": address, "timeout": timeout, "datetime": time.time()}) + '"><div><button id="mbr' + str(index) + "_" + self.id +'" class="video_submit_btn">' + self.value["refreash_stream"] + '</button><button id="mbd' + str(index) + "_" + self.id +'" class="video_submit_btn">' + self.value["stop_stream"] + '</button></div></div>' + temp_script
            index += 1

        inner_html += '<div class="videoStream"><h3>' + self.value["title"] + '</h3><p>' + self.value["desc"] + '</p><div>' + temp + '</div></div>'
        return inner_html