import Famcy
import json

class label(Famcy.FamcyElement):
    def __init__(self):
        super(label, self).__init__()

    def render_inner(self):
        html = "<label" + self.setAttrTag() + ">"

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self
        self.html = html
        html += "</label>"
        return html