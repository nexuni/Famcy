import markdown
import Famcy
import json

class inputPassword(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = inputPassword.generate_template_content()
        super(inputPassword, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
                "title": "inputPassword",
                "desc": "",
                "mandatory": True,
                "action_after_post": "save",                    # (clean / save)
            }

    def render_inner(self):
        input_html = '<div class="inputPassword"><label for="' + self.id + '">' + self.value["title"] + '</label><p>' + self.value["desc"] + '</p><div id="' + self.id + '" class="' + self.mandatory + '_password"></div></div>' + '<script>$(document).ready(function($) { $("#' + self.id + '").strength_meter({strengthMeterClass: "t_strength_meter", name: "' + self.name + '"})});</script>'
        return input_html
