import Famcy
import json

class h1(Famcy.FamcyElement):
    def __init__(self):
        super(h1, self).__init__()

    def render_inner(self):
        html = "<h1" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self
        self.html = html
        html += "</h1>"
        return html