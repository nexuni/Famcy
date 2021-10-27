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
                "mandatory": False,
                "action_after_post": "clean",                    # (clean / save)
            }

    def render_inner(self):
        input_html = '<div id="' + self.id + '" class="inputPassword"><label for="' + self.id + "_input" + '">' + self.value["title"] + '</label><p>' + self.value["desc"] + '</p><div id="' + self.id + "_input" + '" class="' + self.mandatory + '_password"></div></div>' + '<script>$(document).ready(function($) { $("#' + self.id + "_input" + '").strength_meter({strengthMeterClass: "t_strength_meter", name: "' + self.name + '"})});</script>'
        return input_html
