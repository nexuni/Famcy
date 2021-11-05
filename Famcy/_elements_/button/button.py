import Famcy
import json

class button(Famcy.FamcyElement):
    def __init__(self):
        super(button, self).__init__()

    def render_inner(self):
        html = "<button" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</button>"
        return html