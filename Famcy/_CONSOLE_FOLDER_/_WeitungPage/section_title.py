import Famcy
import json

class sectionTitle(Famcy.FamcyBlock):
    def __init__(self):
        self.value = sectionTitle.generate_template_content()
        super(sectionTitle, self).__init__()
        self.init_block()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "sectionTitle"
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id
        self.body["className"] = "sectionTitle"

        h1 = Famcy.h2()

        self.body.addElement(h1)

    def render_inner(self):
        self.body.children[0].innerHTML = self.value["title"]

        return self.body