import Famcy
import json

class p(Famcy.FamcyElement):
    def __init__(self):
        super(p, self).__init__()

    def render_inner(self):
        html = "<p" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</p>"
        return html