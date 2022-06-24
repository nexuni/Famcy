import Famcy
import json

class link(Famcy.FamcyElement):
    def __init__(self):
        super(link, self).__init__()

    def render_element(self):
        return "<link" + self.setAttrTag() + ">"