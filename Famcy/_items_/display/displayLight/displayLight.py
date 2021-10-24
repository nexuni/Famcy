import markdown
import Famcy
import json

class displayLight(Famcy.FamcyBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = displayLight.generate_template_content()
        super(displayLight, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "Traffic light",
            "status": {"red": "bulb_red", "yellow": "", "green": ""}, 
            "light_size": "30%",
        }

    def render_inner(self):
        inner_html = '<div id="' + self.id + '" class="displayLight"><div class="bulb_holder" style="width: ' + self.value["light_size"] + ';"><div class="bulb ' + self.value["status"]["red"] + '"></div><div class="bulb ' + self.value["status"]["yellow"] + '"></div><div class="bulb ' + self.value["status"]["green"] + '"></div></div></div>'
        return inner_html
