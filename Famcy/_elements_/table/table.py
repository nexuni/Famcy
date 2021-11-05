import Famcy
import json

class table(Famcy.FamcyElement):
    def __init__(self):
        super(table, self).__init__()

    def render_inner(self):
        html = "<table" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</table>"
        return html