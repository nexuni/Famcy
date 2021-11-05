import Famcy
import json

class h4(Famcy.FamcyElement):
    def __init__(self):
        super(h4, self).__init__()

    def render_inner(self):
        html = "<h4" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</h4>"
        return html