import markdown
import Famcy
import json

class pureInput(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = pureInput.generate_template_content()
        super(pureInput, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "type": "pureInput",
            "title": "pureInput1",
            "desc": "",
            "input_type": "text",                               # text / number
            "num_range": None,                               # if type == number
            "placeholder": "",
            "mandatory": True,
            "action_after_post": "save",                    # (clean / save)
        }

    def render_inner(self):
        addition_text = ""
        if self.value["input_type"] == "number" and self.value["num_range"]:
            addition_text = ' min="' + str(self.value["num_range"][0]) + '" max="' + str(self.value["num_range"][1]) + '" '
        inner_html = '<div class="pureInput"><label for="' + self.id + '">' + self.value["title"] + '</label><p>' + self.value["desc"] + '</p><input type="' + self.value["input_type"] + '" id="' + self.id + '" name="' + self.name + '" placeholder="' + self.value["placeholder"] + '"' + self.extra_keyup + addition_text + self.mandatory + '></div>' + self.extra_script
        return inner_html
