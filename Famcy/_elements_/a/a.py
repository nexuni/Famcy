import Famcy
import json

class a(Famcy.FamcyElement):
    def __init__(self):
        super(a, self).__init__()

    def render_inner(self):
        html = "<a" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</a>"
        return html