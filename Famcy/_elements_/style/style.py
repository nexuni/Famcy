import Famcy
import json

class style(Famcy.FamcyElement):
    def __init__(self):
        super(style, self).__init__()

    def render_inner(self):
        html = "<style" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
        self.html = html
        html += "</style>"
        return html