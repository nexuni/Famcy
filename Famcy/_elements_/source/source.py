import Famcy
import json

class source(Famcy.FamcyElement):
    def __init__(self):
        super(source, self).__init__()

    def render_element(self):
        return "<source" + self.setAttrTag() + ">"