import markdown
import Famcy
import json

class inputParagraph(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = inputParagraph.generate_template_content()
        super(inputParagraph, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "inputParagraph",
            "desc": "",
            "height": "300px",                                  # eg: ("200px")
            "placeholder": "",
            "mandatory": True,
            "action_after_post": "save",                    # (clean / save)
        }

    def render_inner(self):
        input_html = '<div id="' + self.id + '" class="inputParagraph"><label for="' + self.id + "_inputParagraph" + '">' + self.value["title"] + '</label><p>' + self.value["desc"] + '</p><textarea style="height: ' + self.value["height"] + ';" id="' + self.id + "_inputParagraph" + '" name="' + self.name + '" placeholder="' + self.value["placeholder"] + '"' + self.extra_keyup + self.mandatory + '></textarea></div>' + self.extra_script
        return input_html
