import Famcy
import json

class input(Famcy.FamcyElement):
    def __init__(self):
        super(input, self).__init__()

    def render_inner(self):
        html = "<input" + self.setAttrTag() + ">"
        return html