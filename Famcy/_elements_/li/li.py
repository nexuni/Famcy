import Famcy
import json

class li(Famcy.FamcyElement):
    def __init__(self):
        super(li, self).__init__()

    def render_element(self):
        html = ""

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self
        self.html = html
        return "<li" + self.setAttrTag() + ">" + html + "</li>"