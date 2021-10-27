import markdown
import Famcy
import json

class inputBtn(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = inputBtn.generate_template_content()
        super(inputBtn, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "inputBtn",
            "desc": "",
            "input_type": "number",                         # ("number" / "text" / "password")
            "num_range": None,                              # if type == number ([0, 10] / None)
            "placeholder": "",
            "mandatory": False,
            "button_name": "送出",                          # btn name in same section must not be same
            "action_after_post": "clean",                   # (clean / save)
        }

    def render_inner(self):
        addition_text = ""
        if self.value["input_type"] == "number" and self.value["num_range"]:
            addition_text = ' min="' + str(self.value["num_range"][0]) + '" max="' + str(self.value["num_range"][1]) + '" '
        input_html = '<div id="' + self.id + '" class="inputBtn"><label for="' + self.id + "_input" + '">' + self.value["title"] + '</label><p>' + self.value["desc"] + '</p><input type="' + self.value["input_type"] + '" id="' + self.id + "_input" + '" name="' + self.name + '" placeholder="' + self.value["placeholder"] + '"' + self.extra_keyup + addition_text + self.mandatory + '><input type="submit" name="send" value="' + self.value["button_name"] + '"></div>' + self.extra_script
        return input_html
