import Famcy
import json

class select(Famcy.FamcyElement):
    def __init__(self):
        super(select, self).__init__()

    def render_inner(self):
        html = "<select" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</select>"
        return html