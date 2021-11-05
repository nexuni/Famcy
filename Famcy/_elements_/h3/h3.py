import Famcy
import json

class h3(Famcy.FamcyElement):
    def __init__(self):
        super(h3, self).__init__()

    def render_inner(self):
        html = "<h3" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</h3>"
        return html