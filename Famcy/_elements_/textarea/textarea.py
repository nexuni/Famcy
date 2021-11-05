import Famcy
import json

class textarea(Famcy.FamcyElement):
    def __init__(self):
        super(textarea, self).__init__()

    def render_inner(self):
        html = "<textarea" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</textarea>"
        return html