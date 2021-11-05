import Famcy
import json

class div(Famcy.FamcyElement):
    def __init__(self):
        super(div, self).__init__()

    def render_inner(self):
        html = "<div" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</div>"
        return html
