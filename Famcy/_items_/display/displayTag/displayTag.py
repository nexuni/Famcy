import markdown
import Famcy
import json

class displayTag(Famcy.FamcyBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = displayTag.generate_template_content()
        super(displayTag, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "displayTag",
            "content": "displayTag content",
        }

    def render_inner(self):
        inner_html = '<div id="' + self.id + '" class="displayTag"><h3>' + self.value["title"] + '</h3><h4>' + self.value["content"] + '</h4></div>'
        return inner_html
