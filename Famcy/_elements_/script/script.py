import Famcy
import json

class script(Famcy.FamcyElement):
    def __init__(self):
        super(script, self).__init__()

    def render_inner(self):
        html = "<script" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
        self.html = html
        html += "</script>"
        return html