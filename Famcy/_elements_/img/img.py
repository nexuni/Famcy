import Famcy
import json

class img(Famcy.FamcyElement):
    def __init__(self):
        super(img, self).__init__()

    def render_inner(self):
        html = "<img" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</img>"
        return html