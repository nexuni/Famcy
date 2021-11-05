import Famcy
import json

class option(Famcy.FamcyElement):
    def __init__(self):
        super(option, self).__init__()

    def render_inner(self):
        html = "<option" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self

        html += "</option>"
        return html