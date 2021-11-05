import Famcy
import json

class ol(Famcy.FamcyElement):
    def __init__(self):
        super(ol, self).__init__()

    def render_inner(self):
        html = "<ol" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</ol>"
        return html